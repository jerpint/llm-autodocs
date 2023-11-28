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
        help="The directory to scan for tracked Python files.",
        default=".",
    )
    parser.add_argument(
        "-f",
        "--files-list",
        nargs="+",
        default=None,
        help="Specify specific python files to consider (they must be tracked by git). Separate file names by a space.",
    )
    parser.add_argument(
        "--documenter",
        required=False,
        type=str,
        help="The type of documenter to use. Currently supported: ['ChatGPT', 'MockDocumenter']",
        default="gpt-3.5-turbo",
    )
    return parser.parse_args()


def main():
    """
    Parse command line arguments, call the documentation generation function, and run the asyncio event loop.
    """
    args = parse_args()

    print(args)
    asyncio.run(
        docgen_main(
            documenter_name=args.documenter,
            files=args.files_list,
            directory=args.directory,
        )
    )


if __name__ == "__main__":
    main()
