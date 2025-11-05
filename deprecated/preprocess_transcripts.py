"""Convert agent-customer transcripts into labeled, well-formatted conversation data.

This script loads the saved Hugging Face dataset from ./transcripts_dataset and labels each 
transcript using `label_transcript_with_openai`, and writes a structured JSONL file that contains:

- id: sequential index within the filtered subset
- source_zip: original dataset source identifier (for traceability)
- raw_text: the original transcript text
- segments: list of {text, speaker, confidence}
- conversation: a single multiline string with lines like
  "agent: Hello there (conf=0.92)"
- summary: an object summarizing motivation, information exchanged, actions taken, outcome, and sub_topic

Outputs are designed for easy ingestion into downstream LLM policy extraction tasks.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from datasets import load_from_disk

from role_labeling.label_transcript import label_transcript_with_openai, label_transcript_gemini_structured
from openai import OpenAI

from google import genai
from pydantic import BaseModel
import enum

_GEMINI_CLIENT: genai.Client | None = None

def _get_gemini_client() -> genai.Client:
    """Return a singleton Gemini client instance."""
    global _GEMINI_CLIENT
    if _GEMINI_CLIENT is None:
        _GEMINI_CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _GEMINI_CLIENT

class SubTopicCategory(enum.Enum):
    PET_APPOINTMENT_SCHEDULING = "Pet Appointment Scheduling"
    DENTAL_APPOINTMENT_REQUESTS = "Dental Appointment Requests"
    OTHER_MEDICAL_APPOINTMENT_MANAGEMENT = "Other Medical Appointment Management"
    MEDICAL_PROCEDURE_INQUIRIES = "Medical Procedure Inquiries"
    BILLING_AND_PAYMENT_INQUIRIES = "Billing and Payment Inquiries"
    PET_INQUIRIES = "Pet Inquiries"
    OTHER = "Other"

class SummaryResponse(BaseModel):
    motivation: str
    information_exchanged: str
    actions_taken: str
    outcome: str
    sub_topic: SubTopicCategory


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

def _summarize_conversation_gemini(conversation: str, model: str = "gemini-2.5-flash") -> Dict[str, str]:
    client = _get_gemini_client()
    
    response = client.models.generate_content(
        model=model,
        contents=(
            "Summarize this customer support call into key fields "
            "(motivation, information_exchanged, actions_taken, outcome, sub_topic).\n"
            "For sub_topic, choose ONLY from these categories:\n"
            "- Pet Appointment Scheduling: Scheduling/rescheduling/canceling vet appointments for animals (mentions: pet/dog/cat/vet/animal hospital). Not general pet advice.\n"
            "- Dental Appointment Requests: Scheduling/rescheduling/canceling dental services (cleaning, fillings, extraction, orthodontics). Not general medical procedures or billing.\n"
            "- Other Medical Appointment Management: Scheduling/rescheduling/canceling medical visits that are not dental and not pets.\n"
            "- Medical Procedure Inquiries: Questions about procedures/tests/surgery/prep/recovery/results/referrals; not scheduling-focused.\n"
            "- Billing and Payment Inquiries: Bills, charges, statements, refunds, prior auth framed as billing, payment plans.\n"
            "- Pet Inquiries: Pet health/medication/general questions without appointment scheduling.\n"
            "- Other: Everything else.\n\n"
            "Rules:\n"
            "- Prefer appointment categories over inquiry if both appear for the same domain.\n"
            "- Output one of the category names exactly, nothing else.\n\n"
            f"Conversation:\n{conversation}"
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": SummaryResponse
        },
    )
    
    return {
        "motivation": response.parsed.motivation,
        "information_exchanged": response.parsed.information_exchanged,
        "actions_taken": response.parsed.actions_taken,
        "outcome": response.parsed.outcome,
        "sub_topic": getattr(response.parsed.sub_topic, "value", response.parsed.sub_topic),
    }

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

def _extract_turn_metadata_Gemini(
    segments: List[Dict[str, Any]],
    context_k: int,
    model: str = "gemini-2.5-flash",
    temperature: float = 0.0,
) -> List[Dict[str, Any]]:
    """Batch extract per-turn metadata for the entire transcript using Gemini.

    The model should return a JSON array of length equal to the number of segments,
    where each element is the metadata for the turn with the same index.
    """
    if not segments:
        return []

    client = _get_gemini_client()
    system_instructions = _load_turn_prompt_template()

    minimal_segments: List[Dict[str, Any]] = [
        {
            "turn_index": idx,
            "speaker": seg.get("speaker", "unknown"),
            "text": seg.get("text", ""),
        }
        for idx, seg in enumerate(segments)
    ]

    payload = {
        "segments": minimal_segments,
        "context_window": int(max(0, context_k)),
    }

    # Instruct the model to return an array aligned to segment indices
    instruction_suffix = (
        "\n\nYou are given the full conversation split into segments with turn_index. "
        "For EACH segment, produce the minimal metadata defined above, using up to 'context_window' "
        "previous segments as context.\n"
        f"Return ONLY a JSON array of length {len(minimal_segments)}, where array[i] corresponds to turn_index i.\n"
        "Do not include any additional keys or explanations."
    )

    response = client.models.generate_content(
        model=model,
        contents=f"{system_instructions}{instruction_suffix}\n\n{json.dumps(payload, ensure_ascii=False)}",
        config={
            "response_mime_type": "application/json",
        },
    )

    content = ""
    try:
        content = (getattr(response, "text", "") or "").strip()
    except Exception:
        content = ""

    data = json.loads(content)

    return data

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
        default=1,
        help="Number of previous turns to include as context (default: 1)",
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
            if segments:
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
        default="medicare_inbound.zip",
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
        "--summary-model",
        default="gemini-2.5-flash",
        help="Gemini model to use for summarization (default: gemini-2.5-flash)",
    )
    parser.add_argument(
        "--turnmeta-model",
        default="gemini-2.5-flash",
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
        default=1,
        help="Number of previous turns to include as context (default: 1)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel workers (default: 8)",
    )

    args = parser.parse_args()
    ds = load_from_disk(args.dataset_path)
    subset = ds.filter(lambda x: x.get("source_zip") == args.source_zip)
    total = len(subset)
    count = total if args.limit in (None, 0) else min(args.limit, total)

    print(count, "examples to process.")

    def _process_transcript(i: int) -> str:
        example = subset[i]
        text = example.get("text", "")
        result: Dict[str, Any] | None = None
        segments: List[Dict[str, Any]] = []
        conversation = ""
        error: Exception | None = None
        summary: Dict[str, Any] = {}
        summary_error: Exception | None = None

        try:
            result = label_transcript_gemini_structured(text, model=args.model)
        except Exception as e:
            error = e

        if result:
            try:
                segments = result.get("segments", [])
                conversation = _format_conversation(segments)
                error = None
            except Exception as e:
                error = e
                segments = []
                conversation = ""

        summary_input = conversation if conversation else text
        try:
            summary = _summarize_conversation_gemini(summary_input, model=args.summary_model)
            summary_error = None
        except Exception as e:
            summary_error = e

        if summary.get("sub_topic") in {"Dental Appointment Requests", "Other Medical Appointment Management"}:

            # Turn-level metadata extraction (single batch call per transcript)
            if segments:
                md_list = _extract_turn_metadata_Gemini(
                    segments,
                    context_k=args.turnmeta_context,
                    model=args.turnmeta_model,
                    temperature=args.turnmeta_temperature,
                )
                for idx, seg in enumerate(segments):
                    if idx < len(md_list) and isinstance(md_list[idx], dict):
                        seg["metadata"] = md_list[idx]
                        seg["metadata_error"] = None
                    else:
                        seg["metadata"] = {}
                        seg["metadata_error"] = {
                            "type": "ValueError",
                            "message": "Batch metadata length mismatch or invalid element",
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
            return json.dumps(record, ensure_ascii=False) + "\n"

        return ""

    # Execute preprocessing in parallel
    with open(args.output, "w", encoding="utf-8") as f:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(_process_transcript, i) for i in range(count)]
            for j, fut in enumerate(as_completed(futures), 1):
                line = fut.result()
                f.write(line)
                if j % 50 == 0:
                    print(f"Completed {j}/{count}")

if __name__ == "__main__":
    main_gemini()