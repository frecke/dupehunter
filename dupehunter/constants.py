import logging
from pathlib import Path

# Constants
DEFAULT_DB_PATH = Path("file_catalog.db").resolve()
DEFAULT_DELETE_CANDIDATES_FILE = Path("delete_candidates.txt").resolve()
DEFAULT_FILES_TO_COPY_FILE = Path("files_to_copy.txt").resolve()
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}
DEFAULT_LOG_LEVEL = logging.INFO
