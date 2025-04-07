import math

def binomial_tree_price(S, K, T, r, sigma, option_type="call", steps=200):
    """
    Calculate the price of a European option using Binomial Tree method.
    
    Args:
        S: Current price of the underlying asset (spot price)
        K: Strike price of 1option
        T: Time t maturity in years
        r: Risk-free interest rate (annualized)
        sigma: Volatility of the underlying asset (annualized)
        option_type: 'call' or 'put'
        steps: Number of time steps in binomial tree (default = 200)
        
    Returns:
        Estimated price of European option using the binomial tree model.
    
    """
    
    if T <= 0 or sigma <= 0:
        raise ValueError("Time to maturity and volatility must be positive.")
    
    if option_type not in ['call', 'put']:
        raise ValueError("option_type must be 'call' or 'put'.")
    
    dt = T / steps
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)

    prices = [S * (u ** j) * (d ** (steps - j)) for j in range(steps + 1)]
    option_values = [max(0, (price - K) if option_type == "call" else (K - price)) for price in prices]

    for i in range(steps - 1, -1, -1):
        option_values = [
            math.exp(-r * dt) * (p * option_values[j + 1] + (1 - p) * option_values[j])
            for j in range(i + 1)
        ]
    return option_values[0]