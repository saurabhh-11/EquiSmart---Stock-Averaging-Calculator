import streamlit as st
from calculations import calculate_averaging
from portfolio_uploader import portfolio_upload_ui
from data_handler import validate_inputs

# Page config with custom theme - MUST be the first Streamlit command
st.set_page_config(
    page_title="📊 EquiSmart - Stock Averaging Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    st.image("https://img.icons8.com/fluency/96/000000/stocks.png", width=120)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>EquiSmart</h1>", unsafe_allow_html=True)
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
        Made with ❤️ by EquiSmart
    </div>
    """, unsafe_allow_html=True)

# Main content with enhanced header
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #1f1f1f; font-size: 2.5rem; font-weight: 700;'>
            📈 EquiSmart: Smart Stock Averaging Calculator
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
    
    # Create a form with enhanced styling
    with st.form("single_stock_form"):
        col1, col2 = st.columns(2)
        
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
                value=50.0,
                help="Enter the current market price"
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
    portfolio_upload_ui()

# Remove the old simple footer and add a new professional footer at the end of the file
st.markdown('''
<hr style="margin-top: 3rem; margin-bottom: 1.5rem; border: none; border-top: 1px solid #e0e0e0;" />
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 1.5rem 0 0.5rem 0;">
    <div style="font-size: 1.1rem; color: #222; font-weight: 600; margin-bottom: 0.3rem; letter-spacing: 0.5px;">
        EquiSmart – Smarter Stock Averaging
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
        &copy; 2025 EquiSmart. All rights reserved.
    </div>
</div>
''', unsafe_allow_html=True)
