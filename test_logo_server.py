#!/usr/bin/env python3
"""
Test case for QR code generator server with logo integration
"""
import os
import unittest
import subprocess
import time
import socket
import tempfile
import shutil

class TestLogoServer(unittest.TestCase):
    """Test case for QR code generator server with logo integration"""
    
    def setUp(self):
        """Set up the test environment"""
        # Check if port 8000 is already in use
        self.port_in_use = False
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', 8000))
            s.close()
        except OSError:
            self.port_in_use = True
        
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a test logo
        self.test_logo_path = os.path.join(self.temp_dir, "test_logo.txt")
        with open(self.test_logo_path, "w") as f:
            f.write("TEST LOGO")
    
    def tearDown(self):
        """Clean up the test environment"""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_server_has_logo_option(self):
        """Test that the server has the logo option in the form"""
        if self.port_in_use:
            self.skipTest("Port 8000 is already in use")
        
        # Start the server
        server_process = subprocess.Popen(
            ["python3", "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # Wait for the server to start
            time.sleep(2)
            
            # Check if the server is running
            self.assertIsNone(server_process.poll(), "Server process terminated unexpectedly")
            
            # Send a curl request to the server
            curl_process = subprocess.run(
                ["curl", "-s", "http://localhost:8000/"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if the curl request was successful
            self.assertEqual(curl_process.returncode, 0, "Curl request failed")
            
            # Check if the response contains the logo option
            self.assertIn('id="use_logo"', curl_process.stdout, "Response does not contain logo checkbox")
            self.assertIn('id="logo"', curl_process.stdout, "Response does not contain logo file input")
            self.assertIn('toggleLogoUpload', curl_process.stdout, "Response does not contain toggleLogoUpload function")
            self.assertIn('previewLogo', curl_process.stdout, "Response does not contain previewLogo function")
        finally:
            # Terminate the server
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
    
    def test_server_form_submission(self):
        """Test submitting the form to the server"""
        if self.port_in_use:
            self.skipTest("Port 8000 is already in use")
        
        # Start the server
        server_process = subprocess.Popen(
            ["python3", "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # Wait for the server to start
            time.sleep(2)
            
            # Check if the server is running
            self.assertIsNone(server_process.poll(), "Server process terminated unexpectedly")
            
            # Send a curl request to the server with form data
            curl_process = subprocess.run(
                ["curl", "-s", "-X", "POST", "-d", "text=Test", "http://localhost:8000/generate"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if the curl request was successful
            self.assertEqual(curl_process.returncode, 0, "Curl request failed")
            
            # Check if the response contains the form with the submitted text
            self.assertIn('value="Test"', curl_process.stdout, "Response does not contain submitted text")
            
            # Check if the response contains the logo option
            self.assertIn('id="use_logo"', curl_process.stdout, "Response does not contain logo checkbox")
        finally:
            # Terminate the server
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()

if __name__ == "__main__":
    unittest.main()
