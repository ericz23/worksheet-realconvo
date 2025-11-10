import os
from google import genai
from pathlib import Path
from typing import Optional
from datasets import load_from_disk
from dotenv import load_dotenv
from annotation_structure import Summary
import time

load_dotenv()

def submit_batch_gemini(batch_indices, subset, model, prompt, batch_num=0, batch_name_prefix="annotation-batch"):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    requests = []
    schema = Summary.model_json_schema()
    for i, idx in enumerate(batch_indices):
        text = subset[idx]["text"] or ""
        requests.append({
            'contents': [{
                'parts': [{'text': f"{prompt}\n\n{text}"}],
                'role': 'user'
            }],
            'config': {
                'response_mime_type': 'application/json',
                'response_schema': schema
            }
        })
    
    start_conv_idx = min(batch_indices)
    end_conv_idx = max(batch_indices)
    display_name = f"{batch_name_prefix}-{start_conv_idx}-{end_conv_idx}-{int(time.time())}"
    batch_job = client.batches.create(
        model=model,
        src=requests,
        config={"display_name": display_name}
    )
    
    job_status = client.batches.get(name=batch_job.name)
    if job_status.state.name == 'JOB_STATE_PENDING':
        return batch_job.name, display_name
    
    return None, None

def submit_dataset_jobs(
    model: str,
    dataset_path: str = "./transcripts_dataset",
    source_zip: str = "medicare_inbound.zip",
    index_start: Optional[int] = None,
    index_end: Optional[int] = None,
    keyword: Optional[str] = None,
    batch_size: int = 100,
    job_tracker_file: str = "submitted_jobs.txt",
    batch_name_prefix: str = "annotation-batch"
):
    ds = load_from_disk(dataset_path)
    subset = ds.filter(lambda x: x.get("source_zip") == source_zip)
    n = len(subset)
    indices = list(range(0 if index_start is None else max(0, index_start),
                         n if index_end is None else min(n, index_end)))
    if keyword:
        indices = [i for i in indices if keyword.lower() in (subset[i]["text"] or "").lower()]
    
    num_batches = (len(indices) + batch_size - 1) // batch_size
    prompt_path = Path("data_extraction/annotation_prompt_simple.txt")
    prompt = prompt_path.read_text(encoding="utf-8")
    
    submitted_jobs = []
    
    for batch_idx in range(num_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(indices))
        batch_indices = indices[start_idx:end_idx]
        
        start_conv_idx = min(batch_indices)
        end_conv_idx = max(batch_indices)
        print(f"Submitting batch {batch_idx + 1}/{num_batches} (conversations {start_conv_idx}-{end_conv_idx}, {len(batch_indices)} total)")
        
        job_name, display_name = submit_batch_gemini(batch_indices, subset, model, prompt, batch_idx + 1, batch_name_prefix)
        
        if job_name:
            with open(job_tracker_file, 'a', encoding='utf-8') as f:
                f.write(f"{job_name}\t{display_name}\n")
            submitted_jobs.append((job_name, display_name))
            print(f"Submitted job: {display_name} ({job_name})")
        else:
            print(f"Failed to submit batch {batch_idx + 1}")
    
    print(f"Submitted {len(submitted_jobs)} jobs, tracking in {job_tracker_file}")

if __name__ == "__main__":
    submit_dataset_jobs(
        model="gemini-2.5-flash",
        dataset_path="./transcripts_dataset",
        source_zip="medicare_inbound.zip",
        index_start=15418,
        # index_end=6000,
        keyword="appointment",
        batch_size=1000,
        job_tracker_file="data_extraction/submitted_jobs.txt",
        batch_name_prefix="appointment-annotation"
    )