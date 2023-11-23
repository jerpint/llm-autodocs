import subprocess

from documenters import select_documenter


def get_tracked_python_files() -> list:
    """
    Get a list of all tracked Python (*.py) files in the Git repository.

    Returns:
    list: A list of file paths.
    """
    # Run Git command to list tracked .py files
    result = subprocess.run(["git", "ls-files", "*.py"], capture_output=True, text=True)
    files = result.stdout.strip().split("\n")
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


def main():
    python_files = get_tracked_python_files()

    documenter = select_documenter(name="MockDocumenter")

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


if __name__ == "__main__":
    main()
