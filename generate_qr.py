import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

def run_server():
    """Run a simple HTTP server in the current directory."""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Starting HTTP server...")
    httpd.serve_forever()

def generate_qr_code(text):
    """Generate a QR code using our qr_generator.py script."""
    os.system(f'python3 qr_generator.py "{text}"')
    
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a moment for the server to start
    time.sleep(1)
    
    # Open the browser
    webbrowser.open('http://localhost:8000/qr_code.html')
    
    print("\nPress Ctrl+C to exit when done.")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        text = input("Enter text or URL to generate QR code: ")
    else:
        text = sys.argv[1]
    
    generate_qr_code(text)
