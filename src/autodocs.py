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

    return files


def confirm_action(files: list[str]) -> bool:
    """Display a warning and ask the user for confirmation to proceed.

    Args:
    files: A list of file paths.

    Returns:
    bool: True if the user confirms, False otherwise.
    """
    print(
        f"""** Warning ** : This action will modify the following {len(files)} file(s) in-place:

{files}

This might be a destructive action. We recommend working on a clean git branch and having a backup just in case.\n\n"""
    )
    choice = input("Do you want to proceed? ([y]/n): ").strip().lower()
    return choice in ["y", ""]


async def main(
    documenter_name: str,
    directory: str,
    allowed_files: list[str] = None,
    ignored_files: list[str] = None,
):
    """Asynchronously generates documentation for the specified Python files.

    Args:
    documenter_name: The name of the documenter to be used.
    directory: A string representing the directory path.
    allowed_files: A list of strings representing the names of allowed files.
    ingored_files: A list of strings representing the names of files to ignore.

    Raises:
    ValueError: If no directory or file is specified, or if both directory and file are specified.
    """

    # get all .py under directory tracked by git
    python_files = get_tracked_python_files(directory)

    # include allowed files only
    if allowed_files is not None:
        for allowed in allowed_files:
            python_files = [file for file in python_files if file.endswith(allowed)]

    # exclude all ignored files
    if ignored_files is not None:
        for ignore in ignored_files:
            python_files = [file for file in python_files if not file.endswith(ignore)]

    if len(python_files) == 0:
        print(f"No tracked .py files found matching the criteria. Aborting.")
        return

    # Select the documenter to use
    documenter = select_documenter(documenter_name)

    print(f"Selected documenter: {documenter_name}\n")

    if confirm_action(python_files):
        tasks = [documenter.document(file) for file in python_files]
        await asyncio.gather(*tasks)

        print("Documentation generation completed.")

    else:
        print("Action aborted by the user.")
