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
        "--directory",
        type=str,
        help="The directory to scan for Python files.",
        default=None,
    )
    parser.add_argument(
        "--file",
        type=str,
        help="The single python file to handle",
        default=None,
    )
    parser.add_argument(
        "--documenter",
        required=False,
        type=str,
        help="The type of documenter to use. Currently supported: ['ChatGPT', 'MockDocumenter']",
        default="ChatGPT",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(args)
    asyncio.run(
        docgen_main(
            documenter_name=args.documenter, file=args.file, directory=args.directory
        )
    )


if __name__ == "__main__":
    main()
