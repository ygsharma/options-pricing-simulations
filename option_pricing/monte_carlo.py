import numpy as np

def monte_carlo_price(S, K, T, r, sigma, option_type="call", num_simulations=100000):
    """
    Estimatews European option price using Monte Carlo.
    
    Args:
        S: Current stock price
        K: Strike price
        T: Time to expiration (in years)
        r: Risk-free interest rate
        sigma: Volatility
        option_type: 'call' or 'put'
        num_simulations: Number of simulations
    
    Returns:
        Estimated option price
    """
    
    if T <= 0 or sigma <= 0:
        raise ValueError("Time to maturity and volatility must be positive.")
    
    Z = np.random.standard_normal(num_simulations)
    ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
    payoff = np.maximum(ST - K, 0) if option_type == "call" else np.maximum(K - ST, 0)
    
    return np.exp(-r * T) * payoff.mean()