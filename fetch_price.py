from nsetools import Nse

nse = Nse()

def get_live_price(stock_name):
    try:
        stock_code = stock_name.strip().upper()
        stock_data = nse.get_quote(stock_code)
        return stock_data['lastPrice']
    except Exception as e:
        print(f"Error fetching price for {stock_name}: {e}")
        return None
