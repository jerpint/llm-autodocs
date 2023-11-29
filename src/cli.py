import argparse
import asyncio
from src.autodocs import main as docgen_main


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
        "-d",
        "--directory",
        type=str,
        help="The directory to scan for tracked Python files.",
        default=".",
    )
    parser.add_argument(
        "-a",
        "--allowed-files",
        nargs="+",
        default=None,
        help="Specify specific python files to consider (they must be tracked by git). Will only include all files ending with the patterns specifed (e.g. base.py). Disabled if not specified.",
    )
    parser.add_argument(
        "-i",
        "--ignored-files",
        nargs="+",
        default=None,
        help="Specify specific python files to ignore (they must be tracked by git) e.g. __init__.py to ignore any init files. Disabled if not specified.",
    )
    parser.add_argument(
        "--documenter",
        required=False,
        type=str,
        help="The type of documenter to use. Currently supported models: 'gpt-3.5-turbo', 'gpt-4' and any of their variants. 'debug' also supported for debugging.",
        default="gpt-3.5-turbo",
    )
    return parser.parse_args()


def main():
    """
    Parse command line arguments, call the documentation generation function, and run the asyncio event loop.
    """
    args = parse_args()

    asyncio.run(
        docgen_main(
            documenter_name=args.documenter,
            allowed_files=args.allowed_files,
            ignored_files=args.ignored_files,
            directory=args.directory,
        )
    )


if __name__ == "__main__":
    main()
