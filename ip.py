import requests
import sys
import json
import socket

def get_ip_from_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.error as err:
        print(f"Error resolving hostname: {err}")
        sys.exit(1)

def fetch_ip_info(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching IP info: {response.status_code}")
        sys.exit(1)

def print_ip_info(data):
    for key, value in data.items():
        print(f"{key}: {value}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python ip.py <IP_ADDRESS_OR_HOSTNAME>")
        sys.exit(1)

    input_value = sys.argv[1]

    try:
        # Try to fetch IP info using the input directly
        ip = socket.inet_aton(input_value)  # Check if it's a valid IP address
        ip = input_value
    except socket.error:
        # If not a valid IP, treat it as a hostname and resolve it to an IP
        ip = get_ip_from_hostname(input_value)

    # Fetch and print IP info
    ip_info = fetch_ip_info(ip)
    print_ip_info(ip_info)

if __name__ == "__main__":
    main()
