from __future__ import annotations

import argparse
from pathlib import Path

from finsearch.config import PricingConfig
from finsearch.plotting.charts import plot_comparison, plot_error_distribution
from finsearch.pricing.engine import evaluate_option_chain
from finsearch.strategy import rank_trade_candidates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare Black-Scholes and binomial option prices for a given option chain.")
    parser.add_argument("--ticker", default="AAPL", help="Ticker symbol to analyze.")
    parser.add_argument("--date", default="2024-09-20", help="Option expiry date in YYYY-MM-DD format.")
    parser.add_argument("--valuation-date", default=None, help="Optional valuation date in YYYY-MM-DD format; defaults to today.")
    parser.add_argument("--steps", type=int, default=200, help="Number of binomial steps.")
    parser.add_argument("--exercise-style", choices=("european", "american"), default="european")
    parser.add_argument("--option-type", choices=("calls", "puts"), default="calls")
    parser.add_argument("--output-dir", default="results", help="Directory used to save output artifacts.")
    parser.add_argument("--no-plot", action="store_true", help="Skip plot generation.")
    parser.add_argument("--strategy", action="store_true", help="Generate a ranked option mispricing strategy summary.")
    parser.add_argument("--strategy-threshold", type=float, default=0.05, help="Relative mispricing threshold for trade signals.")
    parser.add_argument("--strategy-top-n", type=int, default=10, help="Maximum number of ranked trade candidates to keep.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = PricingConfig(
        ticker=args.ticker,
        expiry_date=args.date,
        valuation_date=args.valuation_date,
        steps=args.steps,
        exercise_style=args.exercise_style,
        output_dir=args.output_dir,
    )

    df = evaluate_option_chain(
        ticker=config.ticker,
        expiry_date=config.expiry_date,
        valuation_date=config.valuation_date,
        steps=config.steps,
        option_type=args.option_type,
        exercise_style=config.exercise_style,
    )

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "option_chain_evaluation.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved evaluation data to {csv_path}")

    if not args.no_plot:
        plot_path = output_dir / "model_comparison.png"
        error_path = output_dir / "error_distribution.png"
        plot_comparison(df, plot_path)
        plot_error_distribution(df, error_path)
        print(f"Saved comparison plot to {plot_path}")
        print(f"Saved error plot to {error_path}")

    mean_abs_err_bs = df["abs_error_bs"].mean()
    mean_abs_err_bin = df["abs_error_bin"].mean()
    print(f"Mean absolute error (Black-Scholes): {mean_abs_err_bs:.4f}")
    print(f"Mean absolute error (Binomial): {mean_abs_err_bin:.4f}")

    if args.strategy:
        signals = rank_trade_candidates(
            df,
            top_n=args.strategy_top_n,
            threshold=args.strategy_threshold,
        )
        strategy_path = output_dir / "trade_candidates.csv"
        signals.to_csv(strategy_path, index=False)
        print(f"Saved ranked trade candidates to {strategy_path}")
        print(signals[["signal", "trade", "relative_gap", "confidence", "model_agreement", "lastPrice", "model_midpoint"]].head(args.strategy_top_n).to_string(index=False))


if __name__ == "__main__":
    main()
