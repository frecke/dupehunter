import asyncio
import logging
from pathlib import Path

from dupehunter.catalog import (
    calculate_storage_savings,
    find_duplicates,
    generate_delete_candidates,
    list_files_to_copy,
)
from dupehunter.constants import (
    DEFAULT_DB_PATH,
    DEFAULT_DELETE_CANDIDATES_FILE,
    DEFAULT_FILES_TO_COPY_FILE,
)
from dupehunter.database import initialize_database, load_catalog
from dupehunter.processing import traverse_directory
from dupehunter.utils import configure_logging, human_readable_size

# Configure logging
configure_logging()


async def main(base_path: Path, target_path: Path, db_path: Path = DEFAULT_DB_PATH):
    """
    Main function to orchestrate the deduplication process.
    Args:
        base_path (Path): Directory to scan for images.
        target_path (Path): Directory to copy unique files to.
        db_path (Path): Path to the SQLite database file.
    """
    logging.info(f"Initializing database at {db_path}")
    initialize_database(db_path)

    logging.info(f"Starting directory traversal for {base_path}")
    await traverse_directory(base_path, db_path)

    logging.info("Loading catalog from database")
    catalog = load_catalog(db_path)

    logging.info("Finding duplicates")
    gold_files, duplicates = find_duplicates(catalog)

    logging.info("Generating files to copy")
    files_to_copy = list_files_to_copy(gold_files, target_path, base_path)

    logging.info("Generating delete candidates")
    delete_candidates = generate_delete_candidates(duplicates, gold_files)

    storage_savings = calculate_storage_savings(duplicates, gold_files)

    # Write results to files
    logging.info(f"Writing files to copy to {DEFAULT_FILES_TO_COPY_FILE}")
    with DEFAULT_FILES_TO_COPY_FILE.open("w") as f:
        for entry in files_to_copy:
            f.write(f"{entry['source']} -> {entry['target']}\n")

    logging.info(f"Writing delete candidates to {DEFAULT_DELETE_CANDIDATES_FILE}")
    with DEFAULT_DELETE_CANDIDATES_FILE.open("w") as f:
        f.writelines("\n".join(delete_candidates))

    logging.info(f"Potential storage savings: {human_readable_size(storage_savings)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DupeHunter: Deduplicate Image Files")
    parser.add_argument("--base-path", required=True, help="Path to scan for images")
    parser.add_argument(
        "--target-path", required=True, help="Path to store unique files"
    )
    parser.add_argument(
        "--db-path",
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite database (default: file_catalog.db)",
    )

    args = parser.parse_args()
    asyncio.run(main(Path(args.base_path), Path(args.target_path), Path(args.db_path)))
