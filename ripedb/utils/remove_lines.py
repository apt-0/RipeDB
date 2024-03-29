import pandas as pd


def remove_lines(dataframe, indici_da_rimuovere):
    """
    Remove specific lines from a DataFrame based on indices.

    Args:
        dataframe (pandas.DataFrame): The DataFrame to modify.
        indici_da_rimuovere (list): List of indices to remove.

    Returns:
        pandas.DataFrame: The modified DataFrame with specified lines removed.
    """
    reducted_df = dataframe.drop(indici_da_rimuovere)
    reducted_df = reducted_df.reset_index(drop=True)

    return reducted_df
