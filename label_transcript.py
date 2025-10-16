"""Minimal LLM-based speaker labeling for support transcripts.

Exposes a single function `label_transcript_with_openai` and a tiny CLI that reads
from a file or stdin and prints JSON with segments labeled as either "agent" or
"customer" with a confidence score in [0,1].
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def label_transcript_with_openai(
    transcript: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """Label transcript segments by speaker using an OpenAI model.

    Args:
        transcript: Raw transcript string to segment and label.
        model: OpenAI model name (e.g., "gpt-4o-mini", "gpt-4o").
        temperature: Sampling temperature; keep low for determinism.

    Returns:
        A dict with key "segments" where each item has fields:
        {"text": str, "speaker": "agent"|"customer", "confidence": float}.
    """
    client = OpenAI()  # Reads OPENAI_API_KEY from env

    system_instructions = (
        "You annotate customer support transcripts. "
        "Split the input transcript into conversational segments and label each as 'agent' or 'customer'. "
        "Return ONLY JSON with the shape: {\"segments\": [{\"text\": str, \"speaker\": \"agent\"|\"customer\", \"confidence\": number in [0,1]}]}. "
        "Do not include explanations or any text outside of JSON."
    )

    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": transcript},
        ],
    )

    content = (completion.choices[0].message.content or "").strip()

    # Try direct JSON parse first
    try:
        return json.loads(content)
    except Exception:
        # Minimal fallback: extract first JSON object substring
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(content[start : end + 1])
            except Exception:
                pass
    raise ValueError("Model did not return parseable JSON output.")


def _read_input_text(path: str | None) -> str:
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    # Read from stdin when no path provided
    import sys

    return sys.stdin.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Label transcript segments by speaker using an OpenAI LLM.")
    parser.add_argument("input", nargs="?", help="Path to transcript file. If omitted, reads from stdin.")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model to use (default: gpt-4o-mini)")
    parser.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature (default: 0.2)")

    args = parser.parse_args()
    transcript = _read_input_text(args.input)
    result = label_transcript_with_openai(transcript=transcript, model=args.model, temperature=args.temperature)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


