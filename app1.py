import streamlit as st
from calculations import calculate_averaging
from portfolio_uploader import portfolio_upload_ui
from data_handler import validate_inputs
from fetch_price import get_live_price
from risk_analyzer import analyze_stock_risk

# Page config with custom theme - MUST be the first Streamlit command
st.set_page_config(
    page_title="📊 Averra – Precision Averaging for Smarter Growth",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safely initialize required session state variables
if "stock_code" not in st.session_state:
    st.session_state["stock_code"] = "RELIANCE"  # or any default
if "market_price" not in st.session_state:
    st.session_state["market_price"] = 50.0
if "live_price" not in st.session_state:
    st.session_state["live_price"] = None
if "risk_analysis" not in st.session_state:
    st.session_state["risk_analysis"] = None


# Enhanced Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .stTitle {
        color: #1f1f1f;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
        padding-bottom: 1rem;
        border-bottom: 2px solid #4CAF50;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Input field styling */
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 0.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stNumberInput>div>div>input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76,175,80,0.2);
    }
    
    /* Select box styling */
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 0.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stSelectbox>div>div>select:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76,175,80,0.2);
    }
    
    /* Expander styling */
    .stExpander {
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .stExpander:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding: 1.5rem;
        background-color: #ffffff;
        box-shadow: 2px 0 8px rgba(0,0,0,0.1);
    }
    
    /* Metric styling */
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Form styling */
    .stForm {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    /* Markdown styling */
    .stMarkdown {
        color: #2c3e50;
    }
    
    /* Custom success message */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    /* Custom error message */
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
    }
    
    /* Custom info message */
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #17a2b8;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar styling with enhanced visuals
with st.sidebar:
    # Logo and title with better spacing
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("Averra.png", width=120)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'></h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation with icons
    menu = ["Single Stock Calculator", "Batch Portfolio Averaging"]
    choice = st.selectbox("📊 Choose Mode", menu)
    
    st.markdown("---")
    
    # Quick stats with better styling
    st.markdown("### 📈 Quick Stats")
    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px;'>
        💡 Smart averaging helps reduce your average cost
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        Made with ❤️ by Averra
    </div>
    """, unsafe_allow_html=True)

# Main content with enhanced header
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #1f1f1f; font-size: 2.5rem; font-weight: 700;'>
            📈 Averra – Precision Averaging for Smarter Growth
        </h1>
        <p style='color: #666; font-size: 1.1rem;'>
            Make smarter investment decisions with our advanced averaging calculator
        </p>
    </div>
""", unsafe_allow_html=True)

