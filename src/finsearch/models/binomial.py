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


def crr_option_price(
    s: float,
    k: float,
    t: float,
    r: float,
    sigma: float,
    option_type: OptionType = "call",
    steps: int = 100,
    exercise_style: str = "european",
) -> float:
    """Price a European or American option with a Cox-Ross-Rubinstein tree."""
    option_kind = _normalize_option_type(option_type)
    if steps <= 0:
        raise ValueError("Number of binomial steps must be positive.")
    if s <= 0 or k <= 0:
        raise ValueError("Underlying price and strike must be positive.")
    if t <= 0:
        raise ValueError("Time to maturity must be positive.")
    if sigma <= 0:
        raise ValueError("Volatility must be positive.")

    exercise_style = str(exercise_style).lower()
    if exercise_style not in {"european", "american"}:
        raise ValueError("exercise_style must be 'european' or 'american'.")

    dt = t / steps
    u = math.exp(sigma * math.sqrt(dt))
    d = math.exp(-sigma * math.sqrt(dt))
    p_up = (math.exp(r * dt) - d) / (u - d)
    discount = math.exp(-r * dt)

    if not 0.0 <= p_up <= 1.0:
        raise ValueError("CRR risk-neutral probability is invalid; check inputs for r, sigma, and dt.")

    payoffs = [0.0] * (steps + 1)
    for j in range(steps + 1):
        stock_value = s * (u ** j) * (d ** (steps - j))
        if option_kind == "call":
            payoffs[j] = max(stock_value - k, 0.0)
        else:
            payoffs[j] = max(k - stock_value, 0.0)

    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            continuation = discount * (p_up * payoffs[j + 1] + (1 - p_up) * payoffs[j])
            if exercise_style == "american":
                stock_value = s * (u ** j) * (d ** (i - j))
                intrinsic = max(stock_value - k, 0.0) if option_kind == "call" else max(k - stock_value, 0.0)
                payoffs[j] = max(continuation, intrinsic)
            else:
                payoffs[j] = continuation

    return payoffs[0]
