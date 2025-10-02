#!/usr/bin/env python3
"""
Professor AI Research Assistant - Startup Script
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'flask', 'flask_cors', 'requests', 'beautifulsoup4', 
        'python-dotenv', 'google-generativeai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirement.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("\n💡 Create a .env file with your API keys:")
        print("   GOOGLE_API_KEY=your_google_api_key_here")
        print("   SERPER_API_KEY=your_serper_api_key_here")
        return False
    
    # Check if required keys exist
    env_content = env_file.read_text()
    required_keys = ['GOOGLE_API_KEY', 'SERPER_API_KEY']
    missing_keys = []
    
    for key in required_keys:
        if key not in env_content or f"{key}=" not in env_content:
            missing_keys.append(key)
    
    if missing_keys:
        print("❌ Missing required environment variables:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\n💡 Add these to your .env file")
        return False
    
    return True

def check_directory_structure():
    """Check if required directories and files exist"""
    required_files = [
        'app.py', 'templates/index.html', 'style.css', 'script.js',
        'get_links.py', 'scrape.py', 'cleaning.py', 'llm.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    return True

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Professor AI Research Assistant...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🧠 Professor AI Research Assistant")
    print("=" * 40)
    
    # Check requirements
    print("🔍 Checking requirements...")
    
    if not check_requirements():
        sys.exit(1)
    
    if not check_env_file():
        sys.exit(1)
    
    if not check_directory_structure():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print()
    
    # Ask user if they want to open browser automatically
    try:
        open_browser = input("🌐 Open browser automatically? (y/n): ").lower().strip()
        if open_browser in ['y', 'yes', '']:
            # Start server in background and open browser
            import threading
            
            def delayed_browser_open():
                time.sleep(2)  # Wait for server to start
                webbrowser.open('http://localhost:5000')
            
            browser_thread = threading.Thread(target=delayed_browser_open)
            browser_thread.daemon = True
            browser_thread.start()
    except KeyboardInterrupt:
        print("\n👋 Startup cancelled by user")
        sys.exit(0)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
