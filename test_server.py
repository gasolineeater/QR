#!/usr/bin/env python3
"""
Test case for QR code generator server
"""
import os
import unittest
import subprocess
import time
import socket

class TestServer(unittest.TestCase):
    """Test case for QR code generator server"""
    
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
    
    def test_server_starts(self):
        """Test that the server starts"""
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
            
            # Try to connect to the server
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('localhost', 8000))
                s.close()
                self.assertTrue(True, "Successfully connected to the server")
            except ConnectionRefusedError:
                self.fail("Could not connect to the server")
        finally:
            # Terminate the server
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
    
    def test_server_responds_to_curl(self):
        """Test that the server responds to curl requests"""
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
            
            # Check if the response contains the expected content
            self.assertIn("QR Code Generator", curl_process.stdout, "Response does not contain expected content")
            self.assertIn("Add a logo", curl_process.stdout, "Response does not contain logo option")
        finally:
            # Terminate the server
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()

if __name__ == "__main__":
    unittest.main()
