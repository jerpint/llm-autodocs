import asyncio
import subprocess
from pathlib import Path

from src.documenters import select_documenter


def get_tracked_python_files(directory: str) -> list:
    """Get a list of all git tracked Python (*.py) files in the directory.

    Args:
    directory: A string representing the directory path.

    Returns:
    list: A list of file paths.
    """
    fullpath = str(Path(directory).absolute())
    # Run Git command to list tracked .py files
    result = subprocess.check_output(
        f"cd {fullpath} && git ls-files | grep '\.py$'", shell=True
    ).decode("utf-8")
    files = result.strip().split("\n")

    # Drop __init__.py files
    if "__init__.py" in files:
        files.remove("__init__.py")

    return files


def confirm_action(files: list[str]) -> bool:
    """Display a warning and ask the user for confirmation to proceed.

    Args:
    files: A list of file paths.

    Returns:
    bool: True if the user confirms, False otherwise.
    """
    print(
        f"Warning: This action will modify {len(files)} files. This might be a destructive action. We recommend working on a clean git branch. Make sure you have backups just in case."
    )
    print(f"List of files that will be modified: {files}")
    choice = input("Do you want to proceed? ([y]/n): ").strip().lower()
    return choice in ["y", ""]


async def main(
    documenter_name: str = "MockDocumenter", directory: str = None, file: str = None
):
    """Asynchronously generates documentation for the specified Python files.

    Args:
    documenter_name: The name of the documenter to be used.
    directory: A string representing the directory path.
    file: A string representing a single file path.

    Raises:
    ValueError: If no directory or file is specified, or if both directory and file are specified.
    """
    if directory is None and file is None:
        raise ValueError("No directory or file specified.")

    if directory is not None and file is not None:
        raise ValueError("Only one of directory or file should be specified.")

    python_files = []
    if directory is not None:
        python_files = get_tracked_python_files(directory)

    if file is not None:
        python_files = [file]

    documenter = await select_documenter(name=documenter_name)

    if confirm_action(python_files):
        tasks = [documenter.document(file) for file in python_files]
        await asyncio.gather(*tasks)

        print("Documentation generation completed.")

    else:
        print("Action aborted by the user.")
