import argparse
import asyncio
import logging
from pathlib import Path

from dupehunter.constants import DEFAULT_DB_PATH, DEFAULT_LOG_LEVEL
from dupehunter.core import main
from dupehunter.utils import configure_logging


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for DupeHunter.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="DupeHunter: Deduplicate Image Files")
    parser.add_argument(
        "--base-path",
        required=True,
        help="Directory to scan for images",
        type=Path,
    )
    parser.add_argument(
        "--target-path",
        required=True,
        help="Directory to store unique files",
        type=Path,
    )
    parser.add_argument(
        "--db-path",
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite database file (default: file_catalog.db)",
        type=Path,
    )
    parser.add_argument(
        "--log-level",
        default=DEFAULT_LOG_LEVEL,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)",
    )
    return parser.parse_args()


def cli_entry_point() -> None:
    """
    Entry point for the DupeHunter CLI.
    """
    args = parse_arguments()
    configure_logging(args.log_level)

    logging.info("Starting DupeHunter CLI")
    try:
        asyncio.run(main(args.base_path, args.target_path, args.db_path))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    cli_entry_point()
