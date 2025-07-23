# # import streamlit as st
# # import yfinance as yf

# # # --- Live price fetch function ---
# # def get_live_price(stock_name):
# #     try:
# #         if not isinstance(stock_name, str) or not stock_name.strip():
# #             return None
# #         stock_code = stock_name.strip().upper() + ".NS"

# #         ticker = yf.Ticker(stock_code)
# #         price = ticker.info.get('regularMarketPrice')

# #         if price is None:
# #             hist = ticker.history(period="1d", interval="1m")
# #             if not hist.empty:
# #                 price = round(hist["Close"].iloc[-1], 2)

# #         return price
# #     except Exception as e:
# #         print(f"Error fetching live price for {stock_name}: {e}")
# #         return None


# import yfinance as yf

# # --- Live price fetch function ---
# def get_live_price(stock_name):
#     try:
#         if not isinstance(stock_name, str) or not stock_name.strip():
#             return None
#         stock_code = stock_name.strip().upper() + ".NS"

#         ticker = yf.Ticker(stock_code)
#         price = ticker.info.get('regularMarketPrice')

#         # Fallback: Use 1-minute intraday data
#         if price is None:
#             hist = ticker.history(period="1d", interval="1m")
#             if not hist.empty:
#                 price = round(hist["Close"].iloc[-1], 2)

#         return price
#     except Exception as e:
#         print(f"Error fetching live price for {stock_name}: {e}")
#         return None
import yfinance as yf
from nsetools import Nse

nse = Nse()

def get_live_price(stock_name):
    try:
        if not isinstance(stock_name, str) or not stock_name.strip():
            return None
        stock_code = stock_name.strip().upper()
        # Try yfinance first
        try:
            ticker = yf.Ticker(stock_code + ".NS")
            price = ticker.info.get('regularMarketPrice')
            if price is not None:
                return price
        except Exception as yf_exc:
            print(f"yfinance error for {stock_code}: {yf_exc}")
        # Fallback to nsetools
        stock_data = nse.get_quote(stock_code)
        return stock_data['lastPrice']
    except Exception as e:
        print(f"Error fetching price for {stock_name}: {e}")
        return None
