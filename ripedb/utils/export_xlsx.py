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

def export_xlsx_newsheet(export_path, sheet, df_name):
    """
    Export DataFrame to a new sheet in an existing Excel file or create a new Excel file.

    Args:
        export_path (str): The path to the Excel file.
        sheet (str): The name of the new sheet.
        df_name (pandas.DataFrame): The DataFrame to export.
    """
    try:
        with pd.ExcelWriter(export_path, engine='openpyxl', mode='a') as writer:
            df_name.to_excel(writer, sheet_name=sheet, index=False)
        print(f'File overwritten: {export_path}\nNew sheet created: {sheet}')
        print(" ")
    except PermissionError:
        print('[!] Export failed: The xslx file must be closed in order to be overwritten by the program. Close it and try the execution again.')
        print(" ")
        risposta = input(
            "Do you want to try exporting the results to an xslx file again? (y/n):")
        print(" ")
        if risposta.lower() == 'y':
            with pd.ExcelWriter(export_path, engine='openpyxl', mode='a') as writer:
                df_name.to_xslx(writer, sheet_name=sheet, index=False)
                print(
                    f'File overwritten: {export_path}\nNew sheet created: {sheet}')
                print(" ")
