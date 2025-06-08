import streamlit as st
import pandas as pd
from calculations import calculate_averaging
from data_handler import load_and_validate_file
from visualization import display_results_table, download_csv_button

def portfolio_upload_ui():
    # Enhanced header
    st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h2 style='color: #1f1f1f; font-size: 1.8rem; font-weight: 600;'>
                📁 Upload Portfolio CSV or Excel
            </h2>
            <p style='color: #666; font-size: 1.1rem;'>
                Process multiple stocks at once with our batch calculator
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # File upload instructions with better styling
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;'>
            <h3 style='color: #1f1f1f; margin-bottom: 1rem;'>📋 File Format Requirements</h3>
            <p style='color: #666; margin-bottom: 1rem;'>Your CSV/Excel file should have these columns:</p>
            <ul style='color: #666; list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 0.5rem;'>📌 <strong>Stock</strong>: Stock name/symbol</li>
                <li style='margin-bottom: 0.5rem;'>📌 <strong>Current Quantity</strong>: Number of shares you own</li>
                <li style='margin-bottom: 0.5rem;'>📌 <strong>Current Average Price</strong>: Your current average purchase price</li>
                <li style='margin-bottom: 0.5rem;'>📌 <strong>Current Market Price</strong>: Current market price of the stock</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # File uploader with enhanced styling
    uploaded_file = st.file_uploader(
        "Upload your portfolio file (CSV or Excel)",
        type=["csv", "xlsx"],
        help="Upload a CSV or Excel file with your portfolio data"
    )

    if not uploaded_file:
        st.markdown("""
            <div style='text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 12px;'>
                <p style='color: #666; font-size: 1.1rem;'>👆 Please upload a file to begin</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # Strategy selection with enhanced layout
    st.markdown("""
        <div style='margin: 2rem 0;'>
            <h3 style='color: #1f1f1f; text-align: center; margin-bottom: 1.5rem;'>
                📈 Select Averaging Strategy
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        strategy = st.selectbox(
            "Choose your strategy",
            [
                "Mean of current avg & market",
                "10% below current avg",
                "5% above market price"
            ],
            help="Select how you want to calculate the target average price"
        )
    
    with col2:
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 12px;'>
                <h4 style='color: #1f1f1f; margin-bottom: 1rem;'>💡 Strategy Details</h4>
                <ul style='color: #666; list-style-type: none; padding-left: 0;'>
                    <li style='margin-bottom: 0.5rem;'>📊 <strong>Mean</strong>: Balanced approach</li>
                    <li style='margin-bottom: 0.5rem;'>🔻 <strong>10% Below</strong>: Conservative</li>
                    <li style='margin-bottom: 0.5rem;'>🔺 <strong>5% Above</strong>: Aggressive</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Load and validate file
    df, error = load_and_validate_file(uploaded_file)

    if error:
        st.markdown(f"""
            <div class='error-message'>
                ❌ {error}
            </div>
        """, unsafe_allow_html=True)
        return

    if df is None or df.empty:
        st.markdown("""
            <div class='error-message'>
                ⚠️ No data found in the file.
            </div>
        """, unsafe_allow_html=True)
        return

    # Process data with enhanced progress bar
    st.markdown("""
        <div style='margin: 2rem 0;'>
            <h3 style='color: #1f1f1f; text-align: center; margin-bottom: 1.5rem;'>
                🔄 Processing Your Portfolio
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_rows = len(df)
    
    for idx, row in df.iterrows():
        # Update progress
        progress = (idx + 1) / total_rows
        progress_bar.progress(progress)
        status_text.text(f"Processing row {idx + 1} of {total_rows}")
        
        current_qty = row["Current Quantity"]
        current_avg_price = row["Current Average Price"]
        market_price = row["Current Market Price"]

        if current_qty == 0 or market_price == 0:
            continue

        if market_price >= current_avg_price:
            shares, new_avg = None, None
            profit = (market_price - current_avg_price) * current_qty
            note = "✅ Profitable"
        else:
            if strategy == "Mean of current avg & market":
                target_avg_price = (current_avg_price + market_price) / 2
            elif strategy == "10% below current avg":
                target_avg_price = current_avg_price * 0.90
            elif strategy == "5% above market price":
                target_avg_price = market_price * 1.05
            else:
                target_avg_price = (current_avg_price + market_price) / 2

            shares, new_avg, profit = calculate_averaging(
                current_qty,
                current_avg_price,
                market_price,
                target_avg_price
            )
            note = "🔻 Loss - Averaging Suggested"

        results.append({
            "Stock": row["Stock"],
            "Current Quantity": current_qty,
            "Current Average Price": round(current_avg_price, 2),
            "Current Market Price": round(market_price, 2),
            "Shares to Buy": shares if shares is not None else "N/A",
            "New Average Price": round(new_avg, 2) if new_avg else "N/A",
            "Estimated Profit": round(profit, 2) if profit else "N/A",
            "Smart Note": note
        })

    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()

    if not results:
        st.markdown("""
            <div class='error-message'>
                ⚠️ No valid rows to calculate.
            </div>
        """, unsafe_allow_html=True)
        return

    # Display results with enhanced organization
    st.markdown("""
        <div style='margin: 2rem 0;'>
            <h3 style='color: #1f1f1f; text-align: center; margin-bottom: 1.5rem;'>
                📊 Portfolio Analysis Results
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Summary statistics with enhanced styling
    total_stocks = len(results)
    profitable_stocks = sum(1 for r in results if r["Smart Note"] == "✅ Profitable")
    loss_stocks = sum(1 for r in results if r["Smart Note"] == "🔻 Loss - Averaging Suggested")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;'>
                <h4 style='color: #1f1f1f; margin-bottom: 0.5rem;'>Total Stocks</h4>
                <p style='color: #4CAF50; font-size: 1.5rem; font-weight: 600;'>{total_stocks}</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;'>
                <h4 style='color: #1f1f1f; margin-bottom: 0.5rem;'>Profitable Stocks</h4>
                <p style='color: #28a745; font-size: 1.5rem; font-weight: 600;'>{profitable_stocks}</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;'>
                <h4 style='color: #1f1f1f; margin-bottom: 0.5rem;'>Stocks Needing Averaging</h4>
                <p style='color: #dc3545; font-size: 1.5rem; font-weight: 600;'>{loss_stocks}</p>
            </div>
        """, unsafe_allow_html=True)

    # Display results table
    result_df = pd.DataFrame(results)
    display_results_table(result_df)
    
    # Download button with enhanced styling
    st.markdown("""
        <div style='margin: 2rem 0;'>
            <h3 style='color: #1f1f1f; text-align: center; margin-bottom: 1.5rem;'>
                💾 Download Results
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    download_csv_button(result_df)

    # Add simple footer
    st.markdown("""
        <div style='margin-top: 2rem; padding: 1rem; text-align: center; color: #666; font-size: 0.9rem;'>
            Created with ❤️ by Saurabh
        </div>
    """, unsafe_allow_html=True)
