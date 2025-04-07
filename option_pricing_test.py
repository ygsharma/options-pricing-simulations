import math
import pytest
from option_pricing.black_scholes import black_scholes_price
from option_pricing.monte_carlo import monte_carlo_price
from option_pricing.binomial_tree import binomial_tree_price


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_black_scholes(option_type):
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    price = black_scholes_price(S, K, T, r, sigma, option_type)
    assert price > 0

def test_black_scholes_put_call_parity():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    call = black_scholes_price(S, K, T, r, sigma, "call")
    put = black_scholes_price(S, K, T, r, sigma, "put")
    expected_diff = S - K * math.exp(-r * T)
    assert abs(call - put - expected_diff) < 0.01

@pytest.mark.parametrize("option_type", ["call", "put"])
def test_monte_carlo(option_type):
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    price = monte_carlo_price(S, K, T, r, sigma, option_type, num_simulations=100000)
    assert price > 0

@pytest.mark.parametrize("option_type", ["call", "put"])
def test_binomial_tree(option_type):
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    price = binomial_tree_price(S, K, T, r, sigma, option_type, steps=100)
    assert price > 0

def test_model_consistency():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    bs = black_scholes_price(S, K, T, r, sigma, "call")
    mc = monte_carlo_price(S, K, T, r, sigma, "call", num_simulations=100000)
    bt = binomial_tree_price(S, K, T, r, sigma, "call", steps=100)

    assert abs(bs - mc) < 2.0
    assert abs(bs - bt) < 1.0


def test_black_scholes_invalid_inputs():
    with pytest.raises(ValueError):
        black_scholes_price(100, 100, 0, 0.05, 0.2, "call")
    with pytest.raises(ValueError):
        black_scholes_price(100, 100, 1, 0.05, -0.2, "call")
    with pytest.raises(ValueError):
        black_scholes_price(100, 100, 1, 0.05, 0.2, "invalid")


def test_monte_carlo_invalid_inputs():
    with pytest.raises(ValueError):
        monte_carlo_price(100, 100, 0, 0.05, 0.2, "call")
    with pytest.raises(ValueError):
        monte_carlo_price(100, 100, 1, 0.05, -0.2, "call")
    with pytest.raises(ValueError):
        monte_carlo_price(100, 100, 1, 0.05, 0.2, "invalid")


def test_binomial_tree_invalid_inputs():
    with pytest.raises(ValueError):
        binomial_tree_price(100, 100, 0, 0.05, 0.2, "call")
    with pytest.raises(ValueError):
        binomial_tree_price(100, 100, 1, 0.05, -0.2, "call")
    with pytest.raises(ValueError):
        binomial_tree_price(100, 100, 1, 0.05, 0.2, "invalid")
