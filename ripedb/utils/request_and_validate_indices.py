import ripedb.utils.process_input_indixes
def request_valid_indixes(max_indice):
    """
    Prompt the user to enter indices or ranges of indices to remove.

    Args:
        max_indice (int): The maximum index allowed.

    Returns:
        list: List of valid indices or ranges of indices to remove.
    """
    while True:
        input_utente = input(
            "Enter the index or range of indices to remove (e.g., '3' or '1-3,4-5'), or 'n' to finish:")
        if input_utente.lower() == 'n':
            return []
        indici_validati = process_input_indixes(input_utente, max_indice)
        if indici_validati is not None:
            return indici_validati
        else:
            print("Input not valid. Try again.")
