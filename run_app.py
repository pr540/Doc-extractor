import subprocess
import sys
import time
import os

def run_services():
    print("🚀 Starting Doc-Extractor Pro...")
    
    # Start Backend
    print("📡 Starting Backend on port 9000...")
    backend_process = subprocess.Popen([sys.executable, "backend/main.py"])
    
    # Wait a bit for backend to initialize
    time.sleep(2)
    
    # Start Frontend on Requested Port 9092
    print("💻 Starting Streamlit Frontend on port 9092...")
    frontend_command = [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "9092", "--browser.gatherUsageStats", "false"]
    frontend_process = subprocess.Popen(frontend_command)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    run_services()
