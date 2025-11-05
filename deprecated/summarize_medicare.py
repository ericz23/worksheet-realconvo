"""Summarize Medicare transcripts (conversation-level only) with sub-topic labeling.

Loads the saved Hugging Face dataset, filters to source_zip == "medicare_inbound.zip",
and generates a concise JSON summary for each transcript including:

- motivation
- information_exchanged
- actions_taken
- outcome
- sub_topic (2–5 word sub-topic label)

Writes one JSON object per line (JSONL) for easy downstream clustering and analysis.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import asyncio
from typing import Any, Dict

from datasets import load_from_disk
from openai import OpenAI
from dotenv import load_dotenv
import os
from google import genai
from pydantic import BaseModel


class SummaryWithSubtopic(BaseModel):
    motivation: str
    information_exchanged: str
    actions_taken: str
    outcome: str
    sub_topic: str


async def summarize_conversation_with_subtopic_gemini(
    conversation: str,
    model: str = "gemini-2.5-flash",
) -> Dict[str, str]:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    response = await client.aio.models.generate_content(
        model=model,
        contents=f"Summarize this Medicare support call into key fields with a 2-5 word sub_topic label:\n{conversation}",
        config={
            "response_mime_type": "application/json",
            "response_schema": SummaryWithSubtopic,
        },
    )
    
    return {
        "motivation": response.parsed.motivation,
        "information_exchanged": response.parsed.information_exchanged,
        "actions_taken": response.parsed.actions_taken,
        "outcome": response.parsed.outcome,
        "sub_topic": response.parsed.sub_topic
    }


async def summarize_conversation_with_subtopic(
    conversation: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
) -> Dict[str, str]:
    """Summarize a conversation and return key fields plus a sub_topic.

    Returns a dict with keys: motivation, information_exchanged, actions_taken, outcome, sub_topic.
    """
    client = OpenAI()

    system_instructions = (
        "You are a helpful analyst summarizing a Medicare inbound support call. "
        "Given the dialog, produce ONLY JSON with keys: "
        "{\"motivation\": str, \"information_exchanged\": str, \"actions_taken\": str, \"outcome\": str, \"sub_topic\": str}. "
        "Keep it concise and factual. sub_topic should be a 2–5 word label (e.g., 'prescription refill'). "
        "Do not include any text outside JSON."
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
    raise ValueError("Model did not return parseable JSON summary with sub_topic.")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Medicare transcripts with sub_topic (conversation-level only)")
    parser.add_argument(
        "--dataset-path",
        default=os.path.join(os.path.dirname(__file__), "transcripts_dataset"),
        help="Path to dataset saved via datasets.save_to_disk (default: ./transcripts_dataset)",
    )
    parser.add_argument(
        "--source-zip",
        default="medicare_inbound.zip",
        help="Filter value for 'source_zip' (default: medicare_inbound.zip)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use for summarization (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature for summarization (default: 0.2)",
    )
    parser.add_argument(
        "--output",
        default="medicare_conversation_summaries_with_subtopic.jsonl",
        help="Output JSONL file path (default: ./medicare_conversation_summaries_with_subtopic.jsonl)",
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
        help="Number of retries if summarization fails (default: 1)",
    )

    args = parser.parse_args()

    # Load environment variables (including OPENAI_API_KEY) from .env
    load_dotenv()

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

            summary: Dict[str, Any] = {}
            summary_error: Exception | None = None
            for attempt in range(max(0, args.retries) + 1):
                try:
                    # summary = summarize_conversation_with_subtopic(
                    #     text,
                    #     model=args.model,
                    #     temperature=args.temperature,
                    # )
                    summary = await summarize_conversation_with_subtopic(text)
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
                "summary": summary,
                "summary_error": None
                if summary_error is None
                else {"type": summary_error.__class__.__name__, "message": str(summary_error)[:500]},
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    asyncio.run(main())