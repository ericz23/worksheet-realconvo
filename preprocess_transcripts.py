"""Convert agent-customer transcripts into labeled, well-formatted conversation data.

This script loads the saved Hugging Face dataset from ./transcripts_dataset and labels each 
transcript using `label_transcript_with_openai`, and writes a structured JSONL file that contains:

- id: sequential index within the filtered subset
- source_zip: original dataset source identifier (for traceability)
- raw_text: the original transcript text
- segments: list of {text, speaker, confidence}
- conversation: a single multiline string with lines like
  "agent: Hello there (conf=0.92)"

Outputs are designed for easy ingestion into downstream LLM policy extraction tasks.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict, List

from datasets import load_from_disk

from label_transcript import label_transcript_with_openai


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert auto insurance transcripts into labeled JSONL")
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
        "--retries",
        type=int,
        default=1,
        help="Number of retries if labeling fails (default: 1)",
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

            # Retry loop for robustness
            for attempt in range(max(0, args.retries) + 1):
                try:
                    result = label_transcript_with_openai(
                        text, model=args.model, temperature=args.temperature
                    )
                    break
                except Exception as e:
                    error = e
                    if attempt < max(0, args.retries):
                        # Exponential backoff: 1s, 1.5s, 2.25s, ...
                        time.sleep(1.5 ** attempt)
                    else:
                        # Exhausted retries; proceed to write an error record
                        result = None

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
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()


