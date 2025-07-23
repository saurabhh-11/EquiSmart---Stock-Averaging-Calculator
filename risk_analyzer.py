# import yfinance as yf
# import numpy as np
# import datetime

# def analyze_stock_risk(stock_code):
#     """
#     Fetches and analyzes stock fundamentals and risk metrics for a given NSE stock code.
#     Returns a dictionary with fundamentals, risk level, and investment suggestion.
#     """
#     try:
#         ticker = yf.Ticker(stock_code + ".NS")
#         info = ticker.info

#         # Fetch metrics
#         pe = info.get("trailingPE") or info.get("forwardPE")
#         roe = info.get("returnOnEquity")
#         if roe is not None:
#             roe = round(roe * 100, 2)

#         eps = info.get("trailingEps")
#         market_cap = info.get("marketCap")
#         sector = info.get("sector")
#         industry = info.get("industry")

#         # Improved accuracy for Debt-to-Equity and P/B from balance sheet
#         def fetch_accurate_ratios(ticker):
#             try:
#                 balance = ticker.balance_sheet
#                 if balance.empty or "Total Liab" not in balance.index or "Total Stockholder Equity" not in balance.index:
#                     return None, None

#                 total_liabilities = float(balance.loc["Total Liab"][0])
#                 equity = float(balance.loc["Total Stockholder Equity"][0])
#                 market_cap = ticker.info.get("marketCap")

#                 debt_to_equity = round(total_liabilities / equity, 2) if equity else None
#                 pb_ratio = round(market_cap / equity, 2) if market_cap and equity else None

#                 return debt_to_equity, pb_ratio

#             except Exception as e:
#                 print("Error calculating accurate ratios:", e)
#                 return None, None

#         debt, pb = fetch_accurate_ratios(ticker)

#         # Historical volatility (1-year std dev)
#         end = datetime.datetime.today()
#         start = end - datetime.timedelta(days=365)
#         hist = ticker.history(start=start, end=end)["Close"].pct_change().dropna()
#         volatility = np.std(hist) * np.sqrt(252) if len(hist) > 30 else None

#         # Fundamental scoring logic
#         score = 0
#         reasons = []

#         if pe is not None and pe < 25:
#             score += 1
#             reasons.append("✔️ P/E ratio is reasonable")
#         else:
#             reasons.append("❌ P/E ratio too high or unavailable")

#         if roe is not None and roe > 12:
#             score += 1
#             reasons.append("✔️ ROE is strong")
#         else:
#             reasons.append("❌ ROE is weak or unavailable")

#         if debt is not None and debt < 1:
#             score += 1
#             reasons.append("✔️ Low debt-to-equity")
#         else:
#             reasons.append("❌ High or unknown debt-to-equity")

#         if pb is not None and pb < 5:
#             score += 1
#             reasons.append("✔️ Price-to-book ratio is healthy")
#         else:
#             reasons.append("❌ P/B ratio is high or missing")

#         if eps is not None and eps > 0:
#             score += 1
#             reasons.append("✔️ EPS is positive")
#         else:
#             reasons.append("❌ EPS is negative or missing")

#         # Classify fundamentals
#         if score >= 4:
#             fundamentals_rating = "Good"
#         elif score >= 2:
#             fundamentals_rating = "Average"
#         else:
#             fundamentals_rating = "Poor"

#         # Risk level based on volatility
#         if volatility is None:
#             risk_level = "Unknown"
#         elif volatility < 0.25:
#             risk_level = "Low"
#         elif volatility < 0.5:
#             risk_level = "Moderate"
#         else:
#             risk_level = "High"
#             reasons.append(f"⚠️ High volatility detected: {volatility:.2f}")

#         # Enforce strict check on critical metrics
#         debt_ok = debt is not None and debt < 1
#         pb_ok = pb is not None and pb < 5

#         # Final decision: must pass overall fundamentals, risk, and core financial ratios
#         allowed = (
#             fundamentals_rating == "Good"
#             and risk_level in ["Low", "Moderate"]
#             and debt_ok
#             and pb_ok
#         )

#         if not allowed:
#             if not debt_ok:
#                 reasons.append(f"❌ Critical: Debt-to-equity too high or missing: {debt}")
#             if not pb_ok:
#                 reasons.append(f"❌ Critical: Price-to-book too high or missing: {pb}")

#         return {
#             "pe": pe,
#             "roe": roe,
#             "debt": debt,
#             "pb": pb,
#             "eps": eps,
#             "volatility": volatility,
#             "risk_level": risk_level,
#             "fundamentals_rating": fundamentals_rating,
#             "market_cap": market_cap,
#             "sector": sector,
#             "industry": industry,
#             "allowed": allowed,
#             "reasons": reasons,
#             "raw_info": info
#         }

#     except Exception as e:
#         return {
#             "pe": None, "roe": None, "debt": None, "pb": None, "eps": None, "volatility": None,
#             "risk_level": "Unknown", "fundamentals_rating": "Unknown", "allowed": False,
#             "reasons": [f"⚠️ Error fetching data: {e}"], "raw_info": {}
#         }


# import yfinance as yf
# import numpy as np
# import datetime

# def analyze_stock_risk(stock_code):
#     """
#     Fetches and analyzes stock fundamentals and risk metrics for a given NSE stock code.
#     Returns a dictionary with fundamentals, risk level, and investment suggestion.
#     """
#     try:
#         ticker = yf.Ticker(stock_code + ".NS")
#         info = ticker.info

#         # Fetch basic metrics
#         pe = info.get("trailingPE") or info.get("forwardPE")
#         roe = info.get("returnOnEquity")
#         if roe is not None:
#             roe = round(roe * 100, 2)

