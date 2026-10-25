from __future__ import annotations

import pandas as pd


def generate_trade_signals(
    df: pd.DataFrame,
    threshold: float = 0.05,
    min_confidence: float = 0.0,
    min_model_agreement: float = 0.0,
) -> pd.DataFrame:
    """Generate a simple relative-mispricing signal using the same option-pricing models.

    The strategy compares the average of Black-Scholes and binomial valuations with
    the observed market price. A signal is only emitted when the relative gap exceeds
    the threshold and the two model estimates are sufficiently aligned.
    """
    required = {"lastPrice", "bsm_valuation", "binomial_valuation"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {sorted(missing)}")

    result = df.copy().copy()
    result["model_midpoint"] = (result["bsm_valuation"] + result["binomial_valuation"]) / 2.0

    price_denominator = result["lastPrice"].replace(0, pd.NA)
    result["relative_gap"] = (result["model_midpoint"] - result["lastPrice"]) / price_denominator
    result["relative_gap"] = result["relative_gap"].fillna(0.0)

    model_spread = (result["bsm_valuation"] - result["binomial_valuation"]).abs()
    model_scale = (result["bsm_valuation"].abs() + result["binomial_valuation"].abs()).replace(0, 1e-9)
    result["model_agreement"] = 1.0 - (model_spread / model_scale)
    result["model_agreement"] = result["model_agreement"].clip(lower=0.0, upper=1.0)

    result["confidence"] = result["relative_gap"].abs() * result["model_agreement"]

    signals = pd.Series(0, index=result.index, dtype=int)
    buy_mask = (result["relative_gap"] > threshold) & (result["model_agreement"] >= min_model_agreement)
    sell_mask = (result["relative_gap"] < -threshold) & (result["model_agreement"] >= min_model_agreement)
    signals[buy_mask] = 1
    signals[sell_mask] = -1
    result["signal"] = signals

    result["trade"] = result["signal"].map({-1: "sell", 0: "hold", 1: "buy"})
    result["rank_score"] = result["confidence"]

    if min_confidence > 0:
        result = result[result["confidence"] >= min_confidence].copy()

    return result


def rank_trade_candidates(
    df: pd.DataFrame,
    top_n: int = 10,
    threshold: float = 0.05,
    min_confidence: float = 0.0,
    min_model_agreement: float = 0.0,
) -> pd.DataFrame:
    """Return the highest-conviction opportunities from the strategy output."""
    ranked = generate_trade_signals(
        df,
        threshold=threshold,
        min_confidence=min_confidence,
        min_model_agreement=min_model_agreement,
    )
    ranked = ranked[ranked["signal"] != 0].copy()
    ranked = ranked.sort_values(["rank_score", "relative_gap"], ascending=[False, False]).head(top_n).copy()
    return ranked
