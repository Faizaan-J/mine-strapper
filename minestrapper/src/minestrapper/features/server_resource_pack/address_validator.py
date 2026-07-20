import ipaddress
import socket

def is_valid_ip(ip_address: str) -> bool:
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        raise ValueError(f"Invalid IP address for server resource pack: {ip_address}")
    
    return True

def get_port_integer(port: str) -> int:
    try:
        return int(port)
    except (TypeError, ValueError):
        raise ValueError(f"Port must be an integer, got {port}")

def is_valid_port(port: int) -> bool:
    if (port < 1 or port > 65535):
        raise ValueError(f"Port must be between 1 and 65535, got {port}")

    return True

def is_port_free(ip: str, port: str) -> bool:
    candidate_port = int(port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((ip, candidate_port)) != 0

def get_clean_address(ip: str, port: str) -> tuple[str, int]:
    cleaned_ip = ip
    cleaned_port = port

    if (ip == "localhost"):
        cleaned_ip = "127.0.0.1"
    if (ip in [None, ""]):
        cleaned_ip = "0.0.0.0"

    if (not is_valid_ip(cleaned_ip)):
        raise ValueError(f"Invalid IP address for server resource pack: {cleaned_ip}")
    
    port_int = get_port_integer(port)
    if (not is_valid_port(port_int)):
        raise ValueError(f"Invalid port for server resource pack: {port}")
    
    if (not is_port_free(cleaned_ip, port)):
        cleaned_port = 0

    return cleaned_ip, int(cleaned_port)