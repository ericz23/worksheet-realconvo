from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def encode_sentences(sentences, model):
    embeddings = model.encode(sentences, convert_to_tensor=False)
    return embeddings


model = SentenceTransformer("all-MiniLM-L6-v2")


def process_data(data, model, batch_size=64, max_workers=8):
    rows = []
    for conv in tqdm(data, desc="Processing conversations"):
        if not conv.get("is_appointment", False):
            continue
        segments = conv.get("segments", [])
        first_customer_idx = None
        for i, seg in enumerate(segments):
            if seg["speaker"] == "customer":
                first_customer_idx = i
                break
        if first_customer_idx is None:
            continue
        for i, seg in enumerate(segments):
            if seg["speaker"] != "agent":
                continue
            if i <= first_customer_idx:
                continue
            prev_segments = segments[:i]
            prev_context_text = "\n".join(f"{s['speaker']}: {s['text']}" for s in prev_segments)
            rows.append({
                "turn_index": i,
                "prev_context_text": prev_context_text,
                "prev_context_embedding": None,
                "new_turn_text": seg["text"],
                "appointment_type": conv.get("appointment_type")
            })

    if not rows:
        return rows

    texts = [r["prev_context_text"] for r in rows]
    indices = list(range(len(texts)))
    chunks = [indices[i:i + batch_size] for i in range(0, len(indices), batch_size)]
    embeddings = [None] * len(texts)

    def worker(chunk_indices):
        chunk_texts = [texts[i] for i in chunk_indices]
        chunk_embs = encode_sentences(chunk_texts, model)
        return chunk_indices, chunk_embs

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for chunk_indices, chunk_embs in tqdm(
            executor.map(worker, chunks),
            total=len(chunks),
            desc="Encoding embeddings"
        ):
            for idx, emb in zip(chunk_indices, chunk_embs):
                embeddings[idx] = emb.tolist()

    for r, emb in zip(rows, embeddings):
        r["prev_context_embedding"] = emb
    return rows

if __name__ == "__main__":
    import json
    json_file_path = "annotated/appointment/labeled.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = process_data(data[:1], model, batch_size=64, max_workers=8)
    for i, row in enumerate(rows):
        if i <= 3:
            print(row)
            print("-------------------")