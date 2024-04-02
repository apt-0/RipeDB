import requests

def get_ripe_reverse_dns(ip):
    """
    Retrieve reverse DNS information from RIPE for the given IP address.

    Args:
        ip (str): The IP address.

    Returns:
        str: The domain name associated with the IP address or an error message if not found.
    """
    url = f"https://stat.ripe.net/data/reverse-dns-ip/data.json?resource={ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', {}).get('description', 'No domain found')
    else:
        return "No domain found"
