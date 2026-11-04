import os
import sys
import subprocess
import venv

# Path definitions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, "venv")

# Python executable inside virtualenv
if sys.platform == "win32":
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
else:
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")

REQUIRED_PACKAGES = [
    "typing-extensions>=4.8.0",
    "yfinance",
    "scipy",
    "numpy",
    "tabulate",
    "requests",
    "fastapi",
    "uvicorn",
    "jinja2"
]

def setup_environment():
    """Creates virtual environment if missing and upgrades critical packages."""
    print("=" * 60)
    print("         🍉 WATERMELON REAL-TIME MARKET SIMULATOR")
    print("=" * 60)
    
    # Step 1: Create venv if not exists
    if not os.path.exists(VENV_DIR):
        print("\n[1/3] Creating isolated virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("\n[1/3] Virtual environment detected.")

    # Step 2: Auto-install & upgrade required dependencies
    print("[2/3] Checking and updating required dependencies...")
    try:
        # Upgrade pip first
        subprocess.check_call(
            [VENV_PYTHON, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Install/upgrade typing-extensions & requirements
        subprocess.check_call(
            [VENV_PYTHON, "-m", "pip", "install", "--upgrade"] + REQUIRED_PACKAGES,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[✔] Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Dependency installation warning: {e}")
        print("Attempting to run with existing environment...")

def launch_main():
    """Launches main.py using the isolated virtual environment."""
    print("\n[3/3] Starting Watermelon Market Simulator...")
    print("=" * 60 + "\n")
    
    main_script = os.path.join(BASE_DIR, "main.py")
    
    # Run main.py using virtual environment's python interpreter
    try:
        subprocess.run([VENV_PYTHON, main_script])
    except KeyboardInterrupt:
        print("\n[!] Program closed by user.")
    except Exception as e:
        print(f"\n[❌] Error running simulator: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    setup_environment()
    launch_main()