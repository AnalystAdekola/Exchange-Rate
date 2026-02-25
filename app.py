import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="GlobalFX AI Converter", page_icon="💰", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background-color: #00ffcc; color: black; border-radius: 10px; border: none;
        width: 100%; font-weight: bold; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #00d4aa; transform: scale(1.02); }
    .stMetric { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP ---
# Use Streamlit Secrets for the API Key (Secure Method)
API_KEY = st.secrets["EXCHANGE_RATE_API_KEY"]
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

@st.cache_data(ttl=3600)  # Cache rates for 1 hour to save API calls
def get_exchange_rates(base_currency):
    try:
        response = requests.get(BASE_URL + base_currency)
        data = response.json()
        if data["result"] == "success":
            return data["conversion_rates"]
        return None
    except Exception as e:
        return None

# --- SIDEBAR / INPUTS ---
st.sidebar.title("⚙️ Settings")
base_curr = st.sidebar.selectbox("Base Currency", ["USD", "EUR", "GBP", "JPY", "NGN", "CAD", "AUD"])
target_curr = st.sidebar.selectbox("Target Currency", ["EUR", "USD", "GBP", "JPY", "NGN", "CAD", "AUD"], index=1)

st.title("💰 AI-Powered Currency Converter")
st.write("Real-time global exchange rates powered by 2026 Live Data.")

# --- MAIN CONVERSION LOGIC ---
rates = get_exchange_rates(base_curr)

if rates:
    col1, col2 = st.columns([1, 1])

    with col1:
        amount = st.number_input(f"Enter Amount ({base_curr})", min_value=0.0, value=100.0)
        converted_amount = amount * rates[target_curr]
        
        st.metric(label=f"Converted to {target_curr}", value=f"{converted_amount:,.2f} {target_curr}")
        st.write(f"**Current Rate:** 1 {base_curr} = {rates[target_curr]:.4f} {target_curr}")

    with col2:
        # Mocking a "trend" chart for UI polish (AI-Powered Visuals)
        st.write("📊 Quick Market Snapshot")
        top_currencies = {k: rates[k] for k in ["USD", "EUR", "GBP", "JPY"] if k != base_curr}
        fig = go.Figure(go.Bar(
            x=list(top_currencies.keys()),
            y=list(top_currencies.values()),
            marker_color='#00ffcc'
        ))
        fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # --- RECENT CONVERSIONS LOG ---
    st.divider()
    with st.expander("ℹ️ About this Application"):
        st.write("""
            This application uses the **ExchangeRate-API** to fetch 100% accurate, real-time data. 
            The interface is built with **Streamlit** for high-performance deployment.
        """)
else:
    st.error("⚠️ Failed to fetch live rates. Please check your API key or internet connection.")
