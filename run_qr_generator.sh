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

# Check if a parameter was provided
if [ $# -eq 0 ]; then
    # No parameter, run the web server
    echo "Starting QR Code Generator web server..."
    python3 app.py
else
    # Parameter provided, generate a QR code directly
    echo "Generating QR code for: $1"
    python3 generate_qr.py "$1"
fi
