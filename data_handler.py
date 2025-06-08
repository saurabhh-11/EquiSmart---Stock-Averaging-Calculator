

# import pandas as pd

# REQUIRED_COLUMNS = [
#     "Stock",
#     "Current Quantity",
#     "Current Average Price",
#     "Current Market Price"
# ]

# # Map your CSV columns to expected column names
# COLUMN_MAPPING = {
#     "Stock Name": "Stock",
#     "Quantity": "Current Quantity",
#     "Average buy price": "Current Average Price",
#     "Closing price": "Current Market Price"
# }

# def load_and_validate_file(uploaded_file):
#     try:
#         if uploaded_file.name.endswith(".csv"):
#             df = pd.read_csv(uploaded_file)
#         elif uploaded_file.name.endswith(".xlsx"):
#             df = pd.read_excel(uploaded_file)
#         else:
#             return None, "Unsupported file type."

#         df.rename(columns=COLUMN_MAPPING, inplace=True)

#         missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
#         if missing_cols:
#             return None, f"Missing required columns after mapping: {', '.join(missing_cols)}"

#         df.dropna(subset=REQUIRED_COLUMNS, inplace=True)

#         for col in ["Current Quantity", "Current Average Price", "Current Market Price"]:
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#         df.dropna(subset=["Current Quantity", "Current Average Price", "Current Market Price"], inplace=True)

#         return df, None

#     except Exception as e:
#         return None, f"Error reading file: {e}"


# 



import pandas as pd
from fetch_price import get_live_price

COLUMN_MAPPING = {
    "Stock Name": "Stock",
    "Quantity": "Current Quantity",
    "Average buy price": "Current Average Price",
    "Closing price": "Current Market Price"
}

REQUIRED_COLUMNS = ["Stock", "Current Quantity", "Current Average Price", "Current Market Price"]

def load_and_validate_file(uploaded_file):
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file type."

        df.rename(columns=COLUMN_MAPPING, inplace=True)

        for idx, row in df.iterrows():
            if pd.isna(row.get("Current Market Price", None)):
                live_price = get_live_price(row["Stock"])
                if live_price:
                    df.at[idx, "Current Market Price"] = live_price

        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            return None, f"Missing required columns: {', '.join(missing_cols)}"

        df.dropna(subset=REQUIRED_COLUMNS, inplace=True)

        for col in ["Current Quantity", "Current Average Price", "Current Market Price"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        return df, None

    except Exception as e:
        return None, f"Error processing file: {e}"


def validate_inputs(current_qty, current_avg_price, market_price, target_avg_price):
    if current_qty <= 0:
        return False, "Current quantity must be greater than 0."
    if current_avg_price < 0 or market_price <= 0 or target_avg_price <= 0:
        return False, "Prices must be greater than 0."
    return True, None