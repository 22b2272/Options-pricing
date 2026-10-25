import math

import numpy as np

from finsearch.models.black_scholes import black_scholes_price
from finsearch.models.binomial import crr_option_price


def test_black_scholes_call_price_matches_reference():
    s = 100.0
    k = 100.0
    t = 1.0
    r = 0.05
    sigma = 0.2

    price = black_scholes_price(s, k, t, r, sigma, option_type="call")

    expected = 10.450583
    assert abs(price - expected) < 1e-3


def test_black_scholes_put_price_matches_reference():
    s = 100.0
    k = 100.0
    t = 1.0
    r = 0.05
    sigma = 0.2

    price = black_scholes_price(s, k, t, r, sigma, option_type="put")

    expected = 5.573526
    assert abs(price - expected) < 1e-3


def test_binomial_call_close_to_black_scholes():
    s = 100.0
    k = 100.0
    t = 1.0
    r = 0.05
    sigma = 0.2

    bs_price = black_scholes_price(s, k, t, r, sigma, option_type="call")
    bin_price = crr_option_price(s, k, t, r, sigma, option_type="call", steps=2000)

    assert abs(bin_price - bs_price) < 0.05


def test_binomial_put_close_to_black_scholes():
    s = 100.0
    k = 100.0
    t = 1.0
    r = 0.05
    sigma = 0.2

    bs_price = black_scholes_price(s, k, t, r, sigma, option_type="put")
    bin_price = crr_option_price(s, k, t, r, sigma, option_type="put", steps=2000)

    assert abs(bin_price - bs_price) < 0.05


def test_option_type_validation():
    try:
        black_scholes_price(100, 100, 1, 0.05, 0.2, option_type="invalid")
        raise AssertionError("Expected ValueError for invalid option type")
    except ValueError:
        pass

    try:
        crr_option_price(100, 100, 1, 0.05, 0.2, option_type="invalid", steps=50)
        raise AssertionError("Expected ValueError for invalid option type")
    except ValueError:
        pass
