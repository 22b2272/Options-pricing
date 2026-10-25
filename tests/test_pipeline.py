import pandas as pd

from finsearch.pricing.engine import evaluate_option_chain


def test_evaluate_option_chain_returns_expected_columns():
    df = evaluate_option_chain(
        ticker="AAPL",
        expiry_date="2025-09-19",
        valuation_date="2025-01-01",
        steps=50,
        option_type="calls",
    )

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert {"strike", "lastPrice", "bsm_valuation", "binomial_valuation", "abs_error_bs", "abs_error_bin"}.issubset(df.columns)
    assert (df["bsm_valuation"].notna()).all()
    assert (df["binomial_valuation"].notna()).all()
