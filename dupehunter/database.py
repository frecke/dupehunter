import sqlite3
from pathlib import Path
from typing import Dict, List


def initialize_database(db_path: Path) -> None:
    """Initialize the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS file_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            checksum TEXT,
            metadata TEXT,
            file_size INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


def load_catalog(db_path: Path) -> List[Dict]:
    """Load the file catalog from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path, checksum, metadata, file_size FROM file_info")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "file_path": row[0],
            "checksum": row[1],
            "metadata": row[2],
            "file_size": row[3],
        }
        for row in rows
    ]
