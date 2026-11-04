import math
import requests
import yfinance as yf
from scipy.stats import norm

class MarketDataEngine:
    @staticmethod
    def get_live_price(symbol, asset_type="STOCK"):
        symbol = symbol.upper()
        ticker_symbol = symbol
        
        if asset_type == "CRYPTO" and not symbol.endswith("-USD"):
            ticker_symbol = f"{symbol}-USD"
        elif asset_type == "FOREX" and not symbol.endswith("=X"):
            ticker_symbol = f"{symbol}=X"
        elif asset_type == "COMMODITY" and not symbol.endswith("=F"):
            ticker_symbol = f"{symbol}=F"
            
        try:
            ticker = yf.Ticker(ticker_symbol)
            fast_info = ticker.fast_info
            price = fast_info.last_price if hasattr(fast_info, 'last_price') and fast_info.last_price else None
            
            if price is None or math.isnan(price):
                hist = ticker.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                    
            if price and not math.isnan(price):
                return round(float(price), 4)
            return None
        except Exception:
            return None

    @staticmethod
    def search_ticker(query):
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        params = {
            'q': query,
            'quotesCount': 8,
            'newsCount': 0,
            'enableFuzzyQuery': False,
            'quotesQueryId': 'tss_match_phrase_query'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                quotes = data.get('quotes', [])
                results = []
                for q in quotes:
                    symbol = q.get('symbol')
                    shortname = q.get('shortname') or q.get('longname') or 'N/A'
                    exch = q.get('exchDisp') or q.get('exchange') or 'N/A'
                    quote_type = q.get('quoteType') or 'N/A'
                    if symbol:
                        results.append({
                            'symbol': symbol,
                            'name': shortname,
                            'exchange': exch,
                            'type': quote_type
                        })
                return results
            return []
        except Exception:
            return []

    @staticmethod
    def calculate_black_scholes_option(underlying_symbol, strike_price, time_to_expiry_years, option_type="CALL", risk_free_rate=0.05, volatility=0.25):
        S = MarketDataEngine.get_live_price(underlying_symbol, "STOCK")
        if not S:
            return None
            
        K = strike_price
        T = time_to_expiry_years
        r = risk_free_rate
        sigma = volatility

        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        if option_type.upper() == "CALL":
            premium = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        else:
            premium = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return round(float(max(premium, 0.01)), 2), S