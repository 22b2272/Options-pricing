from __future__ import annotations

from datetime import datetime

import pandas as pd

from finsearch.data.market_data import estimate_volatility, fetch_option_chain, get_10yr_treasury_rate, get_current_stock_price, get_time_to_maturity
from finsearch.models.black_scholes import black_scholes_price
from finsearch.models.binomial import crr_option_price


def evaluate_option_chain(
    ticker: str,
    expiry_date: str,
    valuation_date: str | None = None,
    risk_free_rate: float | None = None,
    volatility: float | None = None,
    steps: int = 200,
    option_type: str = "calls",
    exercise_style: str = "european",
) -> pd.DataFrame:
    """Price each option in a chain using both models and return comparison metrics."""
    if valuation_date is None:
        valuation_date = datetime.today().strftime("%Y-%m-%d")

    if risk_free_rate is None:
        risk_free_rate = get_10yr_treasury_rate() / 100.0
    if volatility is None:
        volatility = estimate_volatility(ticker)

    stock_price = get_current_stock_price(ticker)
    time_to_maturity = get_time_to_maturity(valuation_date, expiry_date)

    chain = fetch_option_chain(ticker, expiry_date, option_type, valuation_date=valuation_date)
    if chain.empty:
        raise ValueError(f"No option chain data returned for {ticker} on {expiry_date}.")

    df = chain.copy()
    df["time_to_maturity"] = time_to_maturity
    df["stock_price"] = stock_price
    df["risk_free_rate"] = risk_free_rate
    df["volatility"] = volatility
    df["bsm_valuation"] = df["strike"].apply(lambda strike: black_scholes_price(stock_price, strike, time_to_maturity, risk_free_rate, volatility, option_type="call" if option_type == "calls" else "put"))
    df["binomial_valuation"] = df["strike"].apply(lambda strike: crr_option_price(stock_price, strike, time_to_maturity, risk_free_rate, volatility, option_type="call" if option_type == "calls" else "put", steps=steps, exercise_style=exercise_style))
    df["abs_error_bs"] = (df["lastPrice"] - df["bsm_valuation"]).abs()
    df["abs_error_bin"] = (df["lastPrice"] - df["binomial_valuation"]).abs()
    return df
