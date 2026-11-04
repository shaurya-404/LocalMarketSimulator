import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="market_sim.db", initial_cash=100000.0):
        self.db_path = db_path
        self.initial_cash = initial_cash
        self._init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Account balance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS account (
                    id INTEGER PRIMARY KEY,
                    cash_balance REAL NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            # Holdings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolio (
                    symbol TEXT PRIMARY KEY,
                    asset_type TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    avg_buy_price REAL NOT NULL
                )
            ''')
            
            # Trade execution logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    trade_type TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    price REAL NOT NULL,
                    total_amount REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Seed starting balance if new database
            cursor.execute("SELECT cash_balance FROM account WHERE id = 1")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO account (id, cash_balance, last_updated) VALUES (1, ?, ?)",
                    (self.initial_cash, datetime.now().isoformat())
                )
            conn.commit()

    def get_balance(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cash_balance FROM account WHERE id = 1")
            row = cursor.fetchone()
            return row[0] if row else self.initial_cash

    def update_balance(self, amount_change):
        current_balance = self.get_balance()
        new_balance = current_balance + amount_change
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE account SET cash_balance = ?, last_updated = ? WHERE id = 1",
                (new_balance, datetime.now().isoformat())
            )
            conn.commit()
        return new_balance

    def get_portfolio(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT symbol, asset_type, quantity, avg_buy_price FROM portfolio")
            return cursor.fetchall()

    def get_position(self, symbol):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT symbol, asset_type, quantity, avg_buy_price FROM portfolio WHERE symbol = ?", (symbol.upper(),))
            return cursor.fetchone()

    def update_position(self, symbol, asset_type, qty_change, price):
        symbol = symbol.upper()
        position = self.get_position(symbol)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if position:
                _, _, current_qty, current_avg = position
                new_qty = current_qty + qty_change
                
                if abs(new_qty) < 1e-6:
                    cursor.execute("DELETE FROM portfolio WHERE symbol = ?", (symbol,))
                elif qty_change > 0:
                    new_avg = ((current_qty * current_avg) + (qty_change * price)) / new_qty
                    cursor.execute("UPDATE portfolio SET quantity = ?, avg_buy_price = ? WHERE symbol = ?", (new_qty, new_avg, symbol))
                else:
                    cursor.execute("UPDATE portfolio SET quantity = ? WHERE symbol = ?", (new_qty, symbol))
            else:
                if qty_change > 0:
                    cursor.execute("INSERT INTO portfolio (symbol, asset_type, quantity, avg_buy_price) VALUES (?, ?, ?, ?)",
                                   (symbol, asset_type, qty_change, price))
            conn.commit()

    def log_trade(self, symbol, asset_type, trade_type, quantity, price, total_amount):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO trades (symbol, asset_type, trade_type, quantity, price, total_amount, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (symbol.upper(), asset_type, trade_type, quantity, price, total_amount, datetime.now().isoformat())
            )
            conn.commit()

    def get_trade_history(self, limit=15):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT symbol, asset_type, trade_type, quantity, price, total_amount, timestamp FROM trades ORDER BY id DESC LIMIT ?", (limit,))
            return cursor.fetchall()