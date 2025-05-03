#!/usr/bin/env python3
"""
Create a simple test logo for QR code testing
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_logo(output_path="test_logo.png", size=(200, 200),
                    bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    """Create a simple test logo with text"""
    # Create a new image with white background
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)

    # Draw a border
    border_width = 5
    draw.rectangle(
        [(border_width, border_width),
         (size[0] - border_width, size[1] - border_width)],
        outline=text_color, width=border_width
    )

    # Add text
    try:
        # Try to use a system font
        font = ImageFont.truetype("Arial", 36)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default()

    text = "TEST"

    # Get text size - different methods depending on Pillow version
    try:
        # For newer Pillow versions
        left, top, right, bottom = font.getbbox(text)
        text_width, text_height = right - left, bottom - top
    except AttributeError:
        try:
            # For older Pillow versions
            text_width, text_height = draw.textsize(text, font=font)
        except AttributeError:
            # Fallback
            text_width, text_height = font.getsize(text) if hasattr(font, 'getsize') else (100, 30)

    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

    # Draw the text
    draw.text(position, text, fill=text_color, font=font)

    # Save the image
    img.save(output_path)
    print(f"Test logo created at: {output_path}")
    return output_path

if __name__ == "__main__":
    # Create directory for test assets if it doesn't exist
    os.makedirs("test_assets", exist_ok=True)

    # Create a test logo
    logo_path = create_test_logo("test_assets/test_logo.png")

    # Create a colored version too
    create_test_logo("test_assets/test_logo_color.png",
                    bg_color=(50, 100, 255),
                    text_color=(255, 255, 0))
