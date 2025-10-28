import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
import json
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import asyncio

from google import genai

load_dotenv()

def encode_sentences(sentences, model):
    embeddings = model.encode(sentences, convert_to_tensor=True)
    return embeddings

def get_sentences_from_summaries(summaries_file = "medicare_conversation_summaries_with_subtopic.jsonl"):
    summaries = []
    with open(summaries_file, "r") as f:
        for line in f:
            data = json.loads(line.strip())
            summaries.append(data['summary']['motivation'])
    # print(summaries[:5])
    return summaries

def cluster_embeddings(embeddings, n_clusters=8, random_state=0):
    X = [e.detach().cpu().numpy().ravel() for e in embeddings]
    X = np.stack(X, axis=0)
    X_unit = normalize(X, norm='l2')
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=random_state)
    labels = kmeans.fit_predict(X_unit)
    return labels

def find_elbow(embeddings, k_range=range(2, 10)):
    X = [e.detach().cpu().numpy().ravel() for e in embeddings]
    X = np.stack(X, axis=0)
    X_unit = normalize(X, norm='l2')
    inertias = []
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X_unit)
        inertias.append(km.inertia_)
    plt.plot(list(k_range), inertias, marker='o')
    plt.xlabel("k")
    plt.ylabel("Inertia (within-cluster variance)")
    plt.show()

def get_clusters(summaries, labels):
    clusters = [[] for _ in range(max(labels) + 1)]
    for summary, label in zip(summaries, labels):
        clusters[label].append(summary)
    return clusters

async def summarize_from_cluster(clusters):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    cluster_summaries = []
    for cluster in clusters:
        cluster_text = "\n".join(f"- {summary}" for summary in cluster)
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""Find the common topic among these conversation summaries and provide a succinct 2-3 word label:

{cluster_text}

Examples:
- Multiple appointment scheduling topics → "scheduling appointments"
- Various billing/payment issues → "billing inquiries" 
- Different coverage questions → "coverage verification"

Common topic:"""
        )
        cluster_summaries.append(response.text)
    return cluster_summaries

def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Loading summaries...")
    summaries = get_sentences_from_summaries()
    print("Encoding sentences...")
    embeddings = encode_sentences(summaries, model)
    # find_elbow(embeddings, k_range=range(2, 20))
    print("Clustering embeddings...")
    labels = cluster_embeddings(embeddings)
    clusters = get_clusters(summaries, labels)
    print("Summarizing clusters...")
    cluster_summaries = asyncio.run(summarize_from_cluster(clusters))
    print(cluster_summaries)

    # cluster_labels = cluster_embeddings(embeddings)
    # print(cluster_labels)
    # print(embeddings[:5])

if __name__ == "__main__":
    main()