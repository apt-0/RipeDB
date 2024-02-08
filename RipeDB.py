import sys
import xml.etree.ElementTree as ET
import ipaddress
import socket

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
# Funzione per espandere il range di indirizzi IP
def expand_ip_range(ip_range):
    try:
            net = ipaddress.ip_network(ip_range, strict=False)
            return [str(ip) for ip in net.hosts()]
    except ValueError:  # Gestisce i valori che non sono un CIDR valido
        return []

def range_to_cidr(ip_range):
    # Gestisce un range di indirizzi IP
    if '-' in ip_range:
        start_ip, end_ip = ip_range.split(' - ')
    else:
        # Se è già un CIDR o un singolo IP, restituisci così com'è
        return ip_range
    
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    
    num_hosts = int(end) - int(start) + 1
    cidr = 32 - int(num_hosts).bit_length() + (num_hosts & (num_hosts - 1) != 0)
    
    return f"{start}/{cidr}"


def rimuovi_righe(dataframe, indici_da_rimuovere):
    # Rimuovi le righe
    dataframe_ridotto = dataframe.drop(indici_da_rimuovere)
    
    # Resetta l'indice per avere un indice continuo
    dataframe_ridotto = dataframe_ridotto.reset_index(drop=True)
    
    return dataframe_ridotto

# Funzione per processare l'input dell'utente e restituire una lista di indici
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
        return "Nessun dominio trovato"
    except socket.gaierror as e:
        return f"Errore nella risoluzione di {ip}: {e}"

def get_ripe_reverse_dns(ip):
    url = f"https://stat.ripe.net/data/reverse-dns-ip/data.json?resource={ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', {}).get('description', 'Nessun dominio trovato')
    else:
        return "Nessun dominio trovato"


print(banner)
# URL di base per la richiesta API
base_url = 'https://apps.db.ripe.net/db-web-ui/api/rest/fulltextsearch/select'
dominio_param = input("Inserisci il parametro di ricerca: ")
# Parametri iniziali
params = {
    'facet': 'true',
    'format': 'xml',
    'hl': 'true',
    'q': '('+dominio_param+')',
    'start': 0,  # Inizia dalla prima pagina
    'wt': 'json'
}

# Lista per tenere traccia dei risultati
results = []

while True:
    # Fai una richiesta GET alla URL con i parametri
    response = requests.get(base_url, params=params)
    xml_data = response.text
    
    # Assicurati che la risposta non sia vuota
    if not xml_data.strip():  # strip() rimuove spazi bianchi e newline
        print("Nessun dato trovato, uscita dal ciclo.")
        break
    
    # Analizza il XML
    root = ET.fromstring(xml_data)
    docs = root.findall('.//doc')
    
    # Controlla se ci sono elementi <doc> nella risposta
    if not docs:
        #print("Nessun dato trovato, uscita dal ciclo.")
        break
    
    # Estrai le descrizioni, le NetName e gli indirizzi IP, e aggiungi al risultato
    for doc in docs:
        descr_element = doc.find("str[@name='descr']")
        netname_element = doc.find("str[@name='netname']")
        inetnum_element = doc.find("str[@name='inetnum']")
        
        descr_text = descr_element.text if descr_element is not None else "N/A"
        netname_text = netname_element.text if netname_element is not None else "N/A"
        inetnum_text = inetnum_element.text if inetnum_element is not None else "N/A"
        
        results.append({"Inetnum": inetnum_text, "Descrizione": descr_text, "NetName": netname_text})
    
    # Aggiorna il parametro 'start' per la prossima pagina
    params['start'] += len(docs)

# Crea un DataFrame dai risultati
df = pd.DataFrame(results)
# Imposta le opzioni di visualizzazione di Pandas
pd.set_option('display.max_rows', None)  # Mostra tutte le righe
pd.set_option('display.max_columns', None)  # Mostra tutte le colonne
pd.set_option('display.width', 1000)  # Aumenta la larghezza massima delle colonne
pd.set_option('display.max_colwidth', None)  # Mostra il contenuto completo delle colonne

