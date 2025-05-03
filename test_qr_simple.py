#!/usr/bin/env python3
"""
Simple test for QR code generator with logo integration
"""
import os
import sys
import unittest
import tempfile
import shutil

class TestQRCodeSimple(unittest.TestCase):
    """Simple test cases for QR code generator"""
    
    def setUp(self):
        """Set up for each test"""
        # Create a temporary directory for test outputs
        self.test_dir = tempfile.mkdtemp()
        
        # Create a test logo
        self.test_logo_path = os.path.join(self.test_dir, "test_logo.txt")
        with open(self.test_logo_path, "w") as f:
            f.write("This is a test logo file")
    
    def tearDown(self):
        """Clean up after each test"""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_qr_code_directories_exist(self):
        """Test that the required directories exist"""
        self.assertTrue(os.path.exists("static/qrcodes"), "QR codes directory does not exist")
        self.assertTrue(os.path.exists("static/logos"), "Logos directory does not exist")
    
    def test_app_py_exists(self):
        """Test that app.py exists"""
        self.assertTrue(os.path.exists("app.py"), "app.py does not exist")
    
    def test_index_html_exists(self):
        """Test that index.html exists"""
        self.assertTrue(os.path.exists("templates/index.html"), "index.html does not exist")
    
    def test_style_css_exists(self):
        """Test that style.css exists"""
        self.assertTrue(os.path.exists("static/css/style.css"), "style.css does not exist")
    
    def test_app_py_contains_logo_code(self):
        """Test that app.py contains logo integration code"""
        with open("app.py", "r") as f:
            content = f.read()
        
        self.assertIn("logo_path", content, "app.py does not contain logo_path parameter")
        self.assertIn("static/logos", content, "app.py does not reference logos directory")
        self.assertIn("use_logo", content, "app.py does not contain use_logo parameter")
    
    def test_index_html_contains_logo_upload(self):
        """Test that index.html contains logo upload elements"""
        with open("templates/index.html", "r") as f:
            content = f.read()
        
        self.assertIn("use_logo", content, "index.html does not contain use_logo checkbox")
        self.assertIn("logo_upload_section", content, "index.html does not contain logo upload section")
        self.assertIn("toggleLogoUpload", content, "index.html does not contain toggleLogoUpload function")
    
    def test_style_css_contains_logo_styles(self):
        """Test that style.css contains logo styles"""
        with open("static/css/style.css", "r") as f:
            content = f.read()
        
        self.assertIn("logo-option", content, "style.css does not contain logo-option styles")
        self.assertIn("logo-preview", content, "style.css does not contain logo-preview styles")
        self.assertIn("logo-upload", content, "style.css does not contain logo-upload styles")

if __name__ == "__main__":
    unittest.main()
