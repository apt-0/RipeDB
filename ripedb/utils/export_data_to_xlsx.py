import os
from .request_confirm import request_confirm 
from .get_export_path import get_export_path 
from .export_xlsx import export_xlsx 

def export_data_to_xlsx(df, domain_param, output_path=None):
    """
    Asks the user if they want to export the data to an xlsx file and proceeds with the export.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        domain_param (str): The domain parameter used to name the file.
        output_path (str, optional): The output path provided by the user. Defaults to None.
    """
    if not output_path:
        reply = request_confirm(
            "Do you want to export the results to an xlsx file? (y/n):")
        print(" ")
        if reply:
            export_path = get_export_path(
                "Enter the export path for the xlsx file (leave blank to use the current directory): ")
    else:
        reply = True
        export_path = get_export_path("", output_path)

    if reply:    
        ds_export_path = os.path.join(export_path, f"{domain_param}_results.xlsx")
        export_xlsx(ds_export_path, domain_param, df)
