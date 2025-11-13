import os
import json
from pathlib import Path
from google import genai
from dotenv import load_dotenv
from pydantic import TypeAdapter
from annotation_structure import Summary
from annotation_structure import Summary

load_dotenv()

def check_and_retrieve_jobs(
    job_tracker_file: str = "submitted_jobs.txt",
    output_path: str = "./annotated/appointment/labeled.json"
):
    if not os.path.exists(job_tracker_file):
        print(f"No job tracker file found: {job_tracker_file}")
        return
    
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    with open(job_tracker_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    job_info = []
    for line in lines:
        job_name, display_name = line.split('\t', 1)
        job_info.append((job_name.strip(), display_name.strip()))
    
    if not job_info:
        print("No jobs to check")
        return
    
    existing_results = []
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            existing_results = json.load(f)
    
    completed_jobs = []
    
    for job_name, display_name in job_info:
        print(f"Checking job: {display_name} ({job_name})")
        
        job_status = client.batches.get(name=job_name)
        state = job_status.state.name
        
        if state == 'JOB_STATE_PENDING' or state == 'JOB_STATE_RUNNING':
            print(f"Job {display_name} is {state}")
            continue
        
        if state == 'JOB_STATE_SUCCEEDED':
            print(f"Job {display_name} succeeded, retrieving results")
            
            batch_results = []
            total_input_tokens = 0
            total_output_tokens = 0
            
            start_id = None
            end_id = None
            if display_name:
                parts = display_name.split('-')
                if len(parts) >= 4:
                    try:
                        start_id = int(parts[-3])
                        end_id = int(parts[-2])
                    except ValueError:
                        pass
            
            responses_list = list(job_status.dest.inlined_responses)
            
            adapter = TypeAdapter(Summary)
            skipped_entries = 0
            
            for i, inline_response in enumerate(responses_list):
                if inline_response.response and inline_response.response.text:
                    try:
                        parsed_summary = adapter.validate_json(inline_response.response.text)
                        parsed_content = parsed_summary.model_dump()
                        
                        if start_id is not None and end_id is not None:
                            if i == 0:
                                parsed_content["id"] = start_id
                            elif i == len(responses_list) - 1:
                                parsed_content["id"] = end_id
                        
                        batch_results.append(parsed_content)
                    except Exception as e:
                        print(f"Skipping entry {i+1} due to validation error: {str(e)}")
                        skipped_entries += 1
                        continue
                    
                    if inline_response.response.usage_metadata:
                        total_input_tokens += inline_response.response.usage_metadata.prompt_token_count or 0
                        total_output_tokens += inline_response.response.usage_metadata.candidates_token_count or 0
            
            print(f"Retrieved {len(batch_results)} results from {display_name}")
            if skipped_entries > 0:
                print(f"Skipped {skipped_entries} invalid entries")
            print(f"Tokens - Input: {total_input_tokens}, Output: {total_output_tokens}, Total: {total_input_tokens + total_output_tokens}")
            
            existing_results.extend(batch_results)
            completed_jobs.append((job_name, display_name))
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(existing_results, f, ensure_ascii=False, indent=2)
        
        elif state == 'JOB_STATE_FAILED':
            print(f"Job {display_name} failed")
            if hasattr(job_status, 'error') and job_status.error:
                print(f"Error: {job_status.error}")
            completed_jobs.append((job_name, display_name))
        
        elif state == 'JOB_STATE_CANCELLED':
            print(f"Job {display_name} was cancelled")
            completed_jobs.append((job_name, display_name))
        
        elif state == 'JOB_STATE_EXPIRED':
            print(f"Job {display_name} expired")
            completed_jobs.append((job_name, display_name))
    
    completed_job_names = {job_name for job_name, _ in completed_jobs}
    remaining_jobs = [(job_name, display_name) for job_name, display_name in job_info if job_name not in completed_job_names]
    
    with open(job_tracker_file, 'w', encoding='utf-8') as f:
        for job_name, display_name in remaining_jobs:
            f.write(f"{job_name}\t{display_name}\n")
    
    print(f"Removed {len(completed_jobs)} completed jobs from tracker")
    print(f"Remaining jobs: {len(remaining_jobs)}")

if __name__ == "__main__":
    check_and_retrieve_jobs(
        job_tracker_file="data_extraction/submitted_jobs.txt",
        output_path="./annotated/appointment/labeled.json"
    )