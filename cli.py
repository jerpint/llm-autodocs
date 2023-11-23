import os
import argparse
from pathlib import Path
import sys

from docgen import main as docgen_main


def parse_args():
    """
    Parse command line arguments.

    Returns:
    Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="CLI for generating documentation in Python files."
    )
    parser.add_argument(
        "directory", type=str, help="The directory to scan for Python files."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Change to the specified directory
    try:
        os.chdir(Path(args.directory).resolve())
    except FileNotFoundError:
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)

    # Call the main function from your original script
    docgen_main()


if __name__ == "__main__":
    main()
