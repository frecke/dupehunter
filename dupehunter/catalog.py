from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


def find_duplicates(catalog: List[Dict]) -> Tuple[Dict, Dict]:
    """Find duplicate files based on checksum."""
    duplicates = defaultdict(list)
    for file in catalog:
        duplicates[file["checksum"]].append(file)

    gold_files = {
        checksum: files[0] for checksum, files in duplicates.items() if len(files) > 1
    }
    return gold_files, duplicates


def list_files_to_copy(
    gold_files: Dict, target_path: Path, base_path: Path
) -> List[Dict]:
    """Generate a list of files to copy with their source and target paths."""
    files_to_copy = []
    for file in gold_files.values():
        relative_path = Path(file["file_path"]).relative_to(base_path)
        target_file_path = target_path / relative_path
        files_to_copy.append(
            {"source": file["file_path"], "target": str(target_file_path)}
        )
    return files_to_copy


def generate_delete_candidates(duplicates: Dict, gold_files: Dict) -> List[str]:
    """Generate a list of files to delete."""
    candidates = []
    for checksum, files in duplicates.items():
        for file in files:
            if file != gold_files.get(checksum):
                candidates.append(file["file_path"])
    return candidates


def calculate_storage_savings(duplicates: Dict, gold_files: Dict) -> int:
    """Calculate potential storage savings."""
    return sum(
        int(file["file_size"])
        for checksum, files in duplicates.items()
        for file in files
        if file != gold_files.get(checksum)
    )
