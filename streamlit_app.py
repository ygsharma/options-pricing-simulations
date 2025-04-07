import streamlit as st
from option_pricing.black_scholes import black_scholes_price
from option_pricing.monte_carlo import monte_carlo_price
from option_pricing.binomial_tree import binomial_tree_price
import yfinance as yf
import requests_cache
from datetime import datetime
import numpy as np
import os

# Setup cache and logging directory
requests_cache.install_cache("yfinance_cache", backend="sqlite", expire_after=1800)

def log_invalid_ticker(ticker):
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{today}.log")
    with open(log_path, "a") as log_file:
        log_file.write(f"{datetime.now().isoformat()} - Invalid Ticker: {ticker}\n")

class OptionPricingApp:
    def __init__(self):
        self.stock = None
        self.expirations = []
        self.ticker = "AAPL"
        self.expiry = None
        self.strike = 100.0
        self.option_type = "call"
        self.model = "Black-Scholes"
        self.r = 0.045
        self.vol_choice = "Implied Volatility"
        self.custom_vol = None
        self.submitted = False

    def fetch_stock_data(self):
        """
        Fetch the stock object and available option expirations from Yahoo Finance.
        """
        
        try:
            self.stock = yf.Ticker(self.ticker)
            test_price = self.stock.history(period="1d")
            if test_price.empty:
                raise ValueError("Invalid ticker or no data available.")
            self.expirations = self.stock.options
            return True
        except Exception:
            self.stock = None
            self.expirations = []
            return False

    def calculate_historical_volatility(self):
        """
        Calculate annualized historical volatility from 1 year of daily returns.
        """
        
        hist = self.stock.history(period="1y")
        log_returns = np.log(hist['Close'] / hist['Close'].shift(1)).dropna()
        return log_returns.std() * np.sqrt(252)

    def get_implied_volatility(self):
        """
        Extract implied volatility for the closest strike to the selected one.
        """
        
        if self.expiry not in self.stock.options:
            raise ValueError(f"Expiration {self.expiry} not available. Choose from: {self.stock.options}")
        
        opt_chain = self.stock.option_chain(self.expiry)
        chain = opt_chain.calls if self.option_type == "call" else opt_chain.puts
        closest_strike = min(chain['strike'], key=lambda x: abs(x - self.strike))
        iv_row = chain[chain['strike'] == closest_strike]
        
        if iv_row.empty or iv_row['impliedVolatility'].isna().all():
            raise ValueError("Implied volatility not available for the selected strike/date.")
        
        iv = float(iv_row['impliedVolatility'].values[0]) / 10
        
        if not (0.01 <= iv <= 3.0):
            raise ValueError(f"Retrieved implied volatility {iv:.2f} is out of expected range (1%-300%).")
        return iv

    def run(self):
        """
        Launch the Streamlit UI for the Option Pricing Simulator.
        Includes ticker validation, autocomplete, and logging of invalid attempts.
        """
        
        st.set_page_config(page_title="Option Pricing Simulator", layout="centered")
        st.title("\U0001F4C8 Option Pricing Simulator")

        with st.form("option_form"):
            self.ticker = st.text_input("Enter stock ticker symbol (e.g., AAPL, TSLA):", self.ticker).upper()


            self.submitted = st.form_submit_button("Calculate")
            self.fetch_stock_data()

            self.expiry = st.selectbox("Select Expiry Date", self.expirations, key="expiry_select") if self.expirations else st.text_input("Enter Expiry Date (YYYY-MM-DD)", value="2025-12-31", key="expiry_text")
            self.strike = st.number_input("Strike Price", min_value=1.0, value=self.strike, key="strike_input")
            self.option_type = st.radio("Option Type", ["call", "put"], horizontal=True, key="option_type_radio")
            self.model = st.selectbox("Model", ["Black-Scholes", "Monte Carlo", "Binomial Tree"], key="model_select")
            self.r = st.slider("Risk-Free Rate (%)", 0.0, 10.0, self.r * 100, key="rate_slider") / 100
            self.vol_choice = st.radio("Volatility Source", ["Implied Volatility", "Historical Volatility", "Custom Volatility"], key="vol_choice_radio")
            
            if self.vol_choice == "Custom Volatility":
                self.custom_vol = st.slider("Custom Volatility (%)", 1.0, 150.0, 25.0, key="custom_vol_slider") / 100

        if self.submitted:
            if self.stock:
                self.calculate_price()
            else:
                log_invalid_ticker(self.ticker)
                st.error("❌ Invalid or unsupported stock ticker. Please enter a valid symbol.")


    def calculate_price(self):
        """
        Compute the option price based on the selected model and volatility input.
        """
        try:
            S = self.stock.history(period="1d")["Close"][0]
            expiry_date = datetime.strptime(self.expiry, "%Y-%m-%d").date()
            T = max((expiry_date - datetime.now().date()).days / 365, 1e-5)

            if self.vol_choice == "Implied Volatility":
                sigma = self.get_implied_volatility()
            elif self.vol_choice == "Historical Volatility":
                sigma = self.calculate_historical_volatility()
            elif self.vol_choice == "Custom Volatility":
                if self.custom_vol is None:
                    raise ValueError("Custom volatility must be selected.")
                sigma = self.custom_vol
            else:
                raise ValueError("Invalid volatility source selection.")

            if self.model == "Black-Scholes":
                price = black_scholes_price(S, self.strike, T, self.r, sigma, self.option_type)
            elif self.model == "Monte Carlo":
                price = monte_carlo_price(S, self.strike, T, self.r, sigma, self.option_type)
            else:
                price = binomial_tree_price(S, self.strike, T, self.r, sigma, self.option_type)

            st.success(f"The estimated {self.option_type} option price using {self.model} is: ${price:.2f}\nVolatility used: {sigma:.2%}")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    app = OptionPricingApp()
    app.run()
