#!/usr/bin/env python3
"""
Test script to verify the AI Email Scheduler setup
"""

import sys
import os
import json
import requests
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing Python imports...")
    
    try:
        import flask
        print("PASS: Flask imported successfully")
    except ImportError as e:
        print(f"FAIL: Flask import failed: {e}")
        return False
    
    try:
        from google.oauth2.credentials import Credentials
        print("PASS: Google OAuth2 imported successfully")
    except ImportError as e:
        print(f"FAIL: Google OAuth2 import failed: {e}")
        return False
    
    try:
        from googleapiclient.discovery import build
        print("PASS: Google API Client imported successfully")
    except ImportError as e:
        print(f"FAIL: Google API Client import failed: {e}")
        return False
    
    try:
        import requests
        print("PASS: Requests imported successfully")
    except ImportError as e:
        print(f"FAIL: Requests import failed: {e}")
        return False
    
    return True

def test_credentials():
    """Test if credentials file exists"""
    print("\nTesting credentials...")
    
    if os.path.exists('credentials.json'):
        print("PASS: credentials.json found")
        try:
            with open('credentials.json', 'r') as f:
                creds = json.load(f)
            if 'installed' in creds or 'web' in creds:
                print("PASS: Valid Google credentials format")
                return True
            else:
                print("FAIL: Invalid credentials format")
                return False
        except json.JSONDecodeError:
            print("FAIL: credentials.json is not valid JSON")
            return False
    else:
        print("FAIL: credentials.json not found")
        print("   Please download your OAuth2 credentials from Google Cloud Console")
        return False

def test_app_structure():
    """Test if all required files exist"""
    print("\nTesting application structure...")
    
    required_files = [
        'app.py',
        'email_reader.py',
        'llm_agent.py',
        'calendar_updater.py',
        'memory.py',
        'requirements.txt',
        'Dockerfile.backend',
        'docker-compose.yml',
        'frontend/src/App.js',
        'frontend/Dockerfile'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"PASS: {file_path}")
        else:
            print(f"FAIL: {file_path}")
            all_exist = False
    
    return all_exist

def test_backend_startup():
    """Test if backend can start (without actually starting it)"""
    print("\nTesting backend startup...")
    
    try:
        # Import the app module
        sys.path.append('.')
        from app import app
        
        # Test if app can be created
        with app.test_client() as client:
            print("PASS: Flask app can be created")
            return True
    except Exception as e:
        print(f"FAIL: Backend startup failed: {e}")
        return False

def test_frontend_dependencies():
    """Test if frontend dependencies are available"""
    print("\nTesting frontend dependencies...")
    
    package_json_path = 'frontend/package.json'
    if os.path.exists(package_json_path):
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            required_deps = ['react', 'axios', '@mui/material']
            missing_deps = []
            
            for dep in required_deps:
                if dep not in package_data.get('dependencies', {}):
                    missing_deps.append(dep)
            
            if missing_deps:
                print(f"FAIL: Missing frontend dependencies: {missing_deps}")
                return False
            else:
                print("PASS: All frontend dependencies found")
                return True
        except Exception as e:
            print(f"FAIL: Error reading package.json: {e}")
            return False
    else:
        print("FAIL: frontend/package.json not found")
        return False

def main():
    """Run all tests"""
    print("AI Email Scheduler - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Imports", test_imports),
        ("Credentials", test_credentials),
        ("App Structure", test_app_structure),
        ("Backend Startup", test_backend_startup),
        ("Frontend Dependencies", test_frontend_dependencies)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"FAIL: {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nSUCCESS: All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Install Docker Desktop")
        print("2. Run: docker compose up --build")
        print("3. Open http://localhost:3000 in your browser")
    else:
        print("\nWARNING: Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Install missing Python packages: pip install -r requirements.txt")
        print("- Download credentials.json from Google Cloud Console")
        print("- Install frontend dependencies: cd frontend && npm install")

if __name__ == "__main__":
    main()