# Applica la funzione a ogni riga del DataFrame per la colonna 'Inetnum'
df['CIDR'] = df['Inetnum'].apply(range_to_cidr)
inetnum_idx = df.columns.get_loc('Inetnum') + 1

# Inserisci la colonna 'IPs' subito dopo 'Inetnum'
df.insert(inetnum_idx, 'CIDR', df.pop('CIDR'))

# Rimuovi le righe dove tutte le colonne sono 'N/A'
df = df[(df['Descrizione'] != 'N/A') | (df['NetName'] != 'N/A') | (df['Inetnum'] != 'N/A')]
df = df.sort_values(by=['NetName', 'Descrizione', 'Inetnum']).reset_index(drop=True)
print("Di seguito i risultati trovati per: "+dominio_param)
print(" ")
print(df.to_string(index=True))
print(" ")
risposta = input("Vuoi eliminare delle righe? (s/n): ")
print(" ")

if risposta.lower() == 's':
    # Ciclo che continua fino a quando l'utente non inserisce 'n'
    while True:
        # Richiedi all'utente di inserire l'indice o i range di indici
        input_utente = input("Inserisci l'indice o i range di indici da rimuovere (es. '3' o '1-3,4-5'), o 'n' per terminare: ")
        print(" ")
        # Controlla se l'utente vuole terminare il processo
        if input_utente.lower() == 'n':
            print("Operazione di pulizia terminata.")
            print(" ")
            break

        # Processa l'input e ottieni la lista di indici da rimuovere
        indici_da_rimuovere = processa_input_indici(input_utente)
        # Usa la funzione per rimuovere le righe e ottenere il DataFrame aggiornato
        df = rimuovi_righe(df, indici_da_rimuovere)
        print(df)
        print(" ")

risposta_reverse = input("Vuoi eseguire il reverse DNS lookup? (s/n): ")
print(" ")

if risposta_reverse.lower() == 's':
    # Seleziona una colonna dal DataFrame che contiene gli indirizzi IP espansi
    ip_colonna = 'CIDR'  # sostituisci con il nome reale della colonna se è diverso

    # Per ogni riga nel DataFrame, applica il reverse DNS lookup a ogni IP nel CIDR
    for indice, riga in df.iterrows():
        cidr = riga[ip_colonna] # Ottieni il CIDR per la riga corrente
        lista_ip = expand_ip_range(cidr)  # Espandi il CIDR in una lista di indirizzi IP

        print("***************************")
        print("Risultati per "+cidr)
        dati_ip_dominio = []

        if not lista_ip:
            print(f"Nessun indirizzo IP trovato per il CIDR: {cidr}")
            print(" ")
            continue
        # Esegui il reverse DNS lookup per ogni IP nella lista
        domini = []
        for ip in lista_ip:
            dominio_locale = reverse_dns(ip) # Esegui il reverse DNS locale
            dominio_ripe = get_ripe_reverse_dns(ip) # Esegui il reverse DNS tramite API di RIPE
        
            if dominio_locale == dominio_ripe or dominio_ripe != "Nessun dominio trovato":
                dominio = dominio_ripe
            elif dominio_locale != "Nessun dominio trovato":
                dominio = dominio_locale
            else:
                dominio = "Nessun dominio trovato"
            
            if dominio != "Nessun dominio trovato":
                dati_ip_dominio.append({'IP': ip, 'Dominio': dominio})

        df_subnet = pd.DataFrame(dati_ip_dominio)
        if not df_subnet.empty:
            print(df_subnet)
        else:
            print("Nessun dominio trovato per gli indirizzi IP in questa subnet.")

    print(" ")
else:
    print("Salto il reverse DNS lookup.")

# Continua con la fase successiva del programma
print("Procedendo alla fase successiva...")