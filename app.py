import os
import sys
import io
import base64
import uuid
import cgi
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import html

# Check if qrcode and PIL are available, if not, provide instructions
try:
    import qrcode
    from PIL import Image
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

# Ensure the directories exist
os.makedirs('static/qrcodes', exist_ok=True)
os.makedirs('static/logos', exist_ok=True)

class QRCodeGenerator:
    @staticmethod
    def generate_qr_code(text, filename, logo_path=None):
        if not HAS_QRCODE:
            # If qrcode is not available, create a dummy file
            with open(filename, 'w') as f:
                f.write("QR Code would be generated here if qrcode library was installed.")
            return False

        # Generate QR code with higher error correction if logo is provided
        error_correction = qrcode.constants.ERROR_CORRECT_H if logo_path else qrcode.constants.ERROR_CORRECT_M

        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        # Create an image from the QR Code
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

        # If logo is provided, add it to the center of the QR code
        if logo_path and os.path.exists(logo_path):
            try:
                # Open the logo image
                logo = Image.open(logo_path).convert('RGBA')

                # Calculate logo size (max 30% of QR code size)
                qr_width, qr_height = qr_img.size
                logo_max_size = int(min(qr_width, qr_height) * 0.3)

                # Resize logo while maintaining aspect ratio
                logo_width, logo_height = logo.size
                if logo_width > logo_max_size or logo_height > logo_max_size:
                    if logo_width > logo_height:
                        new_width = logo_max_size
                        new_height = int(logo_height * (logo_max_size / logo_width))
                    else:
                        new_height = logo_max_size
                        new_width = int(logo_width * (logo_max_size / logo_height))
                    logo = logo.resize((new_width, new_height), Image.LANCZOS)

                # Calculate position to place the logo (center)
                logo_width, logo_height = logo.size
                position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

                # Create a white background for the logo
                logo_bg = Image.new('RGBA', logo.size, (255, 255, 255, 255))
                logo_with_bg = Image.alpha_composite(logo_bg, logo)

                # Paste the logo onto the QR code
                qr_img.paste(logo_with_bg, position, logo_with_bg)
            except Exception as e:
                print(f"Error adding logo to QR code: {e}")

        # Save the image
        qr_img.save(filename)
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
            # Parse the form data
            content_type, pdict = cgi.parse_header(self.headers['Content-Type'])

            if content_type == 'multipart/form-data':
                # Handle multipart form data (with file upload)
                pdict['boundary'] = pdict['boundary'].encode('utf-8')
                content_length = int(self.headers['Content-Length'])

                # Create a temporary file to store the form data
                with tempfile.TemporaryFile() as temp_file:
                    temp_file.write(self.rfile.read(content_length))
                    temp_file.seek(0)

                    form = cgi.FieldStorage(
                        fp=temp_file,
                        headers=self.headers,
                        environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
                    )

                    # Get form fields
                    text = form.getvalue('text', '')
                    use_logo = form.getvalue('use_logo', '') == 'on'

                    # Process logo file if provided
                    logo_path = None
                    if use_logo and 'logo' in form and form['logo'].filename:
                        logo_filename = f"{uuid.uuid4()}_{form['logo'].filename}"
                        logo_path = os.path.join('static/logos', logo_filename)

                        # Save the uploaded logo
                        with open(logo_path, 'wb') as f:
                            f.write(form['logo'].file.read())
            else:
                # Handle regular form data (no file upload)
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                form_data = parse_qs(post_data)

                text = form_data.get('text', [''])[0]
                use_logo = False
                logo_path = None

            if not text:
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return

            # Generate a unique filename
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join('static/qrcodes', filename)

            # Generate QR code
            success = QRCodeGenerator.generate_qr_code(text, filepath, logo_path)

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

            # Set the logo checkbox state
            if use_logo:
                content = content.replace('id="use_logo"', 'id="use_logo" checked')

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
