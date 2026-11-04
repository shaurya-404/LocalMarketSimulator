# 🍉 Watermelon Real-Time Market Simulator

> **A persistent, zero-risk, multi-asset paper trading environment built for global and Indian markets.**  
> Trade Stocks, ETFs, Crypto, Forex, Commodities, Mutual Funds, and Options in real-time with automatic offline state saving, dynamic P&L updates on re-launch, and a custom localhost dashboard formatted in **Indian Rupees (₹)**.

---

## 📑 Table of Contents

- [Overview & Core Concept](#-overview--core-concept)
- [✨ Key USPs (Unique Selling Points)](#-key-usps-unique-selling-points)
  - [1. Offline State Persistence & Real-Time Sync on Restart](#1-offline-state-persistence--real-time-sync-on-restart)
  - [2. Watermelon Analytics Localhost Dashboard](#2-watermelon-analytics-localhost-dashboard)
  - [3. Real-Time Multi-Asset & Indian Market Support](#3-real-time-multi-asset--indian-market-support)
  - [4. Zero-Setup One-Click Launchers](#4-zero-setup-one-click-launchers)
- [📁 Project Architecture](#-project-architecture)
- [🚀 User Guide: How to Launch & Run](#-user-guide-how-to-launch--run)
  - [Method 1: Primary Python Run (`python run.py`)](#method-1-primary-python-run-python-runpy)
  - [Method 2: One-Click OS Launchers (Auto-Installs Python if Missing)](#method-2-one-click-os-launchers-auto-installs-python-if-missing)
  - [Method 3: Terminal CLI Direct (`main.py`)](#method-3-terminal-cli-direct-mainpy)
  - [Method 4: Web Dashboard Server Direct (`server.py`)](#method-4-web-dashboard-server-direct-serverpy)
- [🎮 Menu & Features User Guide](#-menu--features-user-guide)
- [📊 Supported Asset Classes & Ticker Formats](#-supported-asset-classes--ticker-formats)
- [🛠️ Troubleshooting & FAQ](#️-troubleshooting--faq)
- [🛡️ License](#️-license)

---

## 💡 Overview & Core Concept

The **Watermelon Market Simulator** is designed for traders, students, and financial enthusiasts who want to test market strategies without risking real capital.

Instead of relying on fake or static mock data, this simulator connects directly to live global financial feeds via `yfinance`. You start with a virtual cash balance of **₹100,000.00**, allowing you to execute realistic market orders, track performance, analyze asset allocations, and build long-term portfolio strategies.

---

## ✨ Key USPs (Unique Selling Points)

### 1. Offline State Persistence & Real-Time Sync on Restart
* **Offline Local Storage:** Every single transaction, cash balance change, and asset position is automatically stored locally in a SQLite database (`market_sim.db`). You don't need external database servers or cloud sign-ups. Closing your terminal or turning off your PC **never loses your progress**.
* **Smart Compare & Update on Re-launch:** When you close the program today and open it next week, the simulator reads your saved physical holdings (`market_sim.db`), polls the latest live market prices, and instantly **re-calculates your current portfolio net worth and unrealized P&L (₹ and %)** against your original entry cost.

### 2. Watermelon Analytics Localhost Dashboard
* **Modern Web Interface:** Built using FastAPI, Chart.js, and Tailwind CSS, the dashboard offers an intuitive, watermelon-themed UI available right in your browser at `http://127.0.0.1:8000`.
* **Visual Insights:** Live metric cards for Net Worth, Cash Balance, and Portfolio Value, plus dynamic asset allocation donut charts and full holding tables formatted in **Indian Rupees (₹)**.

### 3. Real-Time Multi-Asset & Indian Market Support
* Native integration with the **National Stock Exchange (NSE)** and **Bombay Stock Exchange (BSE)** using `.NS` and `.BO` suffixes.
* Full cross-asset coverage including **US Equities, ETFs, Cryptocurrencies, Forex pairs, Commodities (Gold/Crude Oil), Mutual Funds, and Options** priced using the **Black-Scholes valuation model**.
* Integrated **Company Name Ticker Search** so you can find stock tickers by searching company keywords (e.g. "Reliance", "Tata", "Tesla").

### 4. Zero-Setup One-Click Launchers
* Includes `launch_windows.bat` and `launch_mac.command` OS wrappers. If a user doesn't have Python or required packages installed, the launcher **automatically downloads Python, configures a virtual environment, installs dependencies, and boots the app** with a single double-click.

---

## 📁 Project Architecture

```text
localMarketSimulator/
├── requirements.txt      # Dependency specifications
├── database.py          # SQLite database persistence layer
├── market_data.py      # Real-time yfinance feed & Black-Scholes engine
├── server.py            # FastAPI backend server for web dashboard
├── main.py             # Main CLI menu interface
├── run.py              # Automated Python environment launcher & dependency manager
├── launch_windows.bat  # Windows one-click auto-installer & launcher
├── launch_mac.command  # macOS one-click auto-installer & launcher
├── templates/
│   └── dashboard.html   # Watermelon UI HTML/JS Web Dashboard
└── README.md           # User guide documentation