import hashlib
import logging
from pathlib import Path

from PIL import ExifTags, Image


def calculate_checksum(file_path: Path) -> str:
    """Calculate the SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as error:
        logging.error(f"Error calculating checksum for {file_path}: {error}")
        return ""


def extract_metadata(file_path: Path) -> str:
    """
    Extract image metadata if available.

    Parameters:
        file_path (Path): Path to the image file.

    Returns:
        str: Extracted metadata as a JSON-like string,
        or '{}' if no metadata is available.
    """
    try:
        with Image.open(file_path) as img:
            # Use getexif() for metadata extraction
            exif_data = img.getexif()
            metadata = {
                ExifTags.TAGS.get(tag): value
                for tag, value in exif_data.items()
                if tag in ExifTags.TAGS
            }
            return str(metadata)
    except Exception as error:
        logging.warning(f"Metadata extraction failed for {file_path}: {error}")
        return "{}"
