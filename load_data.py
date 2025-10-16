from datasets import load_dataset

def load_data():
    ds = load_dataset(
        "AIxBlock/92k-real-world-call-center-scripts-english",
        split="train",
        streaming=True
    )
    count = 0
    for i, ex in enumerate(ds):
        try:
            _ = ex 
            count += 1
        except Exception as e:
            print(f"Skipped sample {i}: {e}")
    print(f"Loaded {count} samples successfully.")
    return ds

if __name__ == "__main__":
    ds = load_data()