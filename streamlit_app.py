import streamlit as st
from option_pricing.black_scholes import black_scholes_price
from option_pricing.monte_carlo import monte_carlo_price
from option_pricing.binomial_tree import binomial_tree_price
import yfinance as yf
import requests_cache
from datetime import datetime
import numpy as np

requests_cache.install_cache("yfinance_cache", backend="sqlite", expire_after=1800)

st.set_page_config(page_title="Option Pricing Simulator", layout="centered")
st.title("\U0001F4C8 Option Pricing Simulator")

stock = None
expiration_dates = []

ticker = st.text_input("Stock Ticker", "AAPL")
if ticker:
    try:
        stock = yf.Ticker(ticker)
        expiration_dates = stock.options
    except Exception as e:
        st.error(f"Failed to fetch data for ticker: {ticker}. Error: {e}")

with st.form("option_form"):
    if expiration_dates:
        expiry = st.selectbox("Select Expiry Date", expiration_dates, index=0)
    else:
        expiry = st.text_input("Enter Expiry Date (YYYY-MM-DD)", value="2025-12-31")

    strike = st.number_input("Strike Price", min_value=1.0, value=100.0)
    option_type = st.radio("Option Type", ["call", "put"], horizontal=True)
    model = st.selectbox("Model", ["Black-Scholes", "Monte Carlo", "Binomial Tree"])
    r = st.slider("Risk-Free Rate (%)", 0.0, 10.0, 4.5) / 100
    vol_choice = st.radio("Volatility Source", ["Historical Volatility", "Implied Volatility"])

    if vol_choice == "Historical Volatility":
        manual_vol = st.slider("Estimated Volatility (%)", min_value=1.0, max_value=150.0, value=20.0) / 100
    else:
        manual_vol = None

    submitted = st.form_submit_button("Calculate")

if submitted and stock:
    try:
        S = stock.history(period="1d")["Close"][0]
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        T = max((expiry_date - datetime.now().date()).days / 365, 1e-5)

        if vol_choice == "Historical Volatility":
            hist = stock.history(period="1y")
            log_returns = np.log(hist['Close'] / hist['Close'].shift(1)).dropna()
            sigma = log_returns.std() * np.sqrt(252)
        else:
            if expiry not in stock.options:
                raise ValueError(f"Expiration {expiry} not available. Choose from: {stock.options}")
            opt_chain = stock.option_chain(expiry)
            chain = opt_chain.calls if option_type == "call" else opt_chain.puts
            closest_strike = min(chain['strike'], key=lambda x: abs(x - strike))
            iv_row = chain[chain['strike'] == closest_strike]
            if iv_row.empty or iv_row['impliedVolatility'].isna().all():
                raise ValueError("Implied volatility not available for the selected strike/date.")
            sigma = float(iv_row['impliedVolatility'].values[0])

        if model == "Black-Scholes":
            price = black_scholes_price(S, strike, T, r, sigma, option_type)
        elif model == "Monte Carlo":
            price = monte_carlo_price(S, strike, T, r, sigma, option_type)
        else:
            price = binomial_tree_price(S, strike, T, r, sigma, option_type)

        st.success(f"The estimated {option_type} option price using {model} is: ${price:.2f}\nVolatility used: {sigma:.2%}")
    except Exception as e:
        st.error(f"Error: {e}")
