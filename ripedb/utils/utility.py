import ipaddress
import socket
import requests
import os
import openpyxl


def request_confirm(prompt):
    """
    Asks the user to enter 'y' (yes) or 'n' (no) and keeps asking until a valid response is received.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        bool: True if the user answers 'y', False if they answer 'n'.
    """
    while True:
        risposta = input(prompt).lower()
        if risposta == 'y':
            return True
        elif risposta == 'n':
            return False
        else:
            print("Invalid response. Enter 'y' for yes or 'n' for no.")


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
    cidr = 32 - int(num_hosts).bit_length() + \
        (num_hosts & (num_hosts - 1) != 0)

    return f"{start}/{cidr}"


def export_xlsx(export_path, sheet, df_name):
    df_name.to_excel(export_path, sheet_name=sheet, index=False)
    print(f'File saved in: {export_path}')
    print(" ")


def export_xlsx_newsheet(export_path, sheet, df_name):
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


def remove_lines(dataframe, indici_da_rimuovere):
    dataframe_ridotto = dataframe.drop(indici_da_rimuovere)
    dataframe_ridotto = dataframe_ridotto.reset_index(drop=True)

    return dataframe_ridotto


def request_valid_indixes(max_indice):
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


def process_input_indixes(input_utente, max_indice):
    indici_da_rimuovere = []
    if not input_utente.replace('-', '').replace(',', '').isdigit():
        print("L'input contiene caratteri non validi.")
        return None

    parti = input_utente.split(',')
    for parte in parti:
        try:
            if '-' in parte:
                inizio, fine = map(int, parte.split('-'))
                if 0 <= inizio <= max_indice and 0 <= fine <= max_indice and inizio <= fine:
                    indici_da_rimuovere.extend(range(inizio, fine + 1))
                else:
                    print(
                        f"Index out of range: {parte}. Valid until {max_indice}.")
                    return None
            else:
                indice = int(parte)
                if 0 <= indice <= max_indice:
                    indici_da_rimuovere.append(indice)
                else:
                    print(
                        f"Index out of range: {parte}. Valid until {max_indice}.")
                    return None
        except ValueError:
            print(f"Input not valid: {parte}.")
            return None
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


def get_export_path(prompt):
    """
    Asks the user to enter an export path.
    If the input is empty, uses the current directory.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The export path chosen by the user or the current directory.
    """
    export_path = input(prompt)
    if not export_path:
        export_path = os.getcwd()
    else:
        if not os.path.exists(export_path):
            print(f"The specified directory does not exist: {export_path}")
            return get_export_path(prompt)
    return export_path
