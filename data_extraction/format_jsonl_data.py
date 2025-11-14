import json
import random

# Input and output paths
input_path = "transcripts_labeled_gemini.jsonl"
output_path = "gemini_formatted.jsonl"

def convert_transcript_to_gemini_format(transcript):
    """
    Convert one transcript entry to Vertex AI Gemini fine-tuning JSON format.
    Consecutive turns with the same role are merged into one content block.
    """
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
        ]
    }

    contents = []
    prev_role = None
    buffer_text = []

    for seg in transcript.get("segments", []):
        speaker = seg.get("speaker", "").lower()
        text = seg.get("text", "").strip()
        if not text:
            continue

        # Map speaker to Gemini role
        if speaker == "agent":
            role = "model"
        elif speaker == "customer":
            role = "user"

        # If this segment has same role as previous, accumulate text
        if role == prev_role:
            buffer_text.append(text)
        else:
            # Flush previous role buffer
            if buffer_text and prev_role:
                contents.append({
                    "role": prev_role,
                    "parts": [{"text": " ".join(buffer_text)}]
                })
            # Start new role buffer
            buffer_text = [text]
            prev_role = role

    # Flush last accumulated text
    if buffer_text and prev_role:
        contents.append({
            "role": prev_role,
            "parts": [{"text": " ".join(buffer_text)}]
        })

    if not contents:
        return None

    return {
        "systemInstruction": system_instruction,
        "contents": contents
    }


def main():
    input_path = "transcripts_labeled_gemini.jsonl"
    output_path = "gemini_formatted.jsonl"

    # Convert dataset
    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:

        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                transcript = json.loads(line)
                formatted = convert_transcript_to_gemini_format(transcript)
                if formatted:
                    outfile.write(json.dumps(formatted, ensure_ascii=False) + "\n")
            except json.JSONDecodeError as e:
                print("Skipping invalid line:", e)

    print(f"Finished. Saved formatted dataset to: {output_path}")

    # Split into train/validation
    train_path = "gemini_train.jsonl"
    val_path = "gemini_val.jsonl"
    val_ratio = 0.1  # 10% validation

    with open(output_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    random.seed(1)
    random.shuffle(lines)
    split_index = int(len(lines) * (1 - val_ratio))
    train_lines = lines[:split_index]
    val_lines = lines[split_index:]

    with open(train_path, "w", encoding="utf-8") as f:
        f.writelines(train_lines)
    with open(val_path, "w", encoding="utf-8") as f:
        f.writelines(val_lines)

    print(f"Training examples: {len(train_lines)}")
    print(f"Validation examples: {len(val_lines)}")


if __name__ == "__main__":
    main()