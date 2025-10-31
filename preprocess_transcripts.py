"""Convert agent-customer transcripts into labeled, well-formatted conversation data.

This script loads the saved Hugging Face dataset from ./transcripts_dataset and labels each 
transcript using `label_transcript_with_openai`, and writes a structured JSONL file that contains:

- id: sequential index within the filtered subset
- source_zip: original dataset source identifier (for traceability)
- raw_text: the original transcript text
- segments: list of {text, speaker, confidence}
- conversation: a single multiline string with lines like
  "agent: Hello there (conf=0.92)"
- summary: an object summarizing motivation, information exchanged, actions taken, and outcome

Outputs are designed for easy ingestion into downstream LLM policy extraction tasks.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict, List

from datasets import load_from_disk

from role_labeling.label_transcript import label_transcript_with_openai, label_transcript_gemini_structured
from openai import OpenAI

from google import genai
from pydantic import BaseModel
import enum

class SummaryResponse(BaseModel):
    motivation: str
    information_exchanged: str
    actions_taken: str
    outcome: str

def _summarize_conversation_gemini(conversation: str, model: str = "gemini-2.5-flash") -> Dict[str, str]:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    response = client.models.generate_content(
        model=model,
        contents=f"Summarize this customer support call into key fields:\n{conversation}",
        config={
            "response_mime_type": "application/json",
            "response_schema": SummaryResponse
        },
    )
    
    return {
        "motivation": response.parsed.motivation,
        "information_exchanged": response.parsed.information_exchanged,
        "actions_taken": response.parsed.actions_taken,
        "outcome": response.parsed.outcome
    }

def _format_conversation(segments: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for seg in segments:
        speaker = seg.get("speaker", "unknown")
        confidence = seg.get("confidence")
        if isinstance(confidence, (int, float)):
            conf_str = f"{confidence:.2f}"
        else:
            conf_str = "?"
        text = (seg.get("text", "") or "").strip()
        lines.append(f"{speaker}: {text} (conf={conf_str})")
    return "\n".join(lines)


def _summarize_conversation(
    conversation: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
) -> Dict[str, str]:
    """Summarize the conversation into key fields using an OpenAI model.

    Returns a dict with keys: motivation, information_exchanged, actions_taken, outcome.
    """
    client = OpenAI()

    system_instructions = (
        "You are a helpful analyst summarizing a customer support call. "
        "Given the dialog, produce ONLY JSON with keys: "
        "{\"motivation\": str, \"information_exchanged\": str, \"actions_taken\": str, \"outcome\": str}. "
        "Keep it concise and factual. Do not include any text outside JSON."
    )

    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": conversation},
        ],
    )

    content = (completion.choices[0].message.content or "").strip()

    # Try direct JSON parse first
    import json as _json

    try:
        return _json.loads(content)
    except Exception:
        # Minimal fallback: extract first JSON object substring
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return _json.loads(content[start : end + 1])
            except Exception:
                pass
    raise ValueError("Model did not return parseable JSON for summary.")


def _load_turn_prompt_template() -> str:
    """Load the turn metadata extraction prompt template from prompts directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "turn_extraction.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_turn_metadata(
    recent_context: List[Dict[str, Any]],
    current_turn: Dict[str, Any],
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
) -> Dict[str, Any]:
    """Extract minimal turn metadata using OpenAI and a strict prompt template.

    Returns a JSON dict conforming to the minimal schema.
    """
    client = OpenAI()
    system_instructions = _load_turn_prompt_template()

    payload = {
        "recent_context": recent_context,
        "current_turn": current_turn,
    }

    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )

    content = (completion.choices[0].message.content or "").strip()
    try:
        return json.loads(content)
    except Exception:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(content[start : end + 1])
            except Exception:
                pass
    raise ValueError("Model did not return parseable JSON for turn metadata.")


