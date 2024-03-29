def process_input_indixes(input_utente, max_indice):
    """
    Process the user input of indices or ranges of indices to remove.

    Args:
        input_utente (str): The user input.
        max_indice (int): The maximum index allowed.

    Returns:
        list: List of valid indices or ranges of indices to remove.
    """
    index_to_remove = []
    if not input_utente.replace('-', '').replace(',', '').isdigit():
        print("L'input contiene caratteri non validi.")
        return None

    parti = input_utente.split(',')
    for parte in parti:
        try:
            if '-' in parte:
                inizio, fine = map(int, parte.split('-'))
                if 0 <= inizio <= max_indice and 0 <= fine <= max_indice and inizio <= fine:
                    index_to_remove.extend(range(inizio, fine + 1))
                else:
                    print(
                        f"Index out of range: {parte}. Valid until {max_indice}.")
                    return None
            else:
                indice = int(parte)
                if 0 <= indice <= max_indice:
                    index_to_remove.append(indice)
                else:
                    print(
                        f"Index out of range: {parte}. Valid until {max_indice}.")
                    return None
        except ValueError:
            print(f"Input not valid: {parte}.")
            return None
    return index_to_remove
