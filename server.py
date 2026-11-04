from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import DatabaseManager
from market_data import MarketDataEngine

app = FastAPI(title="Watermelon Market Simulator")
templates = Jinja2Templates(directory="templates")
db = DatabaseManager()

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/portfolio")
async def get_portfolio():
    holdings = db.get_portfolio()
    cash = db.get_balance()
    
    total_invested = 0.0
    total_current_val = 0.0
    processed = []
    allocation = {}

    for symbol, asset_type, qty, avg_price in holdings:
        live_price = MarketDataEngine.get_live_price(symbol, asset_type) or avg_price
        invested = qty * avg_price
        current = qty * live_price
        pnl = (live_price - avg_price) * qty
        pnl_pct = ((live_price - avg_price) / avg_price) * 100 if avg_price > 0 else 0.0

        total_invested += invested
        total_current_val += current
        allocation[asset_type] = allocation.get(asset_type, 0.0) + current

        processed.append({
            "symbol": symbol,
            "asset_type": asset_type,
            "quantity": qty,
            "avg_price": avg_price,
            "invested_val": invested,
            "live_price": live_price,
            "current_val": current,
            "pnl": pnl,
            "pnl_pct": pnl_pct
        })

    net_worth = cash + total_current_val
    total_pnl = total_current_val - total_invested
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0.0

    return {
        "cash": cash,
        "net_worth": net_worth,
        "total_invested": total_invested,
        "total_current_val": total_current_val,
        "total_pnl": total_pnl,
        "total_pnl_pct": total_pnl_pct,
        "holdings": processed,
        "allocation": allocation
    }

@app.get("/api/search")
async def search(q: str):
    return {"results": MarketDataEngine.search_ticker(q) if q else []}

@app.post("/api/buy")
async def buy(symbol: str, asset_type: str, qty: float):
    price = MarketDataEngine.get_live_price(symbol, asset_type)
    if not price:
        return {"success": False, "message": f"Could not fetch price for {symbol}."}

    cost = qty * price
    cash = db.get_balance()

    if cash < cost:
        return {"success": False, "message": f"Insufficient funds. Required: ${cost:,.2f}"}

    db.update_balance(-cost)
    db.update_position(symbol, asset_type, qty, price)
    db.log_trade(symbol, asset_type, "BUY", qty, price, cost)
    return {"success": True, "message": f"Bought {qty} {symbol} at ${price:,.2f}"}

@app.post("/api/sell")
async def sell(symbol: str, qty: float):
    pos = db.get_position(symbol)
    if not pos:
        return {"success": False, "message": f"No position in {symbol}."}

    _, asset_type, avail_qty, avg_price = pos
    if qty > avail_qty:
        return {"success": False, "message": f"Max available to sell: {avail_qty}"}

    price = MarketDataEngine.get_live_price(symbol, asset_type) or avg_price
    proceeds = qty * price

    db.update_balance(proceeds)
    db.update_position(symbol, asset_type, -qty, price)
    db.log_trade(symbol, asset_type, "SELL", qty, price, proceeds)
    return {"success": True, "message": f"Sold {qty} {symbol} at ${price:,.2f}"}