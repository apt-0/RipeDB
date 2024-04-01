import os

def get_export_path(prompt, default_path=None):
    """
    Prompt the user to enter an export path or use the default one.

    Args:
        prompt (str): The message to display to the user.
        default_path (str, optional): A default path to use if provided. Defaults to None.

    Returns:
        str: The export path chosen by the user, the provided default path, or the current directory.
    """
    if default_path and os.path.exists(default_path):
        return default_path
    elif default_path and not os.path.exists(default_path):
        print(f"The specified directory does not exist: {default_path}")
        return os.getcwd() 
    
    export_path = input(prompt)
    if not export_path:
        return os.getcwd() 
    elif not os.path.exists(export_path):
        print(f"The specified directory does not exist: {export_path}")
        return get_export_path(prompt) 
    return export_path
