# Finsearch-24: Options Pricing Models

An educational project comparing **Black–Scholes** and **Cox–Ross–Rubinstein (CRR) binomial-tree** valuations for equity options. It includes a Python package for live option-chain analysis, plotting, and a simple model-based mispricing screen, alongside the original Finsearch 2024 scripts, notebook, data, and reports.

> This is a learning and research project, not investment advice. Model estimates and historical option prices are not trading recommendations.

## What it does

- Prices European calls and puts with the Black–Scholes model.
- Prices European or American calls and puts with a CRR binomial tree.
- Retrieves a selected option chain and market inputs using `yfinance`.
- Compares model valuations with the chain's last-traded prices and saves the results.
- Optionally plots the comparisons and ranks contracts by a simple relative-price-gap signal.

The workflow uses the latest available underlying close, annualized volatility estimated from historical daily returns, and the latest available 10-year Treasury yield as the risk-free rate unless model inputs are supplied directly to the pricing API. The strategy is a simplified model comparison; it does not account for transaction costs, liquidity, dividends, or execution.

## Install

Requires Python 3.9 or later and an internet connection for live market data.

```bash
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install the package and its dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

## Run an analysis

Choose an expiration date that is **in the future and listed for the ticker**. For example:

```bash
python scripts/run_analysis.py --ticker AAPL --date 2026-12-18
```

The example date may not be listed when you run the command; replace it with an expiration available for your ticker. The command-line tool defaults to `AAPL`, calls, European exercise, 200 binomial steps, and the `results/` output directory.

To see all options:

```bash
python scripts/run_analysis.py --help
```

Useful options:

| Option | Description |
| --- | --- |
| `--ticker` | Underlying ticker symbol. |
| `--date` | Option expiration in `YYYY-MM-DD` format; choose a future listed expiration. |
| `--valuation-date` | Valuation date in `YYYY-MM-DD` format; defaults to today. |
| `--option-type` | Option-chain side: `calls` or `puts`. |
| `--exercise-style` | Binomial exercise style: `european` or `american`. |
| `--steps` | Number of CRR tree steps. |
| `--output-dir` | Directory for generated files; defaults to `results/`. |
| `--no-plot` | Save the evaluation CSV without generating plots. |
| `--strategy` | Also save ranked candidates based on model-versus-market price gaps. |
| `--strategy-threshold` | Minimum absolute relative price gap for a buy/sell signal; defaults to `0.05`. |
| `--strategy-top-n` | Maximum number of ranked candidates; defaults to `10`. |

For example, analyze puts with an American-style binomial tree and include the strategy output:

```bash
python scripts/run_analysis.py --ticker AAPL --date 2026-12-18 --option-type puts --exercise-style american --strategy
```

The valuation date and expiration must result in positive time to maturity. The expiration should also match a date offered by the data provider; use a date listed for the selected ticker.

## Output files

By default, the tool writes to `results/`:

- `option_chain_evaluation.csv` — option-chain rows with Black–Scholes and binomial valuations and absolute differences from `lastPrice`.
- `model_comparison.png` and `error_distribution.png` — plots, unless `--no-plot` is supplied.
- `trade_candidates.csv` — ranked signals, when `--strategy` is enabled.

Generated output directories are ignored by Git.

## Run the tests

```bash
python -m pip install pytest
python -m pytest
```

The pricing and strategy tests use local inputs. The option-chain pipeline test calls live market data and currently has a fixed expiration date; update it to a future listed expiration before expecting that test to pass.

## Project layout

```text
.
├── src/finsearch/
│   ├── data/          # Market data retrieval and input estimates
│   ├── models/        # Black–Scholes and CRR pricing models
│   ├── pricing/       # Option-chain valuation and comparison
│   ├── plotting/      # Comparison and error charts
│   ├── cli.py         # Command-line interface
│   └── strategy.py    # Relative-gap signals and ranking
├── scripts/
│   └── run_analysis.py
├── tests/             # Pricing, strategy, and pipeline tests
├── legacy/            # Legacy-artifact notes
├── BSvsBinomial.ipynb # Exploratory notebook
├── bsvsbinomial.py    # Original comparison script
├── finsearch_final.py # Original analysis script
├── option-chain-ED-NIFTY-22-Aug-2024 (1).csv
└── Finsearch_2024_*.pdf
```

The reproducible analysis workflow lives in `src/finsearch/`. The root-level scripts, notebook, CSV, and PDFs are retained as original project materials.

## Models and interpretation

- **Black–Scholes** provides a closed-form European option valuation.
- **CRR binomial tree** supports European and American exercise; increase `--steps` for a finer tree at the cost of more computation.
- The reported absolute differences compare each model value with the option chain's `lastPrice`. They are descriptive comparisons, not proof of predictive accuracy.
- The optional strategy uses the mean of the two model valuations, compares it with `lastPrice`, and emits a signal when the relative gap passes the configured threshold. It is an educational example, not a complete trading system.

## Project background

Created for Finsearch 2024 by Finance Club, IIT Bombay. Team E21: Mahak Sahu, Nandnee Priya, Shrushti Visave, and Shreya Singal.
