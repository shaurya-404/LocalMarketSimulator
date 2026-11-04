#!/bin/bash
cd "$(dirname "$0")"

echo "============================================================"
echo "        🍉 WATERMELON REAL-TIME MARKET SIMULATOR"
echo "============================================================"
echo ""

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "[!] Python3 is not installed on this Mac."
    echo "[⏳] Downloading Python 3.12 Installer package..."
    
    curl -o /tmp/python_mac.pkg https://www.python.org/ftp/python/3.12.2/python-3.12.2-macos11.pkg
    
    echo "[⏳] Installing Python... (System password may be required)"
    sudo installer -pkg /tmp/python_mac.pkg -target /
    
    echo "[✔] Python installation completed!"
    echo ""
else
    echo "[✔] Python3 environment detected."
fi

# Run main python launcher
echo "[🚀] Launching Watermelon Simulator setup..."
echo ""
python3 run.py