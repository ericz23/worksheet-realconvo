import json
import logging
import random
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "raw_full_dataset.json"
OUTPUT_DIR = BASE_DIR / "formatted_data"
OUTPUT_PATH = OUTPUT_DIR / "gemini_formatted_full.jsonl"
TRAIN_PATH = OUTPUT_DIR / "gemini_train_full.jsonl"
VAL_PATH = OUTPUT_DIR / "gemini_val_full.jsonl"
EVAL_PATH = OUTPUT_DIR / "gemini_eval_full.jsonl"
TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
EVAL_RATIO = 0.1
MAX_SEGMENT_CHARS = 600
SPEAKER_ROLE_MAP = {
    "agent": "model",
    "customer": "user",
}

logger = logging.getLogger(__name__)


def convert_transcript_to_gemini_format(transcript: Dict[str, object]) -> Optional[Dict[str, object]]:
    """Convert a raw transcript to the Gemini fine-tuning schema."""
    system_instruction = {
        "role": "system",
        "parts": [
            {
                "text": (
                    "You are a helpful medical appointment scheduling agent. "
                    "Follow professional call center etiquette and assist the customer in booking, "
                    "rescheduling, or confirming appointments."
                )
            }
        ],
    }

    contents: List[Dict[str, object]] = []
    prev_role: Optional[str] = None
    buffer_text: List[str] = []

    for seg in transcript.get("segments", []):
        speaker = str(seg.get("speaker", "")).strip().lower()
        text = str(seg.get("text", "")).strip()
        if not text:
            continue

        role = SPEAKER_ROLE_MAP.get(speaker)
        if role is None:
            continue

        if role == prev_role:
            buffer_text.append(text)
        else:
            if buffer_text and prev_role:
                contents.append({
                    "role": prev_role,
                    "parts": [{"text": " ".join(buffer_text)}],
                })
            buffer_text = [text]
            prev_role = role

    if buffer_text and prev_role:
        contents.append({
            "role": prev_role,
            "parts": [{"text": " ".join(buffer_text)}],
        })

    if not contents:
        return None

    return {
        "systemInstruction": system_instruction,
        "contents": contents,
    }


def load_raw_dataset(path: Path) -> List[Dict[str, object]]:
    """Load the raw dataset stored as a JSON array."""
    with path.open("r", encoding="utf-8") as infile:
        data = json.load(infile)

    if not isinstance(data, list):
        raise ValueError("Expected the raw dataset to be a JSON array.")

    return data


def has_long_segment(transcript: Dict[str, object], max_chars: int) -> bool:
    """Return True if any segment text exceeds the provided length."""
    for seg in transcript.get("segments", []):
        text = str(seg.get("text", "")).strip()
        if len(text) > max_chars:
            return True
    return False


def has_required_roles(transcript: Dict[str, object]) -> bool:
    """Return True if the transcript contains both agent and customer turns."""
    has_agent = False
    has_customer = False

    for seg in transcript.get("segments", []):
        speaker = str(seg.get("speaker", "")).strip().lower()
        if speaker == "agent":
            has_agent = True
        elif speaker == "customer":
            has_customer = True

        if has_agent and has_customer:
            return True

    return False


def serialize_transcripts(transcripts: List[Dict[str, object]], output_file: Path) -> List[str]:
    """Convert transcripts to Gemini format, write them to disk, and return serialized lines."""
    lines: List[str] = []
    skipped_long = 0
    skipped_empty = 0
    skipped_roles = 0

    with output_file.open("w", encoding="utf-8") as outfile:
        for transcript in transcripts:
            if has_long_segment(transcript, MAX_SEGMENT_CHARS):
                skipped_long += 1
                continue

            if not has_required_roles(transcript):
                skipped_roles += 1
                continue

            formatted = convert_transcript_to_gemini_format(transcript)
            if not formatted:
                skipped_empty += 1
                continue
            serialized = json.dumps(formatted, ensure_ascii=False)
            outfile.write(serialized + "\n")
            lines.append(serialized + "\n")

    if skipped_long:
        logger.info(
            "Skipped %d transcripts with segments exceeding %d characters",
            skipped_long,
            MAX_SEGMENT_CHARS,
        )
    if skipped_empty:
        logger.info("Skipped %d transcripts without usable content", skipped_empty)
    if skipped_roles:
        logger.info("Skipped %d transcripts missing agent or customer turns", skipped_roles)

    return lines


def write_dataset_splits(
    lines: List[str],
    train_file: Path,
    val_file: Path,
    eval_file: Path,
    train_ratio: float,
    val_ratio: float,
    eval_ratio: float,
) -> None:
    """Shuffle serialized lines and persist train/validation/eval splits."""
    if not lines:
        logger.warning("No formatted transcripts were produced; skipping dataset splits.")
        return

    total_ratio = train_ratio + val_ratio + eval_ratio
    if not abs(total_ratio - 1.0) < 1e-6:
        raise ValueError("Train/val/eval ratios must sum to 1.0.")

    random.seed(1)
    random.shuffle(lines)

    total = len(lines)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_lines = lines[:train_end]
    val_lines = lines[train_end:val_end]
    eval_lines = lines[val_end:]

    # Ensure no samples are lost due to rounding.
    if len(train_lines) + len(val_lines) + len(eval_lines) != total:
        eval_lines = lines[val_end:]

    with train_file.open("w", encoding="utf-8") as train_out:
        train_out.writelines(train_lines)
    with val_file.open("w", encoding="utf-8") as val_out:
        val_out.writelines(val_lines)
    with eval_file.open("w", encoding="utf-8") as eval_out:
        eval_out.writelines(eval_lines)

    logger.info("Training examples: %d", len(train_lines))
    logger.info("Validation examples: %d", len(val_lines))
    logger.info("Eval examples: %d", len(eval_lines))


def main() -> None:
    """Entry point for converting the raw dataset into Gemini fine-tuning format."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Loading raw dataset from %s", INPUT_PATH)
    transcripts = load_raw_dataset(INPUT_PATH)
    logger.info("Loaded %d transcripts", len(transcripts))

    formatted_lines = serialize_transcripts(transcripts, OUTPUT_PATH)
    logger.info("Wrote %d formatted transcripts to %s", len(formatted_lines), OUTPUT_PATH)

    write_dataset_splits(
        formatted_lines,
        TRAIN_PATH,
        VAL_PATH,
        EVAL_PATH,
        TRAIN_RATIO,
        VAL_RATIO,
        EVAL_RATIO,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()