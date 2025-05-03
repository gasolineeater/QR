import os
import sys
import io
import base64
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import html

# Check if qrcode is available, if not, provide instructions
try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

# Ensure the qrcodes directory exists
os.makedirs('static/qrcodes', exist_ok=True)

class QRCodeGenerator:
    @staticmethod
    def generate_qr_code(text, filename):
        if not HAS_QRCODE:
            # If qrcode is not available, create a dummy file
            with open(filename, 'w') as f:
                f.write("QR Code would be generated here if qrcode library was installed.")
            return False

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        # Create an image from the QR Code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image
        img.save(filename)
        return True

class QRCodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('templates/index.html', 'r') as f:
                content = f.read()

            # Replace Flask-specific template syntax with plain HTML
            content = content.replace("{{ url_for('static', filename='css/style.css') }}", "/static/css/style.css")
            content = content.replace("{{ url_for('generate') }}", "/generate")
            content = content.replace("{{ text if text else '' }}", "")

            # Remove the QR code section if it exists
            if "{% if qr_code %}" in content:
                start_idx = content.find("{% if qr_code %}")
                end_idx = content.find("{% endif %}", start_idx) + len("{% endif %}")
                content = content[:start_idx] + content[end_idx:]

            self.wfile.write(content.encode())

        elif path.startswith('/static/'):
            file_path = path[1:]  # Remove the leading slash

            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)

                if file_path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif file_path.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                else:
                    self.send_header('Content-type', 'application/octet-stream')

                self.end_headers()

                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'File not found')

        elif path.startswith('/download/'):
            filename = path.split('/')[-1]
            file_path = os.path.join('static/qrcodes', filename)

            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.end_headers()

                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'File not found')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Page not found')

    def do_POST(self):
        if self.path == '/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)

            text = form_data.get('text', [''])[0]

            if not text:
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return

            # Generate a unique filename
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join('static/qrcodes', filename)

            # Generate QR code
            success = QRCodeGenerator.generate_qr_code(text, filepath)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('templates/index.html', 'r') as f:
                content = f.read()

            # Replace Flask-specific template syntax with plain HTML
            content = content.replace("{{ url_for('static', filename='css/style.css') }}", "/static/css/style.css")
            content = content.replace("{{ url_for('generate') }}", "/generate")
            content = content.replace("{{ text if text else '' }}", html.escape(text))

            # Replace the QR code section
            if "{% if qr_code %}" in content:
                qr_section = """
                <div class="result">
                    <h2>Your QR Code:</h2>
                    <img src="/static/qrcodes/{0}" alt="QR Code">
                    <div class="download-link">
                        <a href="/download/{0}" class="download-btn">Download QR Code</a>
                    </div>
                </div>
                """.format(filename)

                if not success:
                    qr_section = """
                    <div class="result">
                        <h2>QR Code Generation Failed</h2>
                        <p>The qrcode library is not installed. Please install it with:</p>
                        <pre>pip install qrcode[pil]</pre>
                    </div>
                    """

                start_idx = content.find("{% if qr_code %}")
                end_idx = content.find("{% endif %}", start_idx) + len("{% endif %}")
                content = content[:start_idx] + qr_section + content[end_idx:]

            self.wfile.write(content.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Page not found')

def run(server_class=HTTPServer, handler_class=QRCodeHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting QR Code Generator server on port {port}...")
    print(f"Open your browser and navigate to http://localhost:{port}/")

    if not HAS_QRCODE:
        print("\nWARNING: The 'qrcode' library is not installed.")
        print("For full functionality, please install it with:")
        print("pip install qrcode[pil]")
        print("\nThe application will run in limited mode without QR code generation.")

    httpd.serve_forever()

if __name__ == '__main__':
    run()
