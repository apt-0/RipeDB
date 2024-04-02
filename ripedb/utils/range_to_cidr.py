import ipaddress

def range_to_cidr(ip_range):
    """
    Convert an IP range to its CIDR representation.

    Args:
        ip_range (str): The IP range to convert.

    Returns:
        str: The CIDR representation of the IP range.
    """
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
