from __future__ import annotations

from datetime import datetime

import pandas as pd
import yfinance as yf


def _get_price_series(data: pd.DataFrame, label: str) -> pd.Series:
    if isinstance(data.columns, pd.MultiIndex):
        for column in data.columns:
            if isinstance(column, tuple):
                if len(column) == 2 and column[1] == label:
                    return data[column]
        for column in data.columns:
            if str(column).endswith(label):
                return data[column]

    if label in data.columns:
        return data[label]

    for candidate in data.columns:
        if str(candidate).lower() == label.lower():
            return data[candidate]

    raise KeyError(f"Column {label!r} not found in market data. Available columns: {list(data.columns)}")


def fetch_option_chain(ticker: str, expiry_date: str, option_type: str = "calls", valuation_date: str | None = None) -> pd.DataFrame:
    """Fetch one side of the option chain for a given expiry date."""
    if not ticker:
        raise ValueError("Ticker symbol cannot be empty.")

    option_type = str(option_type).strip().lower()
    if option_type not in {"calls", "puts"}:
        raise ValueError("option_type must be 'calls' or 'puts'.")

    market = yf.Ticker(ticker)
    options = market.options
    if not options:
        raise ValueError(f"No option contracts are available for {ticker!r}.")

    selected_expiry = expiry_date
    if expiry_date not in options:
        if valuation_date is None:
            valuation_date = datetime.today().strftime("%Y-%m-%d")
        valuation_dt = datetime.strptime(valuation_date, "%Y-%m-%d")
        available_dates = [datetime.strptime(item, "%Y-%m-%d") for item in options]
        selected_expiry = min(options, key=lambda item: abs((datetime.strptime(item, "%Y-%m-%d") - valuation_dt).days))

    chain = market.option_chain(selected_expiry)
    frame = getattr(chain, option_type).copy()
    frame = frame.drop(columns=[col for col in ["lastTradeDate", "openInterest", "contractSize", "currency"] if col in frame.columns], errors="ignore")
    return frame


def get_current_stock_price(ticker: str) -> float:
    data = yf.Ticker(ticker).history(period="1d")
    if data.empty:
        raise ValueError(f"No market data available for ticker {ticker!r}.")
    price_series = _get_price_series(data, "Close")
    return float(price_series.iloc[-1].item())


def get_10yr_treasury_rate() -> float:
    treasury_ticker = "^TNX"
    now = datetime.now()
    start = now.replace(year=now.year - 10)
    data = yf.download(treasury_ticker, start=start.strftime("%Y-%m-%d"), end=now.strftime("%Y-%m-%d"), progress=False)
    if data.empty:
        raise ValueError("Treasury yield data is unavailable.")
    close_series = _get_price_series(data, "Close")
    return float(close_series.iloc[-1].item())


def get_time_to_maturity(valuation_date: str, expiry_date: str) -> float:
    valuation = datetime.strptime(valuation_date, "%Y-%m-%d")
    expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
    delta_days = (expiry - valuation).days
    if delta_days <= 0:
        raise ValueError(f"Expiry date {expiry_date} must be after valuation date {valuation_date}.")
    return delta_days / 365.25


def estimate_volatility(ticker: str, lookback_years: int = 1) -> float:
    today = datetime.today()
    start = today.replace(year=today.year - lookback_years)
    data = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=today.strftime("%Y-%m-%d"), progress=False)
    if data.empty:
        raise ValueError(f"Cannot estimate volatility for ticker {ticker!r}.")

    close_series = _get_price_series(data, "Adj Close") if "Adj Close" in data.columns or any("Adj Close" in str(col) for col in data.columns) else _get_price_series(data, "Close")
    returns = close_series.pct_change().dropna()
    if returns.empty:
        raise ValueError(f"No return data available for ticker {ticker!r}.")

    vol_std = returns.std()
    if isinstance(vol_std, pd.Series):
        vol_std = vol_std.iloc[0]
    daily_vol = float(vol_std)
    return float(daily_vol * (252 ** 0.5))
