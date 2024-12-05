import argparse

from dupehunter.core import process_directory


def main():
    parser = argparse.ArgumentParser(
        description="DupeHunter: Find and handle duplicate image files"
    )
    parser.add_argument(
        "--base-path",
        required=True,
        help="Base path to traverse for files",
    )

    parser.add_argument(
        "--target-path", required=True, help="Target path for 'gold' files"
    )

    args = parser.parse_args()

    process_directory(base_path=args.base_path, target_path=args.target_path)
