import sys
import os
import base64
from urllib.parse import quote

def generate_ascii_qr(text, size=10):
    """Generate a simple ASCII QR code representation."""
    # This is a very simplified version that doesn't actually create a valid QR code
    # It's just a visual representation for demonstration purposes
    
    # Create a border
    border = "+" + "-" * (size + 2) + "+"
    
    # Create the middle part
    middle = []
    for i in range(size):
        if i == 0 or i == size - 1 or i == size // 2:
            # Add a pattern row
            row = "| " + "# " * (size // 2) + " |"
        else:
            # Add a random-looking pattern based on the input text
            pattern = ""
            for j in range(size // 2):
                char_index = (i * j + ord(text[j % len(text)])) % 2
                pattern += "# " if char_index == 0 else "  "
            row = "| " + pattern + " |"
        middle.append(row)
    
    # Combine all parts
    ascii_qr = border + "\n" + "\n".join(middle) + "\n" + border
    
    return ascii_qr

def generate_html_with_qr(text):
    """Generate HTML with a simple ASCII QR code."""
    ascii_qr = generate_ascii_qr(text)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple QR Code</title>
    <style>
        body {{
            font-family: monospace;
            text-align: center;
            margin: 50px;
        }}
        pre {{
            display: inline-block;
            text-align: left;
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 5px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .download-link {{
            margin-top: 20px;
        }}
        .download-btn {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #2ecc71;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Simple QR Code Generator</h1>
        <p>Text: {text}</p>
        <pre>{ascii_qr}</pre>
        <p>Note: This is a simplified ASCII representation, not a real QR code.</p>
        <p>To generate actual QR codes, please install the qrcode library:</p>
        <pre>pip install qrcode[pil]</pre>
        <div class="download-link">
            <a href="data:text/plain;charset=utf-8,{quote(ascii_qr)}" download="qr_code.txt" class="download-btn">Download ASCII QR</a>
        </div>
    </div>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qr_generator.py <text>")
        sys.exit(1)
    
    text = sys.argv[1]
    html = generate_html_with_qr(text)
    
    # Save the HTML file
    with open("qr_code.html", "w") as f:
        f.write(html)
    
    print(f"QR code for '{text}' generated as qr_code.html")
    print("Open the file in your browser to view it.")
