from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_comparison(df: pd.DataFrame, output_path: str | Path) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(14, 7))
    plt.scatter(df["lastPrice"], df["bsm_valuation"], alpha=0.6, label="Black-Scholes")
    plt.scatter(df["lastPrice"], df["binomial_valuation"], alpha=0.6, label="Binomial")
    plt.plot([df["lastPrice"].min(), df["lastPrice"].max()], [df["lastPrice"].min(), df["lastPrice"].max()], color="green", linestyle="--")
    plt.xlabel("Market Price")
    plt.ylabel("Model Price")
    plt.title("Model Comparison vs. Observed Market Prices")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output, dpi=200)
    plt.close()


def plot_error_distribution(df: pd.DataFrame, output_path: str | Path) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.hist(df["abs_error_bs"], bins=20, alpha=0.6, label="Black-Scholes")
    plt.hist(df["abs_error_bin"], bins=20, alpha=0.6, label="Binomial")
    plt.xlabel("Absolute Error")
    plt.ylabel("Frequency")
    plt.title("Absolute Pricing Error Distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output, dpi=200)
    plt.close()
