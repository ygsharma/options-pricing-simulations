import streamlit as st
from option_pricing.black_scholes import black_scholes_price
from option_pricing.monte_carlo import monte_carlo_price
from option_pricing.binomial_tree import binomial_tree_price
import yfinance as yf
import requests_cache
from datetime import datetime

requests_cache.install_cache("yfinance_cache", backend="sqlite", expire_after=1800)

st.set_page_config(page_title="Option Pricing Simulator", layout="centered")
st.title("\U0001F4C8 Option Pricing Simulator")

with st.form("option_form"):
    ticker = st.text_input("Stock Ticker", "AAPL")
    strike = st.number_input("Strike Price", min_value=1.0, value=100.0)
    expiry = st.date_input("Expiry Date", value=datetime(2025, 12, 31))
    r = st.slider("Risk-Free Rate (%)", 0.0, 10.0, 5.0) / 100
    sigma = st.slider("Volatility (%)", 0.0, 100.0, 20.0) / 100
    option_type = st.radio("Option Type", ["call", "put"], horizontal=True)
    model = st.selectbox("Model", ["Black-Scholes", "Monte Carlo", "Binomial Tree"])
    submitted = st.form_submit_button("Calculate")

if submitted:
    try:
        stock = yf.Ticker(ticker)
        S = stock.history(period="1d")["Close"][0]
        T = max((expiry - datetime.now().date()).days / 365, 1e-5)

        if model == "Black-Scholes":
            price = black_scholes_price(S, strike, T, r, sigma, option_type)
        elif model == "Monte Carlo":
            price = monte_carlo_price(S, strike, T, r, sigma, option_type)
        else:
            price = binomial_tree_price(S, strike, T, r, sigma, option_type)

        st.success(f"The estimated {option_type} option price using {model} is: ${price:.2f}")
    except Exception as e:
        st.error(f"Error: {e}")