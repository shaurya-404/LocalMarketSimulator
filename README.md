# 🍉 Watermelon Real-Time Market Simulator

A lightweight, persistent, real-time paper trading market simulator built in Python. Designed for both global and domestic trading, it allows you to trade **Stocks, ETFs, Cryptocurrencies, Forex, Commodities, Mutual Funds, and Options** with zero financial risk using live market data, local database storage, and a dual terminal/web interface.

---

## 📑 Table of Contents

- [Core Principles & How It Works](#-core-principles--how-it-works)
  - [1. Persistent State Saving](#1-persistent-state-saving)
  - [2. Dynamic Live Data Refreshing](#2-dynamic-live-data-refreshing)
- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [⚙️ System Requirements](#️-system-requirements)
- [🚀 Setup & Installation Guide](#-setup--installation-guide)
  - [Step 1: Clone or Extract Files](#step-1-clone-or-extract-files)
  - [Step 2: Create a Virtual Environment](#step-2-create-a-virtual-environment)
  - [Step 3: Install Dependencies](#step-3-install-dependencies)
- [🎮 Running the Simulator](#-running-the-simulator)
  - [Method 1: One-Click Auto-Launcher (Recommended)](#method-1-one-click-auto-launcher-recommended)
  - [Method 2: Interactive Terminal CLI](#method-2-interactive-terminal-cli)
  - [Method 3: Watermelon Web Dashboard (Localhost)](#method-3-watermelon-web-dashboard-localhost)
- [📊 Supported Asset Classes & Ticker Format](#-supported-asset-classes--ticker-format)
- [🛠️ Troubleshooting & Frequently Asked Questions](#️-troubleshooting--frequently-asked-questions)
- [🛡️ License](#️-license)

---

## 💡 Core Principles & How It Works

### 1. Persistent State Saving
When you launch the simulator for the first time, an account is created with a starting balance of **$100,000.00**. 

Every trade (Buy/Sell) instantly writes changes to a local SQLite database (`market_sim.db`):
- **Cash Balances:** Automatically updated upon buying or selling.
- **Holdings Ledger:** Keeps track of physical units owned and their dollar-weighted average entry cost (`avg_buy_price`).
- **Trade History:** Logs timestamped audit records of execution price, quantity, and total trade value.

**When you close the program or shut down your PC, no data is lost.** All state remains intact inside `market_sim.db`.

### 2. Dynamic Live Data Refreshing
When you open the simulator on a future run or view your portfolio:
1. **Load Local State:** The program retrieves your saved cash balance and static holdings from `market_sim.db`.
2. **Fetch Real-Time Quotes:** The data engine queries Yahoo Finance (`yfinance`) for live market prices.
3. **Compare & Compute:** It evaluates your static cost basis against live market prices to compute **real-time Unrealized P&L ($ and %)**, **Net Portfolio Value**, and **Asset Allocation percentages**.

---

## ✨ Features

- **Multi-Asset Real-Time Streaming:** Live market data for US Equities, Indian Stock Exchanges (NSE & BSE), Crypto, Commodities, Forex, and Mutual Funds.
- **Company Name Ticker Search:** Integrated search API that translates company names (e.g., "Apple", "Tata", "Reliance") into valid market tickers.
- **Simulated Options Engine:** Black-Scholes valuation algorithm for dynamic Call/Put contract options pricing based on underlying spot prices, volatility, strike price, and time to expiration.
- **Dual Dashboard Systems:**
  - **Terminal Analytics Dashboard:** Detailed CLI tables with visual distribution progress bars, asset weights, top gainers, and worst performers.
  - **Watermelon Localhost Web Dashboard:** Single-click modern web interface powered by FastAPI + Watermelon UI (Tailwind CSS & Chart.js) running locally at `http://127.0.0.1:8000`.
- **Local SQLite Storage:** Zero setup required for databases. Saves all data locally without third-party server dependencies.

---

## 📁 Project Structure

```text
local_market_sim/
├── requirements.txt   # Third-party Python dependencies
├── database.py       # SQLite engine (tracks balance, positions, & logs)
├── market_data.py   # Real-time yfinance data streamer & Black-Scholes pricing
├── server.py         # FastAPI backend server for localhost dashboard
├── main.py          # Terminal CLI interface & interactive menu
├── run.py           # Auto-launcher and dependency installer
├── templates/
│   └── dashboard.html# Watermelon UI Web Dashboard HTML/JS
└── README.md        # Documentation