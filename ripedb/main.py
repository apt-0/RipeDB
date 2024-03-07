import sys
import xml.etree.ElementTree as ET
import ipaddress
import socket
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

def expand_ip_range(ip_range):
    try:
            net = ipaddress.ip_network(ip_range, strict=False)
            return [str(ip) for ip in net.hosts()]
    except ValueError: 
        return []

def range_to_cidr(ip_range):
    if '-' in ip_range:
        start_ip, end_ip = ip_range.split(' - ')
    else:
        return ip_range
    
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    
    num_hosts = int(end) - int(start) + 1
    cidr = 32 - int(num_hosts).bit_length() + (num_hosts & (num_hosts - 1) != 0)
    
    return f"{start}/{cidr}"

def export_xlsx(export_path, sheet, df_name):
    df_name.to_excel(export_path, sheet_name=sheet, index=False)
    print(f'File saved in: {export_path}')
    print(" ")

def export_xlsx_newsheet(export_path, sheet, df_name):
    try:
        with pd.ExcelWriter(export_path, engine='openpyxl', mode='a') as writer:  
            df_name.to_excel(writer, sheet_name=sheet, index=False)  
        print(f'File sovrascritto: {export_path}\nNuovo foglio creato: {sheet}')
        print(" ")
    except PermissionError: 
        print('[!] Export failed: The excel file must be closed in order to be overwritten by the program. Close it and try the execution again.')
        print(" ")
        risposta = input("Do you want to try exporting the results to an Excel file again? (y/n):")
        print(" ")
        if risposta.lower() == 'y': 
            with pd.ExcelWriter(export_path, engine='openpyxl', mode='a') as writer:  
                df_name.to_excel(writer, sheet_name=sheet, index=False)  
                print(f'File sovrascritto: {export_path}\nNuovo foglio creato: {sheet}')
                print(" ")

def rimuovi_righe(dataframe, indici_da_rimuovere):
    # Rimuovi le righe
    dataframe_ridotto = dataframe.drop(indici_da_rimuovere)
    # Resetta l'indice per avere un indice continuo
    dataframe_ridotto = dataframe_ridotto.reset_index(drop=True)
    
    return dataframe_ridotto

def processa_input_indici(input_utente):
    indici_da_rimuovere = []
    # Separa i vari range o indici singoli (es. "1-3,4-5" diventa ["1-3", "4-5"])
    parti = input_utente.split(',')
    for parte in parti:
        # Gestisci un range di indici (es. "1-5")
        if '-' in parte:
            inizio, fine = parte.split('-')
            indici_da_rimuovere.extend(range(int(inizio), int(fine) + 1))
        # Gestisci un singolo indice (es. "3")
        else:
            indici_da_rimuovere.append(int(parte))
    return indici_da_rimuovere

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "No domain found"
    except socket.gaierror as e:
        return f"Error in resolving {ip}: {e}"

def get_ripe_reverse_dns(ip):
    url = f"https://stat.ripe.net/data/reverse-dns-ip/data.json?resource={ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', {}).get('description', 'No domain found')
    else:
        return "No domain found"

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

    df['CIDR'] = df['Inetnum'].apply(range_to_cidr)
    inetnum_idx = df.columns.get_loc('Inetnum') + 1

    df.insert(inetnum_idx, 'CIDR', df.pop('CIDR'))

    # Rimuozione delle righe dove tutte le colonne sono 'N/A'
    df = df[(df['Description'] != 'N/A') | (df['NetName'] != 'N/A') | (df['Inetnum'] != 'N/A')]
    df = df.sort_values(by=['NetName', 'Description', 'Inetnum']).reset_index(drop=True)
    print("Below are the results found for:"+dominio_param)
    print(" ")
    print(df.to_string(index=True))
    print(" ")
    risposta = input("Do you want to delete rows? (y/n):")
    print(" ")

    if risposta.lower() == 'y':
        while True:
            input_utente = input("Enter the index or range of indices to remove (e.g., '3' or '1-3,4-5'), or 'n' to finish:")
            print(" ")

            if input_utente.lower() == 'n':
                print("Cleanup operation completed.")
                print(" ")
                break

            indici_da_rimuovere = processa_input_indici(input_utente)
            df = rimuovi_righe(df, indici_da_rimuovere)
            print(df)
            print(" ")

    # Esporta in xlsx
    risposta = input("Vuoi esportare i risultati in un file excel? (s/n): ")
    print(" ")
    if risposta.lower() == 's':
        export_xlsx(ds_export_path, dominio_param, df)

    risposta_reverse = input("Do you want to perform the reverse DNS lookup? (y/n):")
    print(" ")

    if risposta_reverse.lower() == 'y':
        ip_colonna = 'CIDR'

        for indice, riga in df.iterrows():
            cidr = riga[ip_colonna] 
            lista_ip = expand_ip_range(cidr)  

            print("***************************")
            print("Results for "+cidr)
            dati_ip_dominio = []

            if not lista_ip:
                print(f"No IP address found for the CIDR: {cidr}")
                print(" ")
                continue
           
            domini = []
            for ip in lista_ip:
                dominio_locale = reverse_dns(ip) 
                dominio_ripe = get_ripe_reverse_dns(ip) 
            
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
                risposta = input("Vuoi esportare i risultati in un file excel? (s/n): ")
                print(" ")
                if risposta.lower() == 's':
                    cidr_sheet = cidr.replace("/","-")
                    if os.path.exists(reverseds_export_path):                    
                        export_xlsx_newsheet(reverseds_export_path, cidr_sheet, df_subnet)
                    else:
                        export_xlsx(reverseds_export_path, cidr_sheet, df_subnet)
            else:
                print("No domain found for the IP addresses in this subnet.")

        print(" ")
    else:
        print("Skipping the reverse DNS lookup.")

    #print("Termine Programma...")

if __name__ == "__main__":
    main()