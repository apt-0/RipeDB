def request_confirm(prompt):
    """
    Asks the user to enter 'y' (yes) or 'n' (no) and keeps asking until a valid response is received.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        bool: True if the user answers 'y', False if they answer 'n'.
    """
    while True:
        response = input(prompt).lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Invalid response. Enter 'y' for yes or 'n' for no.")
