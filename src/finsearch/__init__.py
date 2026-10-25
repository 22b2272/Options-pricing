"""Quantitative finance option-pricing utilities."""

from .models.black_scholes import black_scholes_price
from .models.binomial import crr_option_price
from .strategy import generate_trade_signals, rank_trade_candidates

__all__ = ["black_scholes_price", "crr_option_price", "generate_trade_signals", "rank_trade_candidates"]
