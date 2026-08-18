# security_test.py
import requests
import ssl
import socket
from urllib.parse import urlparse

def check_site_security(url):
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"\n🔍 Checking security for: {url}")
    print("="*50)
    
    # Check SSL
    try:
        parsed = urlparse(url)
        hostname = parsed.netloc
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print("✅ SSL Certificate: Valid")
                print(f"   Expires: {cert.get('notAfter', 'Unknown')}")
    except:
        print("❌ SSL Certificate: Invalid or missing")
    
    # Check Headers
    try:
        response = requests.get(url, timeout=5, verify=False)
        headers = response.headers
        
        security_headers = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy": "CSP",
            "X-Frame-Options": "X-Frame",
            "X-Content-Type-Options": "X-Content-Type"
        }
        
        print("\n📋 Security Headers:")
        for h, name in security_headers.items():
            status = "✅" if h in headers else "❌"
            print(f"   {status} {name}")
    except:
        print("❌ Failed to fetch headers")
    
    print("="*50)

if __name__ == "__main__":
    site = input("Enter website URL (e.g., example.com): ").strip()
    if site:
        check_site_security(site)
    else:
        print("❌ No URL entered!")
