import os
import psycopg2
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
from process_data import model, encode_sentences


def load_env():
    load_dotenv()


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg2.connect(database_url)


def ensure_vector_extension(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()


def get_similar_prev_correspondences(query_text, top_k, turn_index):
    load_env()
    conn = get_db_connection()
    ensure_vector_extension(conn)
    register_vector(conn)
    embedding = encode_sentences([query_text], model)[0].tolist()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT prev_context_text, new_turn_text
            FROM appointment_turns
            WHERE abs(turn_index - %s) <= 2
            ORDER BY prev_context_embedding <=> (%s::vector)
            LIMIT %s;
            """,
            (turn_index, embedding, top_k),
        )
        rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]


if __name__ == "__main__":
    text = input("Enter correspondence text: ")
    k = int(input("Enter top_k: "))
    t = int(input("Enter turn_index: "))
    results = get_similar_prev_correspondences(text, k, t)
    for r in results:
        print("----")
        print(r)