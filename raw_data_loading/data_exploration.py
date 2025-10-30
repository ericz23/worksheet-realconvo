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
    
    # auto_insurance_ds = ds.filter(lambda x: x["source_zip"] == "auto_insurance_customer_service_inbound.zip")
    # for i in range(10):
    #     ex = auto_insurance_ds[i]
    #     print("\nTranscript", i, ":")
    #     print(ex.get("text", ""))
    
    # auto_ds = ds.filter(lambda x: x["source_zip"] == "automotive_inbound.zip")
    # for i in range(10):
    #     ex = auto_ds[i]
    #     print("\nTranscript", i, ":")
    #     print(ex.get("text", ""))

    # home_service_ds = ds.filter(lambda x: x["source_zip"] == "home_service_inbound.zip")
    # for i in range(10):
    #     ex = home_service_ds[i]
    #     print("\nTranscript", i, ":")
    #     print(ex.get("text", ""))



if __name__ == "__main__":
    main()