import sqlite3
import numpy as np


class Database:

    def __init__(self, db_path="database/iff_access.db"):
        self.db_path = db_path
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    registration_number TEXT NOT NULL UNIQUE,
                    embedding BLOB NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_user(self, name, registration_number, embedding):

        embedding_blob = embedding.astype(
            np.float32
        ).tobytes()

        with self.connect() as conn:
            conn.execute("""
                INSERT INTO users (
                    name,
                    registration_number,
                    embedding
                )
                VALUES (?, ?, ?)
            """, (
                name,
                registration_number,
                embedding_blob
            ))

    def get_users(self):

        with self.connect() as conn:
            rows = conn.execute("""
                SELECT
                    id,
                    name,
                    registration_number,
                    embedding
                FROM users
            """).fetchall()

        users = []

        for row in rows:

            embedding = np.frombuffer(
                row[3],
                dtype=np.float32
            )

            users.append({
                "id": row[0],
                "name": row[1],
                "registration_number": row[2],
                "embedding": embedding
            })

        return users