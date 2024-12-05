"""Helper functions"""

import logging
from pathlib import Path

from dupehunter.constants import SUPPORTED_EXTENSIONS


def configure_logging(level=logging.INFO):
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def is_supported_file(file_path: Path) -> bool:
    """Check if a file has a supported extension."""
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def human_readable_size(size_in_bytes: float) -> str:
    """
    Convert a file size in bytes to a human-readable string format.

    Parameters:
        size_in_bytes (float): The size in bytes.

    Returns:
        str: The size in a human-readable format (e.g., '1.23 KB', '4.56 MB').
    """
    if size_in_bytes < 0:
        raise ValueError("Size in bytes cannot be negative.")

    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"  # noqa: E231
        size_in_bytes /= 1024

    # If the size exceeds all defined units, default to the largest unit
    return f"{size_in_bytes:.2f} {units[-1]}"  # noqa: E231