def main_OpenAI() -> None:
    parser = argparse.ArgumentParser(description="Convert auto insurance transcripts into labeled JSONL")
    parser.add_argument(
        "--dataset-path",
        default=os.path.join(os.path.dirname(__file__), "transcripts_dataset"),
        help="Path to dataset saved via datasets.save_to_disk (default: ./transcripts_dataset)",
    )
    parser.add_argument(
        "--source-zip",
        default="medicare_inbound.zip",
        help="Filter value for 'source_zip'",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use for labeling (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature for labeling (default: 0.2)",
    )
    parser.add_argument(
        "--output",
        default="transcripts_labeled.jsonl",
        help="Output JSONL file path (default: ./transcripts_labeled.jsonl)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional limit of examples to process (0 means all)",
    )
    parser.add_argument(
        "--summary-model",
        default="gpt-4o-mini",
        help="OpenAI model to use for summarization (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--turnmeta",
        dest="turnmeta",
        action="store_true",
        default=True,
        help="Enable per-turn metadata extraction (default: on)",
    )
    parser.add_argument(
        "--no-turnmeta",
        dest="turnmeta",
        action="store_false",
        help="Disable per-turn metadata extraction",
    )
    parser.add_argument(
        "--turnmeta-model",
        default="gpt-4o-mini",
        help="OpenAI model to use for turn metadata extraction (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--turnmeta-temperature",
        type=float,
        default=0.0,
        help="Sampling temperature for turn metadata extraction (default: 0.0)",
    )
    parser.add_argument(
        "--turnmeta-context",
        type=int,
        default=3,
        help="Number of previous turns to include as context (default: 3)",
    )

    args = parser.parse_args()

    ds = load_from_disk(args.dataset_path)
    subset = ds.filter(lambda x: x.get("source_zip") == args.source_zip)
    total = len(subset)
    count = total if args.limit in (None, 0) else min(args.limit, total)

    with open(args.output, "w", encoding="utf-8") as f:
        for i in range(count):
            print("Processing", i)
            example = subset[i]
            text = example.get("text", "")
            result: Dict[str, Any] | None = None
            segments: List[Dict[str, Any]] = []
            conversation = ""
            error: Exception | None = None
            summary: Dict[str, Any] = {}
            summary_error: Exception | None = None

            try:
                result = label_transcript_with_openai(
                    text, model=args.model, temperature=args.temperature
                )
            except Exception as e:
                error = e


            if result is not None:
                try:
                    segments = result.get("segments", [])
                    conversation = _format_conversation(segments)
                    error = None  # clear any previous error if we eventually succeeded
                except Exception as e:
                    # Formatting or structure issue; record as error
                    error = e
                    segments = []
                    conversation = ""

            # Summarize conversation (even if labeling failed, attempt using raw text)
            # Prefer using conversation if available; else fall back to raw text.
            summary_input = conversation if conversation else text
            try:
                summary = _summarize_conversation(
                    summary_input,
                    model=args.summary_model,
                )
                summary_error = None
            except Exception as e:
                summary_error = e
                

            # Turn-level metadata extraction 
            if args.turnmeta and segments:
                recent: List[Dict[str, Any]] = []
                for idx, seg in enumerate(segments):
                    # Build context window from previous turns
                    start_ctx = max(0, idx - args.turnmeta_context)
                    recent = [
                        {
                            "turn_index": start_ctx + j,
                            "speaker": segments[start_ctx + j].get("speaker", "unknown"),
                            "text": segments[start_ctx + j].get("text", ""),
                        }
                        for j in range(0, idx - start_ctx)
                    ]

                    current_turn = {
                        "turn_index": idx,
                        "speaker": seg.get("speaker", "unknown"),
                        "text": seg.get("text", ""),
                    }

                    md: Dict[str, Any] = {}
                    md_error: Exception | None = None
                    try:
                        md = _extract_turn_metadata(
                            recent,
                            current_turn,
                            model=args.turnmeta_model,
                            temperature=args.turnmeta_temperature,
                        )
                        md_error = None
                    except Exception as e:
                        md_error = e

                    seg["metadata"] = md
                    seg["metadata_error"] = None if md_error is None else {
                        "type": md_error.__class__.__name__,
                        "message": str(md_error)[:500],
                    }

            record = {
                "id": i,
                "source_zip": example.get("source_zip"),
                "segments": segments,
                "error": None
                if error is None
                else {"type": error.__class__.__name__, "message": str(error)[:500]},
                "summary": summary,
                "summary_error": None
                if summary_error is None
                else {"type": summary_error.__class__.__name__, "message": str(summary_error)[:500]},
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

def main_gemini() -> None:
    parser = argparse.ArgumentParser(description="Convert auto insurance transcripts into labeled JSONL using Gemini")
    parser.add_argument(
        "--dataset-path",
        default=os.path.join(os.path.dirname(__file__), "transcripts_dataset"),
        help="Path to dataset saved via datasets.save_to_disk (default: ./transcripts_dataset)",
    )
    parser.add_argument(
        "--source-zip",
        default="automotive_inbound.zip",
        help="Filter value for 'source_zip'",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash",
        help="Gemini model to use for labeling (default: gemini-2.5-flash)",
    )
    parser.add_argument(
        "--output",
        default="transcripts_labeled_gemini.jsonl",
        help="Output JSONL file path (default: ./transcripts_labeled_gemini.jsonl)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional limit of examples to process (0 means all)",
    )

    parser.add_argument(
        "--retries",
        type=int,
        default=1,
        help="Number of retries if labeling fails (default: 1)",
    )
    parser.add_argument(
        "--summary-model",
        default="gemini-2.5-flash",
        help="Gemini model to use for summarization (default: gemini-2.5-flash)",
    )

    args = parser.parse_args()
    ds = load_from_disk(args.dataset_path)
    subset = ds.filter(lambda x: x.get("source_zip") == args.source_zip)
    total = len(subset)
    count = total if args.limit in (None, 0) else min(args.limit, total)

    print(count, "examples to process.")
    with open(args.output, "w", encoding="utf-8") as f:
        for i in range(count):
            print("Processing", i)
            example = subset[i]
            text = example.get("text", "")
            result: Dict[str, Any] | None = None
            segments: List[Dict[str, Any]] = []
            conversation = ""
            error: Exception | None = None
            summary: Dict[str, Any] = {}
            summary_error: Exception | None = None

            for attempt in range(max(0, args.retries) + 1):
                try:
                    result = label_transcript_gemini_structured(text, model=args.model)
                    break
                except Exception as e:
                    error = e
                    if attempt < max(0, args.retries):
                        time.sleep(1.5 ** attempt)
                    else:
                        result = None

            if result is not None:
                try:
                    segments = result.get("segments", [])
                    conversation = _format_conversation(segments)
                    error = None
                except Exception as e:
                    error = e
                    segments = []
                    conversation = ""

            summary_input = conversation if conversation else text
            for attempt in range(max(0, args.retries) + 1):
                try:
                    summary = _summarize_conversation_gemini(summary_input, model=args.summary_model)
                    summary_error = None
                    break
                except Exception as e:
                    summary_error = e
                    if attempt < max(0, args.retries):
                        time.sleep(1.5 ** attempt)
                    else:
                        summary = {}

            record = {
                "id": i,
                "source_zip": example.get("source_zip"),
                "raw_text": text,
                "segments": segments,
                "conversation": conversation,
                "status": "ok" if error is None else "error",
                "error": None
                if error is None
                else {"type": error.__class__.__name__, "message": str(error)[:500]},
                "summary": summary,
                "summary_error": None
                if summary_error is None
                else {"type": summary_error.__class__.__name__, "message": str(summary_error)[:500]},
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main_OpenAI()