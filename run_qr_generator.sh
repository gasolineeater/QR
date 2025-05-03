#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 to use this application."
    exit 1
fi

# Check if qrcode library is installed
python3 -c "import qrcode" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: qrcode library is not installed."
    echo "For full functionality (PNG QR codes), install it with:"
    echo "pip install qrcode[pil]"
    echo ""
    echo "Continuing in fallback mode (ASCII QR codes)..."
    echo ""
fi

# Check if PIL is installed (needed for logo integration)
python3 -c "from PIL import Image" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: PIL/Pillow library is not installed."
    echo "For logo integration functionality, install it with:"
    echo "pip install Pillow"
    echo ""
    echo "Logo integration will not be available..."
    echo ""
fi

# Check if a parameter was provided
if [ $# -eq 0 ]; then
    # No parameter, run the web server
    echo "Starting QR Code Generator web server..."
    echo "Features available:"
    echo "- Generate QR codes from text or URLs"
    echo "- Add custom logos to QR codes (if PIL is installed)"
    echo "- Download QR codes as PNG files"
    echo ""
    echo "Open your browser and navigate to: http://localhost:8000/"
    python3 app.py
else
    # Parameter provided, generate a QR code directly
    echo "Generating QR code for: $1"
    echo "Note: To use logo integration, please use the web interface."
    python3 generate_qr.py "$1"
fi
