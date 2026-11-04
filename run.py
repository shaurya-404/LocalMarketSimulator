import sys
import subprocess
import os

REQUIRED_PACKAGES = [
    "yfinance",
    "scipy",
    "numpy",
    "tabulate"
]

def check_and_install_dependencies():
    """Checks for required packages and installs missing ones automatically."""
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"[!] Missing required dependencies: {', '.join(missing_packages)}")
        print("[*] Automatically installing missing packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            print("[✔] All dependencies installed successfully!\n")
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to install dependencies: {e}")
            print("Please run 'pip install -r requirements.txt' manually.")
            sys.exit(1)

def main():
    check_and_install_dependencies()
    
    # Import main CLI module after dependencies are validated
    try:
        from main import MarketSimulatorCLI
        app = MarketSimulatorCLI()
        app.run()
    except Exception as e:
        print(f"[!] An error occurred while launching the simulator: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()