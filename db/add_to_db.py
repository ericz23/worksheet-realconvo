import os
import json
import psycopg2
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
from tqdm import tqdm
from process_data import model, process_data


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


def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS appointment_turns (
                id BIGSERIAL PRIMARY KEY,
                turn_index INTEGER NOT NULL,
                prev_context_text TEXT NOT NULL,
                prev_context_embedding vector(384) NOT NULL,
                new_turn_text TEXT NOT NULL,
                appointment_type TEXT
            );
            """
        )
    conn.commit()


def insert_rows(conn, rows, batch_size=500):
    for i in tqdm(range(0, len(rows), batch_size), desc="Inserting rows"):
        batch = rows[i:i + batch_size]
        params = [
            (
                r["turn_index"],
                r["prev_context_text"],
                r["prev_context_embedding"],
                r["new_turn_text"],
                r["appointment_type"],
            )
            for r in batch
        ]
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO appointment_turns
                    (turn_index, prev_context_text, prev_context_embedding, new_turn_text, appointment_type)
                VALUES (%s, %s, %s, %s, %s);
                """,
                params,
            )
        conn.commit()


def main():
    load_env()
    conn = get_db_connection()
    ensure_vector_extension(conn)
    register_vector(conn)
    create_table_if_not_exists(conn)

    json_file_path = "annotated\\appointment\\labeled.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = process_data(data, model, batch_size=64, max_workers=8)
    insert_rows(conn, rows)
    conn.close()


if __name__ == "__main__":
    main()