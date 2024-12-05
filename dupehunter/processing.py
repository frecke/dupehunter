import asyncio
import logging
import os
import sqlite3
from pathlib import Path

from dupehunter.constants import SUPPORTED_EXTENSIONS
from dupehunter.files import calculate_checksum, extract_metadata


async def process_file(file_path: Path, db_path: Path) -> None:
    """
    Process a single file: calculate checksum, extract metadata,
    and store in the database.
    """
    checksum = calculate_checksum(file_path)
    if not checksum:
        return

    metadata = extract_metadata(file_path)
    file_size = file_path.stat().st_size

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO file_info (file_path, checksum, metadata, file_size)
            VALUES (?, ?, ?, ?)
            """,
            (str(file_path), checksum, metadata, file_size),
        )
        conn.commit()
    except Exception as error:
        logging.error(f"Database insert error for {file_path}: {error}")
    finally:
        conn.close()


# Directory Traversal
async def traverse_directory(base_path: Path, db_path: Path) -> None:
    """Recursively traverse the directory and process image files."""
    tasks = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if Path(file).suffix.lower() in SUPPORTED_EXTENSIONS:
                file_path = Path(root) / file
                tasks.append(process_file(file_path.resolve(), db_path))
    await asyncio.gather(*tasks)