# Guidelines expander with enhanced styling
with st.expander("📚 Smart Investing Guidelines (Must-Read)", expanded=False):
    st.markdown(
        '''<div style="background-color: #f8f9fa; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
<div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
<img src="https://img.icons8.com/fluency/48/000000/light-on.png" style="width: 32px; height: 32px; margin-right: 1rem;">
<h3 style="color: #1f1f1f; margin: 0;">Understanding Stock Averaging</h3>
</div>
<div style="background-color: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<p style="color: #666; line-height: 1.6; margin-bottom: 1rem;">
Stock averaging is a strategic investment technique where you buy more shares of a stock you already own at a lower price to reduce your average cost per share.
</p>
<div style="background-color: #e8f5e9; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
<p style="color: #2e7d32; margin: 0;"><strong>Example:</strong> Buy 10 shares @ ₹200 → Price drops to ₹150 → Buy 10 more → New avg = ₹175</p>
</div>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
<div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
<img src="https://img.icons8.com/fluency/48/000000/checked-2.png" style="width: 24px; height: 24px; margin-right: 0.5rem;">
<h4 style="color: #1f1f1f; margin: 0;">When to Consider</h4>
</div>
<ul style="color: #666; list-style-type: none; padding-left: 0;">
<li style="margin-bottom: 0.5rem;">✅ Strong company fundamentals</li>
<li style="margin-bottom: 0.5rem;">✅ Thorough research completed</li>
<li style="margin-bottom: 0.5rem;">✅ Long-term investment horizon</li>
<li style="margin-bottom: 0.5rem;">✅ Market correction opportunity</li>
</ul>
</div>
<div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
<img src="https://img.icons8.com/fluency/48/000000/cancel.png" style="width: 24px; height: 24px; margin-right: 0.5rem;">
<h4 style="color: #1f1f1f; margin: 0;">When to Avoid</h4>
</div>
<ul style="color: #666; list-style-type: none; padding-left: 0;">
<li style="margin-bottom: 0.5rem;">❌ Just because price dropped</li>
<li style="margin-bottom: 0.5rem;">❌ Declining company performance</li>
<li style="margin-bottom: 0.5rem;">❌ Overexposure in portfolio</li>
<li style="margin-bottom: 0.5rem;">❌ Emotional decision making</li>
</ul>
</div>
</div>
<div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
<img src="https://img.icons8.com/fluency/48/000000/brain.png" style="width: 24px; height: 24px; margin-right: 0.5rem;">
<h4 style="color: #1f1f1f; margin: 0;">Smart Averaging Tips</h4>
</div>
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 6px;"><p style="color: #666; margin: 0;">🔢 Limit to 2-3 rounds max</p></div>
<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 6px;"><p style="color: #666; margin: 0;">📝 Track reasons for averaging</p></div>
<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 6px;"><p style="color: #666; margin: 0;">🎯 Set clear price targets</p></div>
<div style="background-color: #f8f9fa; padding: 1rem; border-radius: 6px;"><p style="color: #666; margin: 0;">📊 Monitor portfolio balance</p></div>
</div>
</div>
</div>''', unsafe_allow_html=True)

# Strategy expander with enhanced styling
with st.expander("🎯 Choose Your Averaging Strategy", expanded=False):
    st.markdown(
        '''<div style="background-color: #f8f9fa; padding: 2rem; border-radius: 12px;">
<div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
<img src="https://img.icons8.com/fluency/48/000000/strategy.png" style="width: 32px; height: 32px; margin-right: 1rem;">
<h3 style="color: #1f1f1f; margin: 0;">Select Your Strategy</h3>
</div>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2rem;">
<div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
<img src="https://img.icons8.com/fluency/48/000000/balance.png" style="width: 24px; height: 24px; margin-right: 0.5rem;">
<h4 style="color: #1f1f1f; margin: 0;">Balanced Approach</h4>
</div>
<p style="color: #666; margin-bottom: 1rem;"><strong>Mean of current avg & market</strong></p>
<p style="color: #666; font-size: 0.9rem;">Takes the average of your current average price and market price. Perfect for gradual cost reduction and balanced risk management.</p>
</div>
<div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
<img src="https://img.icons8.com/fluency/48/000000/shield.png" style="width: 24px; height: 24px; margin-right: 0.5rem;">
<h4 style="color: #1f1f1f; margin: 0;">Conservative</h4>
</div>
<p style="color: #666; margin-bottom: 1rem;"><strong>10% below current avg</strong></p>
<p style="color: #666; font-size: 0.9rem;">Waits for a deeper price drop before averaging. Ideal for cautious investors who want to ensure better entry points.</p>
</div>
<div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
<img src="https://img.icons8.com/fluency/48/000000/rocket.png" style="width: 24px; height: 24px; margin-right: 0.5rem;">
<h4 style="color: #1f1f1f; margin: 0;">Aggressive</h4>
</div>
<p style="color: #666; margin-bottom: 1rem;"><strong>5% above market price</strong></p>
<p style="color: #666; font-size: 0.9rem;">Aims to average before potential price recovery. Best for investors who believe in quick market rebounds.</p>
</div>
</div>
<div style="background-color: #e8f5e9; padding: 1.5rem; border-radius: 8px; margin-top: 1.5rem;">
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
<img src="https://img.icons8.com/fluency/48/000000/light-on.png" style="width: 24px; height: 24px; margin-right: 0.5rem;">
<h4 style="color: #1f1f1f; margin: 0;">Pro Tip</h4>
</div>
<p style="color: #2e7d32; margin: 0;">Choose your strategy based on your risk tolerance and market outlook. You can always adjust your approach as market conditions change.</p>
</div>
</div>''', unsafe_allow_html=True)

