from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


_DEFAULT_OUTPUT_DIR = Path("results")


@dataclass(frozen=True)
class PricingConfig:
    ticker: str = "AAPL"
    expiry_date: str = "2024-09-20"
    valuation_date: str | None = None
    risk_free_rate: float | None = None
    volatility: float | None = None
    steps: int = 200
    exercise_style: str = "european"
    output_dir: str = str(_DEFAULT_OUTPUT_DIR)

    def __post_init__(self) -> None:
        if not self.ticker:
            raise ValueError("Ticker symbol cannot be empty.")
        if self.steps <= 0:
            raise ValueError("Number of binomial steps must be positive.")

        if self.valuation_date is None:
            object.__setattr__(self, "valuation_date", datetime.today().strftime("%Y-%m-%d"))

        exercise_style = self.exercise_style.lower()
        if exercise_style not in {"european", "american"}:
            raise ValueError("exercise_style must be 'european' or 'american'.")
        object.__setattr__(self, "exercise_style", exercise_style)
