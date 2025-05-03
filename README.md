# Simple QR Code Generator

A simple Python-based QR code generator that converts text or URLs to QR codes.

## Features

- Generate QR codes from text or URLs
- Add custom logos to the center of QR codes
- View QR codes in the browser
- Download QR codes as PNG files (when qrcode library is installed)
- Download QR codes as ASCII text (fallback mode)

## Requirements

- Python 3.x

For full functionality (PNG QR codes):
- qrcode library (`pip install qrcode[pil]`)

## Usage

### Method 1: Using the Web Interface

1. Start the web server:
   ```
   python3 app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000/
   ```

3. Enter the text or URL you want to convert to a QR code
4. Optionally, check the "Add a logo" option and upload a logo image
5. Click "Generate QR Code"

### Method 2: Using the Simple Generator

1. Run the generator script with your text:
   ```
   python3 generate_qr.py "Your text or URL here"
   ```

   Or run it without arguments to be prompted for input:
   ```
   python3 generate_qr.py
   ```

2. A browser window will open automatically with your QR code

## Files

- `app.py` - Main web application using HTTP server
- `generate_qr.py` - Simple script to generate QR codes
- `qr_generator.py` - Core QR code generation functionality
- `templates/index.html` - HTML template for the web interface
- `static/css/style.css` - CSS styles for the web interface
- `static/qrcodes/` - Directory where generated QR codes are stored
- `static/logos/` - Directory where uploaded logos are stored

## Notes

- If the qrcode library is not installed, the application will fall back to generating ASCII representations of QR codes
- To install the qrcode library for full functionality:
  ```
  pip install qrcode[pil]
  ```
- When adding a logo to a QR code:
  - Use simple, high-contrast logos for best results
  - The logo will be automatically resized to fit properly (max 30% of QR code size)
  - Higher error correction is automatically used to ensure the QR code remains scannable
  - Test the QR code with different scanners to ensure compatibility
