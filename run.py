import sys
import subprocess
import os

# Required packages for the simulator
REQUIRED_PACKAGES = [
    "yfinance",
    "scipy",
    "numpy",
    "tabulate",
    "requests",
    "fastapi",
    "uvicorn",
    "jinja2"
]

def check_and_install_requirements():
    """Checks if required packages are installed, and installs missing ones automatically."""
    missing_packages = []

    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"[!] Missing required packages: {', '.join(missing_packages)}")
        print("[⏳] Installing missing dependencies via pip...")
        try:
            # Install missing packages using pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            print("[✔] Dependencies successfully installed!")
        except subprocess.CalledProcessError as e:
            print(f"[❌] Failed to install dependencies automatically: {e}")
            print("Please run 'pip install -r requirements.txt' manually.")
            sys.exit(1)

def run_application():
    """Initializes the database check and starts main CLI application."""
    print("\n[🚀] Launching Watermelon Market Simulator...")
    
    # Import main app after ensuring dependencies are present
    try:
        from main import MarketSimulatorCLI
        app = MarketSimulatorCLI()
        app.run()
    except Exception as e:
        print(f"[❌] Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_and_install_requirements()
    run_application()