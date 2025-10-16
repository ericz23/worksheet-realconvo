from datasets import load_from_disk
import json
import argparse
import os
import sys

# Ensure project root is on sys.path to import src.*
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocess.segments import parse_words, words_to_segments, build_llm_windows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="./transcripts_dataset")
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--max_segments", type=int, default=40)
    parser.add_argument("--overlap", type=int, default=2)
    args = parser.parse_args()

    ds = load_from_disk(args.data_dir)
    ex = ds[args.index]

    words_json = ex.get("words", "")
    words = parse_words(words_json)
    segments = words_to_segments(words)

    metadata = {
        "domain": ex.get("domain", ""),
        "topic": ex.get("topic", ""),
        "call_type": ex.get("call_type", ""),
        "audio_duration": ex.get("audio_duration", ""),
        "source_zip": ex.get("source_zip", ""),
    }

    windows = build_llm_windows(
        segments,
        metadata,
        max_segments_per_window=args.max_segments,
        overlap=args.overlap,
    )

    # Include a preview of subspans of the first few segments
    preview = []
    for s in segments[:3]:
        preview.append({
            "segment_id": s.segment_id,
            "num_subspans": len(s.subspans),
            "subspans": [
                {
                    "idx": sp.idx,
                    "start_ms": sp.start_ms,
                    "end_ms": sp.end_ms,
                    "w_start": sp.w_start,
                    "w_end": sp.w_end,
                    "text": sp.text,
                }
                for sp in s.subspans[:3]
            ],
        })

    print(json.dumps({
        "num_segments": len(segments),
        "first_window": windows[0] if windows else {},
        "segment_subspans_preview": preview,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


