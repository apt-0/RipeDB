import os


def get_export_path(prompt):
    """
    Prompt the user to enter an export path.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The export path chosen by the user or the current directory.
    """
    export_path = input(prompt)
    if not export_path:
        export_path = os.getcwd()
    else:
        if not os.path.exists(export_path):
            print(f"The specified directory does not exist: {export_path}")
            return get_export_path(prompt)
    return export_path
