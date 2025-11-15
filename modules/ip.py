import urllib.request
import sys

def get_public_ip():
    """
    Fetches the public IPv4 address using a simple external service.
    Uses only Python standard library.
    """
    # Use v4.ident.me to specifically request an IPv4 address
    url = 'https://v4.ident.me'
    try:
        # Open the URL and read the response
        with urllib.request.urlopen(url) as response:
            # Decode the response from bytes to a string (utf-8)
            public_ip = response.read().decode('utf-8')
            return public_ip
    except Exception as e:
        return f"Error retrieving public IP: {e}"

if __name__ == "__main__":
    ip_address = get_public_ip()
    print(f"Public IPv4 Address: {ip_address}")
    
    # Exit cleanly
    if "Error" in ip_address:
        sys.exit(1)
    else:
        sys.exit(0)