#         eps = info.get("trailingEps")
#         market_cap = info.get("marketCap")
#         sector = info.get("sector")
#         industry = info.get("industry")

#         # Historical volatility (1-year std dev)
#         end = datetime.datetime.today()
#         start = end - datetime.timedelta(days=365)
#         hist = ticker.history(start=start, end=end)["Close"].pct_change().dropna()
#         volatility = np.std(hist) * np.sqrt(252) if len(hist) > 30 else None

#         # Fundamental scoring logic
#         score = 0
#         reasons = []

#         if pe is not None and pe < 25:
#             score += 1
#             reasons.append("✔️ P/E ratio is reasonable")
#         else:
#             reasons.append("❌ P/E ratio too high or unavailable")

#         if roe is not None and roe > 12:
#             score += 1
#             reasons.append("✔️ ROE is strong")
#         else:
#             reasons.append("❌ ROE is weak or unavailable")

#         if eps is not None and eps > 0:
#             score += 1
#             reasons.append("✔️ EPS is positive")
#         else:
#             reasons.append("❌ EPS is negative or missing")

#         # Classify fundamentals
#         if score >= 3:
#             fundamentals_rating = "Good"
#         elif score == 2:
#             fundamentals_rating = "Average"
#         else:
#             fundamentals_rating = "Poor"

#         # Risk level based on volatility
#         if volatility is None:
#             risk_level = "Unknown"
#         elif volatility < 0.25:
#             risk_level = "Low"
#         elif volatility < 0.5:
#             risk_level = "Moderate"
#         else:
#             risk_level = "High"
#             reasons.append(f"⚠️ High volatility detected: {volatility:.2f}")

#         # Final investment suggestion
#         allowed = fundamentals_rating == "Good" and risk_level in ["Low", "Moderate"]

#         return {
#             "pe": pe,
#             "roe": roe,
#             "eps": eps,
#             "debt": None,         # Compatibility placeholder
#             "pb": None,           # Compatibility placeholder
#             "volatility": volatility,
#             "risk_level": risk_level,
#             "fundamentals_rating": fundamentals_rating,
#             "market_cap": market_cap,
#             "sector": sector,
#             "industry": industry,
#             "allowed": allowed,
#             "reasons": reasons,
#             "raw_info": info
#         }

#     except Exception as e:
#         return {
#             "pe": None, "roe": None, "eps": None,
#             "debt": None, "pb": None, "volatility": None,
#             "risk_level": "Unknown", "fundamentals_rating": "Unknown",
#             "allowed": False,
#             "reasons": [f"⚠️ Error fetching data: {e}"],
#             "raw_info": {}
#         }

import yfinance as yf
import numpy as np
import datetime

def analyze_stock_risk(stock_code):
    """
    Fetches and analyzes stock fundamentals and risk metrics for a given NSE stock code.
    Returns a dictionary with fundamentals, risk level, and investment suggestion.
    """
    try:
        ticker = yf.Ticker(stock_code + ".NS")
        info = ticker.info

        # Fetch key metrics
        pe = info.get("trailingPE") or info.get("forwardPE")
        roe = info.get("returnOnEquity")
        if roe is not None:
            roe = round(roe * 100, 2)

        eps = info.get("trailingEps")
        sector = info.get("sector")
        industry = info.get("industry")

        # Convert market cap to ₹ Crores (1 Cr = 10^7)
        market_cap_raw = info.get("marketCap")
        market_cap = f"{round(market_cap_raw / 1e7, 2)} Cr" if market_cap_raw else "N/A"

        # Historical volatility (1-year std dev)
        end = datetime.datetime.today()
        start = end - datetime.timedelta(days=365)
        hist = ticker.history(start=start, end=end)["Close"].pct_change().dropna()
        volatility = np.std(hist) * np.sqrt(252) if len(hist) > 30 else None

        # Fundamental scoring
        score = 0
        reasons = []

        if pe is not None and pe < 25:
            score += 1
            reasons.append("✔️ P/E ratio is reasonable")
        else:
            reasons.append("❌ P/E ratio too high or unavailable")

        if roe is not None and roe > 12:
            score += 1
            reasons.append("✔️ ROE is strong")
        else:
            reasons.append("❌ ROE is weak or unavailable")

        if eps is not None and eps > 0:
            score += 1
            reasons.append("✔️ EPS is positive")
        else:
            reasons.append("❌ EPS is negative or missing")

        # Classify fundamentals
        if score >= 3:
            fundamentals_rating = "Good"
        elif score == 2:
            fundamentals_rating = "Average"
        else:
            fundamentals_rating = "Poor"

        # Risk level based on volatility
        if volatility is None:
            risk_level = "Unknown"
        elif volatility < 0.25:
            risk_level = "Low"
        elif volatility < 0.5:
            risk_level = "Moderate"
        else:
            risk_level = "High"
            reasons.append(f"⚠️ High volatility detected: {volatility:.2f}")

        # Final investment suggestion
        allowed = fundamentals_rating == "Good" and risk_level in ["Low", "Moderate"]

        return {
            "pe": pe,
            "roe": roe,
            "eps": eps,
            "volatility": volatility,
            "risk_level": risk_level,
            "fundamentals_rating": fundamentals_rating,
            "market_cap": market_cap,
            "sector": sector,
            "industry": industry,
            "allowed": allowed,
            "reasons": reasons,
            "raw_info": info
        }

    except Exception as e:
        return {
            "pe": None, "roe": None, "eps": None,
            "volatility": None,
            "risk_level": "Unknown", "fundamentals_rating": "Unknown",
            "market_cap": "N/A", "sector": None, "industry": None,
            "allowed": False,
            "reasons": [f"⚠️ Error fetching data: {e}"],
            "raw_info": {}
        }
