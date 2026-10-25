from __future__ import annotations

import math
from typing import Literal


OptionType = Literal["call", "put", "C", "P"]


def _normalize_option_type(option_type: str) -> str:
    normalized = str(option_type).strip().lower()
    if normalized in {"call", "c"}:
        return "call"
    if normalized in {"put", "p"}:
        return "put"
    raise ValueError(f"Unsupported option type: {option_type!r}. Use 'call' or 'put'.")


def d1(s: float, k: float, t: float, r: float, sigma: float) -> float:
    if s <= 0 or k <= 0:
        raise ValueError("Underlying price and strike must be positive.")
    if t <= 0:
        raise ValueError("Time to maturity must be positive.")
    if sigma <= 0:
        raise ValueError("Volatility must be positive.")
    return (math.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))


def d2(s: float, k: float, t: float, r: float, sigma: float) -> float:
    return d1(s, k, t, r, sigma) - sigma * math.sqrt(t)


def black_scholes_price(
    s: float,
    k: float,
    t: float,
    r: float,
    sigma: float,
    option_type: OptionType = "call",
) -> float:
    """Return the Black-Scholes price for a European option."""
    option_kind = _normalize_option_type(option_type)

    if s <= 0 or k <= 0:
        raise ValueError("Underlying price and strike must be positive.")
    if t <= 0:
        raise ValueError("Time to maturity must be positive.")
    if sigma <= 0:
        raise ValueError("Volatility must be positive.")

    if option_kind == "call":
        return s * _normal_cdf(d1(s, k, t, r, sigma)) - k * math.exp(-r * t) * _normal_cdf(d2(s, k, t, r, sigma))

    return k * math.exp(-r * t) * _normal_cdf(-d2(s, k, t, r, sigma)) - s * _normal_cdf(-d1(s, k, t, r, sigma))


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
