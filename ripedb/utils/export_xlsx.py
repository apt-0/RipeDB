import pandas as pd


def export_xlsx(export_path, sheet, df_name):
    """
    Export DataFrame to an Excel file.

    Args:
        export_path (str): The path to save the Excel file.
        sheet (str): The name of the Excel sheet.
        df_name (pandas.DataFrame): The DataFrame to export.
    """
    df_name.to_excel(export_path, sheet_name=sheet, index=False)
    print(f'File saved in: {export_path}')
    print(" ")
