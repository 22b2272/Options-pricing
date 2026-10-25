import pandas as pd

from finsearch.strategy import generate_trade_signals


def test_generate_trade_signals_marks_underpriced_and_overpriced_contracts():
    df = pd.DataFrame(
        {
            "lastPrice": [100.0, 140.0],
            "bsm_valuation": [110.0, 120.0],
            "binomial_valuation": [108.0, 118.0],
        }
    )

    signals = generate_trade_signals(df, threshold=0.05)

    assert list(signals["signal"]) == [1, -1]
    assert (signals["confidence"] >= 0).all()
