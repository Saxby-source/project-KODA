import sqlean as sqlite3
from contextlib import contextmanager
from typing import List, Dict
from google.genai import types

DB_PATH = "koda_vault.db"

@contextmanager
def db_session():
    """Context manager to ensure safe DB connections and resource cleanup."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initializes schema if not present. Idempotent operation."""
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                          (id INTEGER PRIMARY KEY, role TEXT, content TEXT, 
                           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS lessons 
                          (id INTEGER PRIMARY KEY, lesson TEXT, context TEXT)''')
        conn.commit()

def save_message(role: str, content: str):
    """Persists a single message to the episodic history."""
    with db_session() as conn:
        conn.execute("INSERT INTO history (role, content) VALUES (?, ?)", (role, content))
        conn.commit()

def get_recent_history(limit: int = 10) -> List[types.Content]:
    """Retrieves context window as official SDK Content objects."""
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM history ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        
        history = []
        for role, content in reversed(rows):
            # We wrap the text in a Part object, then into a Content object
            history.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=content)]
                )
            )
        return history