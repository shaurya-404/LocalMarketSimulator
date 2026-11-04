import sys
import webbrowser
import uvicorn
from tabulate import tabulate
from database import DatabaseManager
from market_data import MarketDataEngine

class MarketSimulatorCLI:
    def __init__(self):
        self.db = DatabaseManager()

    def draw_bar(self, percentage, width=15):
        filled_length = int(round(width * percentage / 100))
        return '█' * filled_length + '░' * (width - filled_length)

    def run(self):
        while True:
            print("\n" + "=" * 60)
            print("       REAL-TIME MARKET SIMULATOR (LOCAL)      ")
            print("=" * 60)
            print(f"Current Cash Balance: ₹{self.db.get_balance():,.2f}")
            print("-" * 60)
            print("1. View Portfolio Dashboard & Detailed P&L 📊")
            print("2. Buy Asset")
            print("3. Sell Asset")
            print("4. Price Quote Lookup")
            print("5. Search Ticker by Company Name 🔍")
            print("6. Trade Simulated Options (Black-Scholes Pricing)")
            print("7. View Trade Log History")
            print("8. Launch Localhost Watermelon Dashboard UI 🍉")
            print("9. Exit & Save State")
            print("=" * 60)
            
            choice = input("Select an option (1-9): ").strip()
            
            if choice == "1":
                self.show_portfolio_dashboard()
            elif choice == "2":
                self.execute_buy()
            elif choice == "3":
                self.execute_sell()
            elif choice == "4":
                self.lookup_quote()
            elif choice == "5":
                self.search_company()
            elif choice == "6":
                self.trade_option()
            elif choice == "7":
                self.show_trade_log()
            elif choice == "8":
                print("\n[🚀] Launching Watermelon Web Dashboard on http://127.0.0.1:8000 ...")
                webbrowser.open("http://127.0.0.1:8000")
                uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
            elif choice == "9":
                print("\n[✔] Data successfully saved to local database ('market_sim.db'). Exiting...")
                sys.exit(0)
            else:
                print("\n[!] Invalid input. Please select from 1 to 9.")

    def show_portfolio_dashboard(self):
        holdings = self.db.get_portfolio()
        cash = self.db.get_balance()
        
        if not holdings:
            print("\n" + "=" * 60)
            print("         PORTFOLIO ANALYTICS DASHBOARD (TERMINAL)         ")
            print("=" * 60)
            print(f" Cash Balance:            ₹{cash:,.2f}")
            print(f" Total Net Worth:         ₹{cash:,.2f}")
            print(" Status: Portfolio is currently empty. Buy assets to track analytics.")
            print("=" * 60)
            return

        print("\n[⏳] Fetching latest live prices for portfolio evaluation...")
        
        total_invested = 0.0
        total_current_holding_val = 0.0
        asset_class_totals = {}
        processed_holdings = []

        for symbol, asset_type, qty, avg_price in holdings:
            live_price = MarketDataEngine.get_live_price(symbol, asset_type) or avg_price
            invested_val = qty * avg_price
            current_val = qty * live_price
            unrealized_pnl = (live_price - avg_price) * qty
            pnl_pct = ((live_price - avg_price) / avg_price) * 100 if avg_price > 0 else 0.0
            
            total_invested += invested_val
            total_current_holding_val += current_val
            asset_class_totals[asset_type] = asset_class_totals.get(asset_type, 0.0) + current_val

            processed_holdings.append({
                "symbol": symbol,
                "asset_type": asset_type,
                "qty": qty,
                "avg_price": avg_price,
                "live_price": live_price,
                "invested_val": invested_val,
                "current_val": current_val,
                "pnl": unrealized_pnl,
                "pnl_pct": pnl_pct
            })

        net_worth = cash + total_current_holding_val
        total_pnl = total_current_holding_val - total_invested
        total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0.0

        processed_holdings.sort(key=lambda x: x["current_val"], reverse=True)

        print("\n" + "═" * 70)
        print("          PORTFOLIO ANALYTICS & INSIGHTS (TERMINAL)          ")
        print("═" * 70)
        print(f" Total Net Worth:         ₹{net_worth:,.2f}")
        print(f" Cash Balance:            ₹{cash:,.2f} ({(cash/net_worth*100):.1f}% of net worth)")
        print(f" Current Holding Value:   ₹{total_current_holding_val:,.2f}")
        print(f" Total Capital Invested:  ₹{total_invested:,.2f}")
        
        pnl_symbol = "▲ +" if total_pnl >= 0 else "▼ -"
        print(f" Total Unrealized P&L:    {pnl_symbol}₹{abs(total_pnl):,.2f} ({total_pnl_pct:+.2f}%)")
        print("─" * 70)

        print("\n--- ASSET CLASS BREAKDOWN ---")
        allocation_rows = []
        for a_type, val in asset_class_totals.items():
            pct = (val / total_current_holding_val * 100) if total_current_holding_val > 0 else 0
            bar = self.draw_bar(pct)
            allocation_rows.append([a_type, f"₹{val:,.2f}", f"{pct:5.1f}%", f"[{bar}]"])
            
        print(tabulate(allocation_rows, headers=["Asset Class", "Current Value", "Share (%)", "Distribution"], tablefmt="simple"))

        print("\n--- DETAILED HOLDINGS PERFORMANCE ---")
        holdings_rows = []
        for item in processed_holdings:
            port_weight = (item["current_val"] / net_worth * 100)
            pnl_indicator = f"+₹{item['pnl']:,.2f} ({item['pnl_pct']:+.1f}%)" if item['pnl'] >= 0 else f"-₹{abs(item['pnl']):,.2f} ({item['pnl_pct']:+.1f}%)"
            
            holdings_rows.append([
                item["symbol"],
                item["asset_type"],
                f"{item['qty']:,.4f}".rstrip('0').rstrip('.'),
                f"₹{item['avg_price']:,.2f}",
                f"₹{item['invested_val']:,.2f}",
                f"₹{item['live_price']:,.2f}",
                f"₹{item['current_val']:,.2f}",
                f"{port_weight:.1f}%",
                pnl_indicator
            ])

        headers = ["Symbol", "Type", "Qty", "Avg Cost", "Invested Val", "Live Price", "Current Val", "Weight", "Unrealized P&L"]
        print(tabulate(holdings_rows, headers=headers, tablefmt="grid"))

        top_gainer = max(processed_holdings, key=lambda x: x["pnl_pct"])
        worst_gainer = min(processed_holdings, key=lambda x: x["pnl_pct"])
        largest_pos = max(processed_holdings, key=lambda x: x["current_val"])

        print("\n--- KEY HIGHLIGHTS ---")
        print(f" 🏆 Top Performing Asset:   {top_gainer['symbol']} ({top_gainer['pnl_pct']:+.2f}%)")
        print(f" ⚠️ Worst Performing Asset: {worst_gainer['symbol']} ({worst_gainer['pnl_pct']:+.2f}%)")
        print(f" 📦 Largest Asset Holding:  {largest_pos['symbol']} (₹{largest_pos['current_val']:,.2f})")
        print("═" * 70 + "\n")

    def search_company(self):
        query = input("\nEnter company name or keyword (e.g. Reliance, Tata, Apple): ").strip()
        if not query:
            return
            
        print(f"Searching for '{query}'...")
        results = MarketDataEngine.search_ticker(query)
        
        if not results:
            print(f"[!] No ticker symbols found for '{query}'.")
            return

        table_data = [[r['symbol'], r['name'], r['exchange'], r['type']] for r in results]
        headers = ["Ticker Symbol", "Company / Asset Name", "Exchange", "Type"]
        print(f"\n=== SEARCH RESULTS FOR '{query.upper()}' ===")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def execute_buy(self):
        print("\n--- BUY ASSET ---")
        symbol_input = input("Enter Ticker Symbol (or type 'S' to search by company name): ").strip().upper()
        
        if symbol_input == 'S':
            query = input("Enter company name to search: ").strip()
            results = MarketDataEngine.search_ticker(query)
            if not results:
                print("[!] No results found.")
                return
            
            table_data = [[r['symbol'], r['name'], r['exchange'], r['type']] for r in results]
            print(tabulate(table_data, headers=["Symbol", "Name", "Exchange", "Type"], tablefmt="grid"))
            symbol = input("Enter exact symbol from list above to buy: ").strip().upper()
        else:
            symbol = symbol_input

        if not symbol:
            return

        print("\nAsset Types: 1. STOCK | 2. ETF | 3. CRYPTO | 4. FOREX | 5. COMMODITY | 6. MUTUAL_FUND")
        type_map = {"1": "STOCK", "2": "ETF", "3": "CRYPTO", "4": "FOREX", "5": "COMMODITY", "6": "MUTUAL_FUND"}
        t_choice = input("Select Asset Type (1-6): ").strip()
        asset_type = type_map.get(t_choice, "STOCK")

        try:
            qty = float(input("Enter Quantity to Buy: ").strip())
            if qty <= 0:
                print("[!] Quantity must be greater than zero.")
                return
        except ValueError:
            print("[!] Invalid numerical quantity.")
            return

        print(f"Fetching real-time ask price for {symbol}...")
        price = MarketDataEngine.get_live_price(symbol, asset_type)
        
        if not price:
            print(f"[!] Could not fetch live price for '{symbol}'. Check symbol or network.")
            return

        total_cost = qty * price
        available_cash = self.db.get_balance()

        if total_cost > available_cash:
            print(f"\n[!] Trade Rejected: Insufficient Cash Balance.")
            print(f"Required: ₹{total_cost:,.2f} | Available: ₹{available_cash:,.2f}")
            return

        self.db.update_balance(-total_cost)
        self.db.update_position(symbol, asset_type, qty, price)
        self.db.log_trade(symbol, asset_type, "BUY", qty, price, total_cost)
        
        print(f"\n[✔] SUCCESS: Bought {qty} units of {symbol} at ₹{price:,.2f} per unit.")
        print(f"Total Deducted: ₹{total_cost:,.2f} | Remaining Cash: ₹{self.db.get_balance():,.2f}")

    def execute_sell(self):
        print("\n--- SELL ASSET ---")
        symbol = input("Enter Ticker Symbol to Sell: ").strip().upper()
        position = self.db.get_position(symbol)
        if not position:
            print(f"[!] You do not own any shares/units of {symbol}.")
            return

        _, asset_type, available_qty, avg_price = position
        print(f"Current Position: {available_qty} {symbol} (Avg Cost: ₹{avg_price:,.2f})")
        
        try:
            qty = float(input("Enter Quantity to Sell: ").strip())
            if qty <= 0 or qty > available_qty:
                print(f"[!] Invalid quantity. Max available to sell: {available_qty}")
                return
        except ValueError:
            print("[!] Invalid numerical quantity.")
            return

        print(f"Fetching real-time bid price for {symbol}...")
        price = MarketDataEngine.get_live_price(symbol, asset_type) or avg_price
        total_proceeds = qty * price
        
        self.db.update_balance(total_proceeds)
        self.db.update_position(symbol, asset_type, -qty, price)
        self.db.log_trade(symbol, asset_type, "SELL", qty, price, total_proceeds)

        realized_pnl = (price - avg_price) * qty
        pnl_str = f"+₹{realized_pnl:,.2f}" if realized_pnl >= 0 else f"-₹{abs(realized_pnl):,.2f}"
        print(f"\n[✔] SUCCESS: Sold {qty} units of {symbol} at ₹{price:,.2f} per unit.")
        print(f"Proceeds Added: ₹{total_proceeds:,.2f} | Realized P&L: {pnl_str}")

    def lookup_quote(self):
        symbol = input("\nEnter Ticker Symbol for Live Quote: ").strip().upper()
        price = MarketDataEngine.get_live_price(symbol)
        if price:
            print(f"\n[+] Real-time Market Quote for {symbol}: ₹{price:,.4f}")
        else:
            print(f"\n[!] Failed to retrieve quote for {symbol}.")

    def trade_option(self):
        print("\n--- SIMULATED OPTIONS TRADING (BLACK-SCHOLES MODEL) ---")
        symbol = input("Underlying Stock Ticker (e.g. NVDA, AAPL): ").strip().upper()
        spot_price = MarketDataEngine.get_live_price(symbol, "STOCK")
        if not spot_price:
            print(f"[!] Unable to retrieve current spot price for {symbol}.")
            return
            
        print(f"Current Spot Price for {symbol}: ₹{spot_price:,.2f}")
        try:
            strike = float(input("Enter Strike Price: ").strip())
            days = float(input("Enter Days to Expiration (e.g. 30): ").strip())
            opt_type = input("Option Type (CALL/PUT): ").strip().upper()
            qty = float(input("Number of Contracts (1 contract = 100 shares): ").strip())
            if opt_type not in ["CALL", "PUT"] or days <= 0 or qty <= 0:
                print("[!] Invalid option parameters.")
                return
        except ValueError:
            print("[!] Numerical input error.")
            return

        t_years = days / 365.0
        premium_per_share, spot = MarketDataEngine.calculate_black_scholes_option(
            symbol, strike, t_years, option_type=opt_type
        )
        
        contract_cost = premium_per_share * 100 * qty
        opt_symbol = f"{symbol}_{days}D_{strike}{opt_type[0]}"
        print(f"\nCalculated Option Premium: ₹{premium_per_share:.2f} / share")
        print(f"Total Option Contract Premium ({qty} contracts): ₹{contract_cost:,.2f}")
        
        confirm = input("Confirm Purchase? (y/n): ").strip().lower()
        if confirm == 'y':
            available_cash = self.db.get_balance()
            if contract_cost > available_cash:
                print("[!] Insufficient cash balance for option trade.")
                return
                
            self.db.update_balance(-contract_cost)
            self.db.update_position(opt_symbol, "OPTION", qty, premium_per_share * 100)
            self.db.log_trade(opt_symbol, "OPTION", "BUY", qty, premium_per_share * 100, contract_cost)
            print(f"\n[✔] Bought {qty} {opt_symbol} contracts for ₹{contract_cost:,.2f}")

    def show_trade_log(self):
        trades = self.db.get_trade_history()
        if not trades:
            print("\n[i] No recorded trade history yet.")
            return

        table_data = []
        for sym, a_type, t_type, qty, price, total, ts in trades:
            table_data.append([
                ts[:19].replace("T", " "), sym, a_type, t_type,
                f"{qty:,.4f}".rstrip('0').rstrip('.'), f"₹{price:,.2f}", f"₹{total:,.2f}"
            ])
            
        headers = ["Timestamp", "Symbol", "Type", "Side", "Qty", "Execution Price", "Total Amount"]
        print("\n=== RECENT TRADE HISTORY ===")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    app = MarketSimulatorCLI()
    app.run()