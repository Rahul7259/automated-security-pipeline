# tests/conftest.py
# Ensures the users.db has the expected schema before tests run,
# so the /user endpoint returns a valid response instead of crashing.
import sqlite3
import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create the users table and seed a test row before the test session."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT INTO users (username) VALUES ('admin')")
    conn.commit()
    conn.close()
    yield
