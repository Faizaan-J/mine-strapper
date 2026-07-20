import urllib.request
import ssl

def get_public_ip():
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen("https://api.ipify.org", context=context) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"