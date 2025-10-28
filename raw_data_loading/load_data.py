from datasets import Dataset
from huggingface_hub import snapshot_download
import json
import os
import zipfile
import re

def load_data(save_path: str = "./transcripts_dataset") -> Dataset:
    dataset_name = "AIxBlock/91706-real-world-call-center-scripts-english"

    def normalize(example):
        normalized = {}
        for key, value in example.items():
            if isinstance(value, (dict, list)):
                normalized[key] = json.dumps(value, ensure_ascii=False)
            elif value is None:
                normalized[key] = ""
            else:
                normalized[key] = str(value)
        return normalized

    def generator():
        repo_dir = snapshot_download(repo_id=dataset_name, repo_type="dataset")
        for root, _, files in os.walk(repo_dir):
            for fname in files:
                if not fname.lower().endswith(".zip"):
                    continue
                zip_path = os.path.join(root, fname)
                base = os.path.basename(zip_path)
                # Parse metadata from filename, e.g.:
                # (re-uploaded)PII_Redacted_Transcripts_aixblock-automotive-stereo-inbound-104h.zip
                # Capture domain_topic = "automotive-stereo", call_type = inbound, hours = 104
                m = re.search(r"aixblock-([a-z0-9-]+)-(inbound|outbound)-(\d+)h", base.lower())
                domain_topic = m.group(1) if m else None
                call_type = m.group(2) if m else None
                hours = m.group(3) if m else None
                domain = None
                topic = None
                if domain_topic:
                    parts = domain_topic.split("-")
                    if parts:
                        domain = parts[0]
                        topic = "-".join(parts[1:]) if len(parts) > 1 else None
                try:
                    with zipfile.ZipFile(zip_path) as zf:
                        for member in zf.namelist():
                            if not member.lower().endswith(".json"):
                                continue
                            try:
                                with zf.open(member) as fp:
                                    try:
                                        data = json.load(fp)
                                    except Exception:
                                        try:
                                            text = fp.read().decode("utf-8", errors="ignore")
                                            data = json.loads(text)
                                        except Exception:
                                            continue
                                if isinstance(data, dict):
                                    ex = normalize(data)
                                    # Add derived metadata as strings for consistency
                                    ex["domain"] = domain or ""
                                    ex["topic"] = topic or ""
                                    ex["call_type"] = call_type or ""
                                    ex["collection_hours"] = hours or ""
                                    ex["source_zip"] = base
                                    yield ex
                                elif isinstance(data, list):
                                    for item in data:
                                        if isinstance(item, dict):
                                            ex = normalize(item)
                                            ex["domain"] = domain or ""
                                            ex["topic"] = topic or ""
                                            ex["call_type"] = call_type or ""
                                            ex["collection_hours"] = hours or ""
                                            ex["source_zip"] = base
                                            yield ex
                            except Exception:
                                continue
                except Exception:
                    continue

    train_dataset: Dataset = Dataset.from_generator(generator)
    train_dataset.save_to_disk(save_path)
    return train_dataset

if __name__ == "__main__":
    ds = load_data()
    # print(ds)