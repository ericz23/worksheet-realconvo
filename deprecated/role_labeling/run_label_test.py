"""Run speaker labeling on the first N transcripts from the saved dataset.

By default, loads the dataset from ./transcripts_dataset and processes the first 5
examples, printing one JSON object per line (JSONL) to stdout. Optionally, write
to a JSONL file via --output.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

from datasets import load_from_disk

from label_transcript import label_transcript_with_openai, label_transcript_gemini_structured


def main() -> None:
    parser = argparse.ArgumentParser(description="Run speaker labeling on the first N transcripts.")
    parser.add_argument(
        "--dataset-path",
        default=os.path.join(os.path.dirname(__file__), "transcripts_dataset"),
        help="Path to dataset saved via datasets.save_to_disk (default: ./transcripts_dataset)",
    )
    parser.add_argument("--n", type=int, default=5, help="Number of examples to process (default: 5)")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model to use (default: gpt-4o-mini)")
    parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature (default: 0.2)")
    parser.add_argument(
        "--output",
        default="",
        help="If set, write JSONL output to this path. Otherwise, print to stdout.",
    )

    args = parser.parse_args()

    ds = load_from_disk(args.dataset_path)
    medicare_ds = ds.filter(lambda x: x["source_zip"] == "medicare_inbound.zip")
    total = len(medicare_ds)
    count = min(args.n, total)

    outputs: List[Dict[str, Any]] = []
    for i in range(count):
        example = medicare_ds[i]
        text = example.get("text", "")
        # result = label_transcript_with_openai(text, model=args.model, temperature=args.temperature)
        result = label_transcript_gemini_structured(
            transcript=text,
            model="gemini-2.5-flash"
        )
        record = {
            "index": i,
            "segments": result.get("segments", []),
        }
        outputs.append(record)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for rec in outputs:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    else:
        for rec in outputs:
            index = rec.get("index", "?")
            print(f"--- Transcript {index} ---")
            for seg in rec.get("segments", []):
                speaker = seg.get("speaker", "unknown")
                confidence = seg.get("confidence")
                if isinstance(confidence, (int, float)):
                    conf_str = f"{confidence:.2f}"
                else:
                    conf_str = "?"
                text = (seg.get("text", "") or "").strip()
                print(f"{speaker}: {text}  (conf={conf_str})")
            print()


if __name__ == "__main__":
    main()