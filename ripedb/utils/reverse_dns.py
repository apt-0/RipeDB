import socket


def reverse_dns(ip):
    """
    Perform reverse DNS lookup for the given IP address.

    Args:
        ip (str): The IP address.

    Returns:
        str: The domain name associated with the IP address or an error message if not found.
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "No domain found"
    except socket.gaierror as e:
        return f"Error in resolving {ip}: {e}"
