

import streamlit as st
import pandas as pd
def highlight_rows(row):
    if row["Shares to Buy"] != "N/A":
        return ['background-color: #fff9c4'] * len(row)  # Yellow for averaging
    elif row["Estimated Profit"] != "N/A" and float(row["Estimated Profit"]) > 0:
        return ['background-color: #c8e6c9'] * len(row)  # Green for profit
    elif row["Estimated Profit"] != "N/A":
        return ['background-color: #ffcdd2'] * len(row)  # Red for loss
    return [''] * len(row)

def display_results_table(df):
    st.markdown("### 📊 Averaging Result Table")
    st.dataframe(df.style.apply(highlight_rows, axis=1))


def download_csv_button(df: pd.DataFrame):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Recommendations CSV",
        data=csv,
        file_name="averaging_recommendations.csv",
        mime="text/csv"
    )

