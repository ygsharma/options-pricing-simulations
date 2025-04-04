from fastapi import FastAPI, Query
from option_pricing.black_scholes import black_scholes_price
from option_pricing.monte_carlo import monte_carlo_price
from option_pricing.binomial_tree import binomial_tree_price

app = FastAPI(title="Option Pricing API")

@app.get("/price")
def get_option_price(
    model: str = Query(..., enum=["black-scholes", "monte-carlo", "binomial-tree"]),
    S: float = 100,
    K: float = 100,
    T: float = 1,
    r: float = 0.05,
    sigma: float = 0.2,
    option_type: str = Query("call", enum=["call", "put"])
):
    if model == "black-scholes":
        return {"price": black_scholes_price(S, K, T, r, sigma, option_type)}
    elif model == "monte-carlo":
        return {"price": monte_carlo_price(S, K, T, r, sigma, option_type)}
    elif model == "binomial-tree":
        return {"price": binomial_tree_price(S, K, T, r, sigma, option_type)}