import sys
import sqlite3
from tabulate import tabulate
from database import DatabaseManager
from market_data import MarketDataEngine

class TerminalPortfolioDashboard:
    def __init__(self):
        self.db = DatabaseManager()

    def draw_bar(self, percentage, width=20):
        """Generates a visual text-based progress bar for allocation and performance."""
        filled_length = int(round(width * percentage / 100))
        bar = '█' * filled_length + '░' * (width - filled_length)
        return bar

    def render_overview(self):
        holdings = self.db.get_portfolio()
        cash = self.db.get_balance()
        
        if not holdings:
            print("\n" + "=" * 60)
            print("         PORTFOLIO ANALYTICS DASHBOARD (TERMINAL)         ")
            print("=" * 60)
            print(f" Cash Balance:            ₹{cash:,.2f}")
            print(f" Total Portfolio Value:   ₹{cash:,.2f}")
            print(" Status: Portfolio is currently empty. Buy assets to view analytics.")
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
            
            # Asset type breakdown calculation
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

        # Sort by current value descending
        processed_holdings.sort(key=lambda x: x["current_val"], reverse=True)

        # -------------------------------------------------------------
        # 1. HEADER SUMMARY CARDS
        # -------------------------------------------------------------
        print("\n" + "═" * 70)
        print("          PORTFOLIO ANALYTICS & INSIGHTS (TERMINAL)          ")
        print("═" * 70)
        print(f" Total Net Worth:         ₹{net_worth:,.2f}")
        print(f" Cash Balance:            ₹{cash:,.2f} ({ (cash/net_worth*100):.1f}% of total)")
        print(f" Invested Assets Value:   ₹{total_current_holding_val:,.2f}")
        print(f" Total Capital Invested:  ₹{total_invested:,.2f}")
        
        pnl_symbol = "▲ +" if total_pnl >= 0 else "▼ -"
        print(f" Total Unrealized P&L:    {pnl_symbol}₹{abs(total_pnl):,.2f} ({total_pnl_pct:+.2f}%)")
        print("─" * 70)

        # -------------------------------------------------------------
        # 2. ASSET ALLOCATION BREAKDOWN
        # -------------------------------------------------------------
        print("\n--- ASSET CLASS ALLOCATION ---")
        allocation_rows = []
        for a_type, val in asset_class_totals.items():
            pct = (val / total_current_holding_val * 100) if total_current_holding_val > 0 else 0
            bar = self.draw_bar(pct, width=15)
            allocation_rows.append([a_type, f"₹{val:,.2f}", f"{pct:5.1f}%", f"[{bar}]"])
            
        print(tabulate(allocation_rows, headers=["Asset Class", "Value", "Share (%)", "Distribution Visual"], tablefmt="simple"))

        # -------------------------------------------------------------
        # 3. DETAILED HOLDINGS TABLE
        # -------------------------------------------------------------
        print("\n--- HOLDINGS & REAL-TIME PERFORMANCE ---")
        holdings_rows = []
        for item in processed_holdings:
            port_weight = (item["current_val"] / net_worth * 100)
            pnl_indicator = f"+₹{item['pnl']:,.2f} ({item['pnl_pct']:+.1f}%)" if item['pnl'] >= 0 else f"-₹{abs(item['pnl']):,.2f} ({item['pnl_pct']:+.1f}%)"
            
            holdings_rows.append([
                item["symbol"],
                item["asset_type"],
                f"{item['qty']:,.4f}".rstrip('0').rstrip('.'),
                f"₹{item['avg_price']:,.2f}",
                f"₹{item['live_price']:,.2f}",
                f"₹{item['current_val']:,.2f}",
                f"{port_weight:.1f}%",
                pnl_indicator
            ])

        headers = ["Symbol", "Type", "Qty", "Avg Cost", "Live Price", "Value", "Weight", "Unrealized P&L"]
        print(tabulate(holdings_rows, headers=headers, tablefmt="grid"))

        # -------------------------------------------------------------
        # 4. TOP PERFORMER / LARGEST HOLDING HIGHLIGHTS
        # -------------------------------------------------------------
        top_gainer = max(processed_holdings, key=lambda x: x["pnl_pct"])
        worst_gainer = min(processed_holdings, key=lambda x: x["pnl_pct"])
        largest_pos = max(processed_holdings, key=lambda x: x["current_val"])

        print("\n--- KEY INSIGHTS ---")
        print(f" 🏆 Top Performing Asset:   {top_gainer['symbol']} ({top_gainer['pnl_pct']:+.2f}%)")
        print(f" ⚠️ Worst Performing Asset: {worst_gainer['symbol']} ({worst_gainer['pnl_pct']:+.2f}%)")
        print(f" 📦 Largest Asset Holding:  {largest_pos['symbol']} (₹{largest_pos['current_val']:,.2f})")
        print("═" * 70 + "\n")

    def run_menu(self):
        while True:
            print("1. Render Portfolio Dashboard")
            print("2. Export Portfolio Summary to File")
            print("3. Return to Main Menu / Exit")
            choice = input("\nSelect option (1-3): ").strip()

            if choice == "1":
                self.render_overview()
            elif choice == "2":
                self.export_summary()
            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    def export_summary(self):
        holdings = self.db.get_portfolio()
        cash = self.db.get_balance()
        filename = "portfolio_summary.txt"
        
        with open(filename, "w") as f:
            f.write(f"PORTFOLIO SUMMARY EXPORT\n")
            f.write(f"Cash Balance: ₹{cash:,.2f}\n")
            f.write("Holdings:\n")
            for symbol, asset_type, qty, avg_price in holdings:
                f.write(f"{symbol} | {asset_type} | Qty: {qty} | Avg Cost: ₹{avg_price}\n")
                
        print(f"[✔] Portfolio exported successfully to '{filename}'.")

if __name__ == "__main__":
    dashboard = TerminalPortfolioDashboard()
    dashboard.render_overview()