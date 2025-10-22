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
import os
from google import genai
from pydantic import BaseModel
import enum

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


class SpeakerType(str, enum.Enum):
    AGENT = "agent"
    CUSTOMER = "customer"


class TranscriptSegment(BaseModel):
    text: str
    speaker: SpeakerType
    confidence: float


class SegmentResponse(BaseModel):
    segments: list[TranscriptSegment]


def label_transcript_gemini_structured(transcript: str, model: str = "gemini-2.5-flash") -> Dict[str, Any]:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    response = client.models.generate_content(
        model=model,
        contents=f"Split transcript into segments and label each as 'agent' or 'customer' with confidence 0-1:\n{transcript}",
        config={
            "response_mime_type": "application/json",
            "response_schema": SegmentResponse
        },
    )
    
    return {
        "segments": [
            {
                "text": segment.text,
                "speaker": segment.speaker.value,
                "confidence": segment.confidence
            }
            for segment in response.parsed.segments
        ]
    }


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


def main_test() -> None:
    sample_transcript = """
    Hello, thank you for calling Medicare support. How can I assist you today? Hi, I'm having trouble understanding my Medicare Part B coverage. I'd be happy to help you with that. Can you tell me your Medicare ID number? Sure, it's 1ABC-DE2-FG34. Thank you. I can see your account now. What specific questions do you have about Part B?
    
    I want to know if my doctor visits are covered. Yes, Medicare Part B covers doctor visits. You'll typically pay 20 percent after meeting your deductible. That's helpful, but what about prescription drugs? Part B doesn't cover most prescription drugs, but Part D does. Would you like me to explain your Part D coverage as well?
    """
    
    print("Testing Gemini structured output:")
    result = label_transcript_gemini_structured(sample_transcript)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main_test()