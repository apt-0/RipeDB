from utils import utility, helper
import sys
import xml.etree.ElementTree as ET
import os
import argparse
import pandas as pd
import requests

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)

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
    parser = argparse.ArgumentParser(
        description='RipeDB: A tool for performing queries and analysis on RipeDB.')
    parser.add_argument('command', nargs='?',
                        help='The command to execute (query, help).')
    parser.add_argument('-q', '--query', help='Query parameter')
    parser.add_argument('-em', '--editing-mode',
                        help='Enable DNS resolution and editing mode', action='store_true')

    args = parser.parse_args()

    if args.command == 'help':
        helper.show_general_help()

    base_url = 'https://apps.db.ripe.net/db-web-ui/api/rest/fulltextsearch/select'

    if args.query:
        domain_param = args.query
    else:
        domain_param = input("Enter the search parameter:")

    params = {
        'facet': 'true',
        'format': 'xml',
        'hl': 'true',
        'q': '('+domain_param+')',
        'start': 0,
        'wt': 'json'
    }

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

            results.append(
                {"Inetnum": inetnum_text, "Description": descr_text, "NetName": netname_text})

        params['start'] += len(docs)

    df = pd.DataFrame(results)

    df['CIDR'] = df['Inetnum'].apply(utility.range_to_cidr)
    inetnum_idx = df.columns.get_loc('Inetnum') + 1

    df.insert(inetnum_idx, 'CIDR', df.pop('CIDR'))

    # Rimuozione delle righe dove tutte le colonne sono 'N/A'
    df = df[(df['Description'] != 'N/A') |
            (df['NetName'] != 'N/A') | (df['Inetnum'] != 'N/A')]
    df = df.sort_values(by=['NetName', 'Description',
                        'Inetnum']).reset_index(drop=True)
    print("Below are the results found for:"+domain_param)
    print(" ")
    print(df.to_string(index=True))
    print(" ")

    if args.editing_mode:
        reply = utility.request_confirm("Do you want to delete rows? (y/n):")
        print(" ")

        if reply:
            while True:
                max_indice = len(df) - 1
                index_to_remove = utility.request_valid_indixes(max_indice)

                if index_to_remove:
                    df = utility.remove_lines(df, index_to_remove)
                    print(df.to_string(index=True))
                else:
                    print("")
                    break

                print(" ")

        reply_reverse = utility.request_confirm(
            "Do you want to perform the reverse DNS lookup? (y/n):")
        print(" ")

        if reply_reverse:
            ip_colonna = 'CIDR'

            for indice, riga in df.iterrows():
                cidr = riga[ip_colonna]
                lista_ip = utility.expand_ip_range(cidr)

                print("***************************")
                print("Results for "+cidr)
                data_ip_domain = []

                if not lista_ip:
                    print(f"No IP address found for the CIDR: {cidr}")
                    print(" ")
                    continue

                for ip in lista_ip:
                    domain_local = utility.reverse_dns(ip)
                    domain_ripe = utility.get_ripe_reverse_dns(ip)

                    if domain_local == domain_ripe or domain_ripe != "No domain found":
                        domain = domain_ripe
                    elif domain_local != "No domain found":
                        domain = domain_local
                    else:
                        domain = "No domain found"

                    if domain != "No domain found":
                        data_ip_domain.append({'IP': ip, 'Domain': domain})

                df_subnet = pd.DataFrame(data_ip_domain)
                if not df_subnet.empty:
                    print(df_subnet)
                    reply = utility.request_confirm(
                        "Do you want to export the results to an xslx file? (y/n):")
                    print(" ")
                    if reply:
                        cidr_sheet = cidr.replace("/", "-")
                        if os.path.exists(reverseds_export_path):
                            utility.export_xlsx_newsheet(
                                reverseds_export_path, cidr_sheet, df_subnet)
                        else:
                            export_path = utility.get_export_path(
                                "Enter the export path for the xslx file (leave blank to use the current directory): ")
                            reverseds_export_path = os.path.join(
                                export_path, f"{domain_param}_reverse_results.xlsx")
                            utility.export_xlsx(
                                reverseds_export_path, cidr_sheet, df_subnet)
                else:
                    print("No domain found for the IP addresses in this subnet.")

            print(" ")
        else:
            print("Skipping the reverse DNS lookup.")

# Esporta in xlsx
    reply = utility.request_confirm(
        "Do you want to export the results to an xslx file? (y/n):")
    print(" ")
    if reply:
        export_path = utility.get_export_path(
            "Enter the export path for the xslx file (leave blank to use the current directory): ")
        ds_export_path = os.path.join(
            export_path, f"{domain_param}_results.xlsx")
        reverseds_export_path = os.path.join(
            export_path, f"{domain_param}_reverse_results.xlsx")
        utility.export_xlsx(ds_export_path, domain_param, df)   

if __name__ == "__main__":
    main()
