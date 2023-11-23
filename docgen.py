import subprocess
from pathlib import Path

from documenters import select_documenter


import subprocess
from pathlib import Path


def get_tracked_python_files(directory: str) -> list:
    """
    Get a list of all git tracked Python (*.py) files in the directory.

    Returns:
    list: A list of file paths.
    """
    fullpath = str(Path(directory).absolute())
    # Run Git command to list tracked .py files
    result = subprocess.check_output(
        f"cd {fullpath} && git ls-files | grep .py", shell=True
    ).decode("utf-8")
    files = result.strip().split("\n")

    # Drop __init__.py files
    files.remove("__init__.py")

    return files


def confirm_action(files: list[str]) -> bool:
    """
    Display a warning and ask the user for confirmation to proceed.

    Args:
    file_count (int): The number of files that will be modified.

    Returns:
    bool: True if the user confirms, False otherwise.
    """
    print(
        f"Warning: This action will modify {len(files)} files. This might be a destructive action. We recommend working on a clean git branch. Make sure you have backups just in case."
    )
    print(f"List of files that will be modified: {files}")
    choice = input("Do you want to proceed? ([y]/n): ").strip().lower()
    print(choice)
    return choice in ["y", ""]


def main(
    documenter_name: str = "MockDocumenter", directory: str = None, file: str = None
):
    if directory is None and file is None:
        raise ValueError("No directory or file specified.")

    if directory is not None and file is not None:
        raise ValueError("Only one of directory or file should be specified.")

    if directory is not None:
        python_files = get_tracked_python_files(directory)

    if file is not None:
        python_files = [file]

    documenter = select_documenter(name=documenter_name)

    if confirm_action(python_files):
        for file in python_files:
            print(f"Beginning documentation generation for {file=}")
            try:
                documenter.document(file)  # Happens in place.
                print("Documentation generation completed.")
            except Exception as e:
                print(f"Something went wrong generating {file=}. See traceback...\n{e}")
    else:
        print("Action aborted by the user.")
