import os
from typing import Dict, Any
from pydantic import TypeAdapter
from google import genai
from openai import OpenAI
from pathlib import Path
import asyncio
from typing import Optional
from datasets import load_from_disk
import json
from dotenv import load_dotenv
from tqdm.asyncio import tqdm_asyncio

from annotation_structure import LabeledConversation

load_dotenv()

def one_pass_annotate(conversation: str, model: str, use_gemini: bool = True) -> Dict[str, Any]:
    prompt_path = Path("data_extraction/annotation_prompt.txt")
    prompt = prompt_path.read_text(encoding="utf-8")
    if use_gemini:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        resp = client.models.generate_content(
            model=model,
            contents=f"{prompt}\n\n{conversation}",
            config={
                "temperature": 0.0,
                "response_mime_type": "application/json",
                "response_schema": LabeledConversation,
            },
        )
        parsed = resp.parsed
        return parsed.model_dump()
    else:
        client = OpenAI()
        schema = LabeledConversation.model_json_schema()
        comp = client.chat.completions.create(
            model=model,
            temperature=0.0,
            response_format={"type": "json_schema", "json_schema": {"name": "LabeledConversation", "schema": schema, "strict": True}},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": conversation},
            ],
        )
        content = comp.choices[0].message.content
        adapter = TypeAdapter(LabeledConversation)
        obj = adapter.validate_json(content)
        return obj.model_dump()

async def label_dataset(
    model: str,
    use_gemini: bool = True,
    dataset_path: str = "./transcripts_dataset",
    source_zip: str = "medicare_inbound.zip",
    index_start: Optional[int] = None,
    index_end: Optional[int] = None,
    workers: int = 8,
    output_path: str = "./medicare_samples/labeled.json"
):
    ds = load_from_disk(dataset_path)
    subset = ds.filter(lambda x: x.get("source_zip") == source_zip)
    n = len(subset)
    a = 0 if index_start is None else max(0, index_start)
    b = n if index_end is None else min(n, index_end)
    indices = list(range(a, b))
    sem = asyncio.Semaphore(workers)
    async def run_one(i: int):
        async with sem:
            text = subset[i]["text"] or ""
            data = await asyncio.to_thread(one_pass_annotate, text, model, use_gemini)
            data["id"] = i
            data["source_zip"] = subset[i].get("source_zip")
            return data
    tasks = [asyncio.create_task(run_one(i)) for i in indices]
    results = []
    for coro in tqdm_asyncio.as_completed(tasks, total=len(tasks), desc="Annotating"):
        r = await coro
        results.append(r)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return results

if __name__ == "__main__":
    asyncio.run(label_dataset(model = "gemini-2.5-flash",
                              use_gemini = True,
                              dataset_path = "./transcripts_dataset",
                              source_zip = "medicare_inbound.zip",
                              index_start = 0,
                              index_end = 3,
                              workers = 4,
                              output_path = "./medicare_labeled.json"))