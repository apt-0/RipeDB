from utils import utils
import sys
import xml.etree.ElementTree as ET
import os

try:
    import requests
except ImportError:
    print('[!] Module "requests" not installed. Try: python3 -m pip install requests')
    sys.exit(-1)

try:
    import pandas as pd
except ImportError:
    print('[!] Module "pandas" not installed. Try: python3 -m pip install pandas')
    sys.exit(-1)

try:
    import openpyxl
except ImportError:
    print('[!] Module "openpyxl" not installed. Try: python3 -m pip install openpyxl')
    sys.exit(-1)


banner = """
····················································
:                                                  :
: 888 88e  ,e,                  888 88e   888 88b, :
: 888 888D  "  888 88e   ,e e,  888 888b  888 88P' :
: 888 88"  888 888 888b d88 88b 888 8888D 888 8K   :
: 888 b,   888 888 888P 888   , 888 888P  888 88b, :
: 888 88b, 888 888 88"   "YeeP" 888 88"   888 88P' :
:              888                                 :
:              888                                 :
:                                                  :
····················································
"""

def main():
    print(banner)
    base_url = 'https://apps.db.ripe.net/db-web-ui/api/rest/fulltextsearch/select'
    dominio_param = input("Enter the search parameter:")
   
    params = {
        'facet': 'true',
        'format': 'xml',
        'hl': 'true',
        'q': '('+dominio_param+')',
        'start': 0,  
        'wt': 'json'
    }

    # Lista per tenere traccia dei risultati
    results = []

    while True:
        response = requests.get(base_url, params=params)
        xml_data = response.text
        
        if not xml_data.strip(): 
            print("No data found, exiting the loop.")
            break
        
        root = ET.fromstring(xml_data)
        docs = root.findall('.//doc')
        
        if not docs:
            print("No data found, exiting the loop.")
            break
        
        for doc in docs:
            descr_element = doc.find("str[@name='description']")
            netname_element = doc.find("str[@name='netname']")
            inetnum_element = doc.find("str[@name='inetnum']")
            
            descr_text = descr_element.text if descr_element is not None else "N/A"
            netname_text = netname_element.text if netname_element is not None else "N/A"
            inetnum_text = inetnum_element.text if inetnum_element is not None else "N/A"
            
            results.append({"Inetnum": inetnum_text, "Description": descr_text, "NetName": netname_text})
        
        params['start'] += len(docs)

    df = pd.DataFrame(results)
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.max_columns', None)  
    pd.set_option('display.width', 1000)  
    pd.set_option('display.max_colwidth', None)

    df['CIDR'] = df['Inetnum'].apply(utils.range_to_cidr)
    inetnum_idx = df.columns.get_loc('Inetnum') + 1

    df.insert(inetnum_idx, 'CIDR', df.pop('CIDR'))

    # Rimuozione delle righe dove tutte le colonne sono 'N/A'
    df = df[(df['Description'] != 'N/A') | (df['NetName'] != 'N/A') | (df['Inetnum'] != 'N/A')]
    df = df.sort_values(by=['NetName', 'Description', 'Inetnum']).reset_index(drop=True)
    print("Below are the results found for:"+dominio_param)
    print(" ")
    print(df.to_string(index=True))
    print(" ")
    risposta = utils.richiedi_conferma("Do you want to delete rows? (y/n):")
    print(" ")

    if risposta:
        while True:
            max_indice = len(df) - 1
            indici_da_rimuovere = utils.richiedi_e_valida_indici(max_indice)

            if indici_da_rimuovere:
                df = utils.rimuovi_righe(df, indici_da_rimuovere)
                print(df.to_string(index=True))
            else:
                print("")
                break
    
            print(" ")

    # Esporta in xlsx
    risposta = utils.richiedi_conferma("Do you want to export the results to an xslx file? (y/n):")
    print(" ")
    if risposta:
        export_path = utils.get_export_path("Enter the export path for the xslx file (leave blank to use the current directory): ")
        ds_export_path = os.path.join(export_path, f"{dominio_param}_results.xlsx")
        reverseds_export_path = os.path.join(export_path, f"{dominio_param}_reverse_results.xlsx")
        utils.export_xlsx(ds_export_path, dominio_param, df)

    risposta_reverse = utils.richiedi_conferma("Do you want to perform the reverse DNS lookup? (y/n):")
    print(" ")

    if risposta_reverse:
        ip_colonna = 'CIDR'

        for indice, riga in df.iterrows():
            cidr = riga[ip_colonna] 
            lista_ip = utils.expand_ip_range(cidr)  

            print("***************************")
            print("Results for "+cidr)
            dati_ip_dominio = []

            if not lista_ip:
                print(f"No IP address found for the CIDR: {cidr}")
                print(" ")
                continue
           
            domini = []
            for ip in lista_ip:
                dominio_locale = utils.reverse_dns(ip) 
                dominio_ripe = utils.get_ripe_reverse_dns(ip) 
            
                if dominio_locale == dominio_ripe or dominio_ripe != "No domain found":
                    dominio = dominio_ripe
                elif dominio_locale != "No domain found":
                    dominio = dominio_locale
                else:
                    dominio = "No domain found"
                
                if dominio != "No domain found":
                    dati_ip_dominio.append({'IP': ip, 'Domain': dominio})

            df_subnet = pd.DataFrame(dati_ip_dominio)
            if not df_subnet.empty:
                print(df_subnet)
                risposta = utils.richiedi_conferma("Do you want to export the results to an xslx file? (y/n):")
                print(" ")
                if risposta:
                    cidr_sheet = cidr.replace("/","-")
                    if os.path.exists(reverseds_export_path):                    
                        utils.export_xlsx_newsheet(reverseds_export_path, cidr_sheet, df_subnet)
                    else:
                        export_path = utils.get_export_path("Enter the export path for the xslx file (leave blank to use the current directory): ")
                        reverseds_export_path = os.path.join(export_path, f"{dominio_param}_reverse_results.xlsx")
                        utils.export_xlsx(reverseds_export_path, cidr_sheet, df_subnet)
            else:
                print("No domain found for the IP addresses in this subnet.")

        print(" ")
    else:
        print("Skipping the reverse DNS lookup.")

    #print("Termine Programma...")

if __name__ == "__main__":
    main()