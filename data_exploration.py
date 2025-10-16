from datasets import load_from_disk


def main():
    ds = load_from_disk("./transcripts_dataset")
    print(f"Total transcripts: {len(ds)}")
    print(f"Fields: {ds.column_names}")
    ex = ds[0]
    print(ex.get("text", ""))
    print(ex)


if __name__ == "__main__":
    main()