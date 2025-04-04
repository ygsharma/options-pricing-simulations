from option_pricing.black_scholes import black_scholes_price
from option_pricing.monte_carlo import monte_carlo_price
from option_pricing.binomial_tree import binomial_tree_price

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
print("Black-Scholes Price:", round(black_scholes_price(S, K, T, r, sigma), 2))
print("Monte Carlo Price:", round(monte_carlo_price(S, K, T, r, sigma), 2))
print("Binomial Tree Price:", round(binomial_tree_price(S, K, T, r, sigma), 2))