if choice == "Single Stock Calculator":
    st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h2 style='color: #1f1f1f; font-size: 1.8rem; font-weight: 600;'>
                📥 Enter Your Stock Details
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for market price
    if 'market_price' not in st.session_state:
        st.session_state['market_price'] = 50.0
    if 'live_price' not in st.session_state:
        st.session_state['live_price'] = None
    
    if 'risk_analysis' not in st.session_state:
        st.session_state['risk_analysis'] = None
    

      # Stock code input and risk analysis button OUTSIDE the form
    stock_code = st.text_input(
        "Stock Name or NSE Code",
        value=st.session_state['stock_code'],
        help="Enter the NSE stock code (e.g., RELIANCE, TCS, INFY) or company name"
    )
    st.session_state['stock_code'] = stock_code
    if st.button("Analyze Risk"):
        st.session_state['risk_analysis'] = analyze_stock_risk(stock_code)
    if st.session_state['risk_analysis']:
        ra = st.session_state['risk_analysis']
        pe_display = f"{ra['pe']}" if ra['pe'] is not None else "N/A"
       # debt_display = f"{ra['debt']}" if ra['debt'] is not None else "N/A"
        volatility_display = f"{ra['volatility']:.2f}" if ra['volatility'] is not None else "N/A"
        roe_display = f"{ra['roe']:.2f}%" if ra['roe'] is not None else "N/A"
       # pb_display = f"{ra['pb']}" if ra['pb'] is not None else "N/A"
        eps_display = f"{ra['eps']}" if ra['eps'] is not None else "N/A"
        market_cap_display = f"{ra['market_cap']}" if ra['market_cap'] is not None else "N/A"
        sector_display = ra['sector'] if ra['sector'] is not None else "N/A"
        industry_display = ra['industry'] if ra['industry'] is not None else "N/A"
        st.markdown(f"""
        <div class='info-message'>
        <b>Risk Analyzer:</b><br>
        PE Ratio: <b>{pe_display}</b><br>
        Volatility (1Y): <b>{volatility_display}</b><br>
        ROE: <b>{roe_display}</b><br>
        EPS: <b>{eps_display}</b><br>
        Market Cap: <b>{market_cap_display}</b><br>
        Sector: <b>{sector_display}</b><br>
        Industry: <b>{industry_display}</b><br>
        <b>Recommendation:</b> {'✅ Averaging Allowed' if ra['allowed'] else '❌ Averaging Not Recommended'}<br>
        {('<br>'.join(ra['reasons'])) if not ra['allowed'] else ''}
        </div>
        """, unsafe_allow_html=True)

    with st.form("single_stock_form"):
        col0, col1, col2 = st.columns([2,2,2])
        with col0:
            # stock_code = st.text_input(
            #     "Stock Name or NSE Code",
            #     value="RELIANCE",
            #     help="Enter the NSE stock code (e.g., RELIANCE, TCS, INFY) or company name"
            # )
            fetch_price_btn = st.form_submit_button("Fetch Live Price")
            if fetch_price_btn and stock_code:
                live_price = get_live_price(stock_code)
                if live_price is not None:
                    st.session_state['market_price'] = float(live_price)
                    st.session_state['live_price'] = float(live_price)
                    st.success(f"Live price for {stock_code}: ₹{live_price}")
                else:
                    st.warning(f"Could not fetch live price for {stock_code}. Please enter manually.")
        with col1:
            current_qty = st.number_input(
                "Current Quantity",
                min_value=1,
                value=10,
                help="Enter your current number of shares"
            )
            current_avg_price = st.number_input(
                "Your Current Average Price (₹)",
                min_value=0.0,
                value=100.0,
                help="Enter your current average purchase price"
            )
        with col2:
            market_price = st.number_input(
                "Current Market Price (₹)",
                min_value=0.01,
                value=st.session_state['market_price'],
                key="market_price",
                help="Enter the current market price or fetch live price"
            )
            st.markdown("### 💡 Averaging Strategy")
            strategy = st.selectbox(
                "Select a Strategy",
                [
                    "Manual Input",
                    "Mean of Current Avg & Market Price",
                    "10% Below Current Avg",
                    "5% Above Market Price"
                ],
                help="Choose your preferred averaging strategy"
            )

        # Strategy calculations with enhanced visual feedback
        if strategy == "Mean of Current Avg & Market Price":
            target_avg_price = round((current_avg_price + market_price) / 2, 2)
            st.markdown(f"""
                <div class='info-message'>
                    📘 Strategy: Average of ₹{current_avg_price} and ₹{market_price} → ₹{target_avg_price}
                </div>
            """, unsafe_allow_html=True)
        elif strategy == "10% Below Current Avg":
            target_avg_price = round(current_avg_price * 0.90, 2)
            st.markdown(f"""
                <div class='info-message'>
                    📘 Strategy: 10% below current average ₹{current_avg_price} → ₹{target_avg_price}
                </div>
            """, unsafe_allow_html=True)
        elif strategy == "5% Above Market Price":
            target_avg_price = round(market_price * 1.05, 2)
            st.markdown(f"""
                <div class='info-message'>
                    📘 Strategy: 5% above market price ₹{market_price} → ₹{target_avg_price}
                </div>
            """, unsafe_allow_html=True)
        else:
            target_avg_price = st.number_input(
                "Target Average Price (₹)",
                min_value=0.01,
                value=70.0,
                help="Enter your target average price"
            )

        submitted = st.form_submit_button("Calculate")

    if submitted:
        is_valid, error = validate_inputs(current_qty, current_avg_price, market_price, target_avg_price)
        if not is_valid:
            st.markdown(f"""
                <div class='error-message'>
                    ❌ {error}
                </div>
            """, unsafe_allow_html=True)
        else:
            result = calculate_averaging(current_qty, current_avg_price, market_price, target_avg_price)
            shares_to_buy, new_avg, estimated_profit = result

            if shares_to_buy is None:
                st.markdown("""
                    <div class='error-message'>
                        ❌ Target average is not reachable with current market price.
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Display results with enhanced styling
                st.markdown("""
                    <div style='margin: 2rem 0;'>
                        <h3 style='text-align: center; color: #1f1f1f; margin-bottom: 1.5rem;'>
                            📊 Calculation Results
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                        <div class='success-message'>
                            ✅ Buy **{shares_to_buy} shares** at ₹{market_price}
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div class='info-message'>
                            🎯 New average price: ₹{new_avg:.2f}
                        </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                        <div class='success-message'>
                            💰 Estimated profit: ₹{estimated_profit:,.2f}
                        </div>
                    """, unsafe_allow_html=True)




elif choice == "Batch Portfolio Averaging":
    st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h2 style='color: #1f1f1f; font-size: 1.8rem; font-weight: 600;'>
                📤 Upload Your Portfolio Excel File
            </h2>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Excel file with columns: Stock, Avg Price, Quantity, P/L", type=['xlsx'])

    if uploaded_file:
        import pandas as pd
        df = pd.read_excel(uploaded_file)
        required_columns = ['Stock', 'Quantity', 'Avg Price', 'P/L']
        df.columns = [col.strip() for col in df.columns]  # Remove spaces

        # Check if all required columns are present
        if not all(col in df.columns for col in required_columns):
            st.error(f"Invalid format. Required columns: {', '.join(required_columns)}")
            st.stop()

        # Reorder columns for consistency
        df = df[required_columns]


        if {'Stock', 'Avg Price', 'Quantity', 'P/L'}.issubset(df.columns):
            st.success("✅ File uploaded successfully and required columns found.")
            st.dataframe(df)

            strategy = st.selectbox(
                "Select Averaging Strategy",
                ["Mean of Avg & Market", "10% Below Avg", "5% Above Market"]
            )

            results = []

            for idx, row in df.iterrows():
                stock = row['Stock']
                avg_price = row['Avg Price']
                qty = row['Quantity']

                # Get market price
                from fetch_price import get_live_price
                market_price = get_live_price(stock)
                if not market_price:
                    continue

                if strategy == "Mean of Avg & Market":
                    target_price = round((avg_price + market_price) / 2, 2)
                elif strategy == "10% Below Avg":
                    target_price = round(avg_price * 0.90, 2)
                else:
                    target_price = round(market_price * 1.05, 2)

                from calculations import calculate_averaging
                shares, new_avg, est_profit = calculate_averaging(qty, avg_price, market_price, target_price)

                from risk_analyzer import analyze_stock_risk
                risk = analyze_stock_risk(stock)

                results.append({
                    'Stock': stock,
                    'Current Avg': avg_price,
                    'Market Price': market_price,
                    'Target Avg': target_price,
                    'Buy Qty': shares,
                    'New Avg': new_avg,
                    'Est. Profit': est_profit,
                    'Risk': risk.get("risk_level", "Unknown"),
                    'Rating': risk.get("fundamentals_rating", "Unknown"),
                    'Allowed': '✅' if risk.get("allowed") else '❌'
                })

            if results:
                st.markdown("""
                    <div style='margin: 2rem 0;'>
                        <h3 style='text-align: center; color: #1f1f1f; margin-bottom: 1.5rem;'>📊 Averaging Summary with Risk</h3>
                    </div>
                """, unsafe_allow_html=True)
                results_df = pd.DataFrame(results)
                st.dataframe(results_df)

                # Download button
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name='averaging_results.csv',
                    mime='text/csv'
                )
            else:
                st.warning("⚠️ No valid stocks processed. Please check names and values.")
        else:
            st.error("❌ Invalid format. Required columns: Stock, Avg Price, Quantity, P/L")


# elif choice == "Batch Portfolio Averaging":
#     st.markdown("""
#         <div style='text-align: center; margin: 2rem 0;'>
#             <h2 style='color: #1f1f1f; font-size: 1.8rem; font-weight: 600;'>
#                 📤 Upload Your Portfolio Excel File
#             </h2>
#         </div>
#     """, unsafe_allow_html=True)

#     uploaded_file = st.file_uploader("Upload Excel file with columns: Stock, Avg Price, Quantity, P/L", type=['xlsx'])

#     if uploaded_file:
#         import pandas as pd
#         df = pd.read_excel(uploaded_file)
#         required_columns = ['Stock', 'Quantity', 'Avg Price', 'P/L']
#         df.columns = [col.strip() for col in df.columns]  # Remove spaces

#         if not all(col in df.columns for col in required_columns):
#             st.error(f"Invalid format. Required columns: {', '.join(required_columns)}")
#             st.stop()

#         df = df[required_columns]

#         st.success("✅ File uploaded successfully and required columns found.")
#         st.dataframe(df)

#         results = []

#         for idx, row in df.iterrows():
#             stock = row['Stock']
#             avg_price = row['Avg Price']
#             qty = row['Quantity']
#             pnl = row['P/L']

#             from fetch_price import get_live_price
#             from calculations import calculate_averaging
#             from risk_analyzer import analyze_stock_risk

#             market_price = get_live_price(stock)
#             if not market_price:
#                 continue

#             risk = analyze_stock_risk(stock)
#             allowed = risk.get("allowed", False)
#             fundamentals = risk.get("fundamentals_rating", "Unknown")
#             risk_level = risk.get("risk_level", "Unknown")

#             # Smart strategy logic based on P/L and risk
#             if pnl > 0:
#                 smart_strategy = "Already in Profit"
#                 shares = new_avg = est_profit = target_price = None
#             elif fundamentals == "Good" and risk_level == "Low":
#                 smart_strategy = "Aggressive"
#                 target_price = round(market_price * 1.05, 2)
#             elif fundamentals == "Good" and risk_level == "Moderate":
#                 smart_strategy = "Balanced"
#                 target_price = round((avg_price + market_price) / 2, 2)
#             else:
#                 smart_strategy = "Conservative"
#                 target_price = round(avg_price * 0.90, 2)

#             if pnl > 0:
#                 remark = "✅ In Profit"
#             elif not allowed:
#                 remark = "❌ Averaging Not Advised"
#             else:
#                 shares, new_avg, est_profit = calculate_averaging(qty, avg_price, market_price, target_price)
#                 remark = "✅ Averaging Suggested" if shares else "⚠️ Target Not Reachable"

#             results.append({
#                 'Stock': stock,
#                 'Current Avg': avg_price,
#                 'Market Price': market_price,
#                 'Target Avg': target_price if pnl <= 0 else 'N/A',
#                 'Buy Qty': shares if pnl <= 0 else 'N/A',
#                 'New Avg': new_avg if pnl <= 0 else 'N/A',
#                 'Est. Profit': est_profit if pnl <= 0 else 'N/A',
#                 'Risk': risk_level,
#                 'Rating': fundamentals,
#                 'Allowed': '✅' if allowed else '❌',
#                 'Strategy': smart_strategy,
#                 'Remark': remark
#             })

#         if results:
#             st.markdown("""
#                 <div style='margin: 2rem 0;'>
#                     <h3 style='text-align: center; color: #1f1f1f; margin-bottom: 1.5rem;'>📊 Portfolio Summary with Strategy</h3>
#                 </div>
#             """, unsafe_allow_html=True)
#             results_df = pd.DataFrame(results)
#             st.dataframe(results_df)

#             csv = results_df.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="📥 Download Results as CSV",
#                 data=csv,
#                 file_name='portfolio_strategy_results.csv',
#                 mime='text/csv'
#             )
#         else:
#             st.warning("⚠️ No valid stocks processed. Please check names and values.")

# Remove the old simple footer and add a new professional footer at the end of the file






# elif choice == "Batch Portfolio Averaging":
#     st.markdown("""
#         <div style='text-align: center; margin: 2rem 0;'>
#             <h2 style='color: #1f1f1f; font-size: 1.8rem; font-weight: 600;'>
#                 📤 Upload Your Portfolio Excel File
#             </h2>
#         </div>
#     """, unsafe_allow_html=True)

#     uploaded_file = st.file_uploader("Upload Excel file with columns: Stock, Avg Price, Quantity, P/L", type=['xlsx'])

#     if uploaded_file:
#         import pandas as pd
#         from fetch_price import get_live_price
#         from calculations import calculate_averaging
#         from risk_analyzer import analyze_stock_risk

#         df = pd.read_excel(uploaded_file)
#         df.columns = [col.strip() for col in df.columns]

#         required_columns = ['Stock', 'Quantity', 'Avg Price', 'P/L']
#         if not all(col in df.columns for col in required_columns):
#             st.error(f"❌ Invalid format. Required columns: {', '.join(required_columns)}")
#             st.stop()

#         df = df[required_columns]
#         st.success("✅ File uploaded successfully and required columns found.")
#         st.dataframe(df)

#         strategy = st.selectbox(
#             "Select Averaging Strategy",
#             ["Mean of Avg & Market", "10% Below Avg", "5% Above Market"]
#         )

#         results = []

#         for idx, row in df.iterrows():
#             stock = str(row['Stock']).strip()
#             avg_price = row['Avg Price']
#             qty = row['Quantity']
#             profit_loss = row['P/L']

#             market_price = get_live_price(stock)
#             if market_price is None:
#                 st.warning(f"⚠️ Could not fetch market price for: {stock}")
#                 continue

#             risk = analyze_stock_risk(stock)
#             fundamentals = risk.get("fundamentals_rating", "Unknown")
#             risk_level = risk.get("risk_level", "Unknown")
#             allowed = risk.get("allowed", False)

#             if profit_loss > 0:
#                 smart_strategy = "Already in Profit"
#                 target_price = new_avg = est_profit = shares = remark = "N/A"
#             elif fundamentals == "Good" and risk_level == "Low":
#                 smart_strategy = "Aggressive"
#                 target_price = round(market_price * 1.05, 2)
#                 shares, new_avg, est_profit = calculate_averaging(qty, avg_price, market_price, target_price)
#                 remark = "✅ Averaging Suggested" if shares else "⚠️ Target Not Reachable"
#             elif fundamentals == "Good" and risk_level == "Moderate":
#                 smart_strategy = "Balanced"
#                 target_price = round((avg_price + market_price) / 2, 2)
#                 shares, new_avg, est_profit = calculate_averaging(qty, avg_price, market_price, target_price)
#                 remark = "✅ Averaging Suggested" if shares else "⚠️ Target Not Reachable"
#             else:
#                 smart_strategy = "Conservative"
#                 target_price = round(avg_price * 0.90, 2)
#                 shares, new_avg, est_profit = calculate_averaging(qty, avg_price, market_price, target_price)
#                 remark = "✅ Averaging Suggested" if shares else "⚠️ Target Not Reachable"

#             results.append({
#                 'Stock': stock,
#                 'Quantity': qty,
#                 'Avg Price': avg_price,
#                 'Market Price': market_price,
#                 'Target Avg': target_price,
#                 'Buy Qty': shares,
#                 'New Avg': new_avg,
#                 'Est. Profit': est_profit,
#                 'Strategy': smart_strategy,
#                 'Risk': risk_level,
#                 'Rating': fundamentals,
#                 'Allowed': '✅' if allowed else '❌',
#                 'Remark': remark,
#                 'Profit_Flag': profit_loss > 0  # Flag to color later
#             })

#         if results:
#             st.markdown("""
#         <div style='margin: 2rem 0;'>
#             <h3 style='text-align: center; color: #1f1f1f; margin-bottom: 1.5rem;'>📊 Averaging Summary with Risk & Strategy</h3>
#         </div>
#     """, unsafe_allow_html=True)


#             df_result = pd.DataFrame(results)

#             def highlight_row(row):
#                 if row.get('Profit_Flag'):
#                     return ['background-color: #d4edda'] * len(row)  # Green row
#                 else:
#                     return ['background-color: #fffbea'] * len(row)  # Yellow row

#             styled_df = df_result.style.apply(highlight_row, axis=1)
#             st.dataframe(styled_df, use_container_width=True)

#     # Export without the styling column
#             csv = df_result.drop(columns=["Profit_Flag"]).to_csv(index=False).encode('utf-8')
#             st.download_button(
#             label="📥 Download Results as CSV",
#             data=csv,
#             file_name='batch_portfolio_with_risk.csv',
#             mime='text/csv'
#     )

st.markdown('''
<hr style="margin-top: 3rem; margin-bottom: 1.5rem; border: none; border-top: 1px solid #e0e0e0;" />
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 1.5rem 0 0.5rem 0;">
    <div style="font-size: 1.1rem; color: #222; font-weight: 600; margin-bottom: 0.3rem; letter-spacing: 0.5px;">
        Averra – Precision Averaging for Smarter Growth 
    </div>
    <div style="color: #666; font-size: 0.98rem; margin-bottom: 0.2rem;">
        Empowering investors with intelligent tools and insights.
    </div>
    <div style="margin-top: 0.5rem;">
        <a href="mailto:saurabh.private11@gmail.com" style="color: #4CAF50; text-decoration: none; font-weight: 500;">
            📧 Contact: saurabh.private11@gmail.com
        </a>
    </div>
    <div style="color: #aaa; font-size: 0.85rem; margin-top: 0.7rem;">
        &copy; 2025 Averra. All rights reserved.
    </div>
</div>
''', unsafe_allow_html=True)