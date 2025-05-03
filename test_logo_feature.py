#!/usr/bin/env python3
"""
Simple test case for QR code generator with logo integration
"""
import os
import unittest

class TestLogoFeature(unittest.TestCase):
    """Test case for QR code generator with logo integration"""
    
    def test_app_has_logo_integration(self):
        """Test that app.py has logo integration code"""
        with open("app.py", "r") as f:
            app_content = f.read()
        
        # Check for logo-related code in app.py
        self.assertIn("logo_path", app_content, "app.py does not have logo_path parameter")
        self.assertIn("use_logo", app_content, "app.py does not have use_logo parameter")
        self.assertIn("static/logos", app_content, "app.py does not reference logos directory")
    
    def test_html_has_logo_upload(self):
        """Test that index.html has logo upload elements"""
        with open("templates/index.html", "r") as f:
            html_content = f.read()
        
        # Check for logo-related elements in index.html
        self.assertIn('id="use_logo"', html_content, "index.html does not have use_logo checkbox")
        self.assertIn('id="logo"', html_content, "index.html does not have logo file input")
        self.assertIn('toggleLogoUpload', html_content, "index.html does not have toggleLogoUpload function")
        self.assertIn('previewLogo', html_content, "index.html does not have previewLogo function")
    
    def test_css_has_logo_styles(self):
        """Test that style.css has logo styles"""
        with open("static/css/style.css", "r") as f:
            css_content = f.read()
        
        # Check for logo-related styles in style.css
        self.assertIn('logo-option', css_content, "style.css does not have logo-option styles")
        self.assertIn('logo-upload', css_content, "style.css does not have logo-upload styles")
        self.assertIn('logo-preview', css_content, "style.css does not have logo-preview styles")
    
    def test_logos_directory_exists(self):
        """Test that logos directory exists"""
        self.assertTrue(os.path.exists("static/logos"), "static/logos directory does not exist")
        self.assertTrue(os.path.isdir("static/logos"), "static/logos is not a directory")
    
    def test_readme_mentions_logo(self):
        """Test that README.md mentions logo integration"""
        with open("README.md", "r") as f:
            readme_content = f.read()
        
        # Check for logo-related information in README.md
        self.assertIn('logo', readme_content.lower(), "README.md does not mention logo")
        self.assertIn('Add custom logos', readme_content, "README.md does not mention adding custom logos")

if __name__ == "__main__":
    unittest.main()
