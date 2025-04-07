import math
from scipy.stats import norm

def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    """
    Calulate the price of a European option using the Black-Scholes model.
    
    Args:
        S: Current price of underlying asset (spot price)
        K: Strike price of the option
        T: Time to maturity in years
        r: Risk-free interest rate
        sigma: Volatility of underlying asset (annualized)
        option_type: 'call' or 'put'
        
    Returns:
        Estimated price of the European option using the Black-Scholes formula
    
    """
    if T <= 0 or sigma <= 0:
        raise ValueError("Time to maturity and volatility must be positive.")
    
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")