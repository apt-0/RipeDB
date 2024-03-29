import ipaddress


def expand_ip_range(ip_range):
    """
    Expand an IP range into a list of individual IP addresses.

    Args:
        ip_range (str): The IP range to expand.

    Returns:
        list: A list of individual IP addresses.
    """
    try:
        net = ipaddress.ip_network(ip_range, strict=False)
        return [str(ip) for ip in net.hosts()]
    except ValueError:
        return []
