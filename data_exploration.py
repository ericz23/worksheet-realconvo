from datasets import load_from_disk
from collections import Counter


def main():
    ds = load_from_disk("./transcripts_dataset")
    print(f"Total transcripts: {len(ds)}")
    print(f"Fields: {ds.column_names}")
    ex = ds[0]
    print(ex.get("text", ""))

    # Print unique 'domain' values with counts
    sources = ds["source_zip"]
    counts = Counter(sources)
    print("Unique sources and counts:")
    for source, count in sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        print(f"{source}: {count}")



if __name__ == "__main__":
    main()