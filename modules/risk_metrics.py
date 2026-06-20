"""
Risk metrics module for QuantLab Agent.

This module calculates portfolio and strategy risk metrics for research-oriented
backtesting analysis.

Important:
- Metrics are based on historical data only.
- They do not predict future returns.
- They are not financial advice.
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np
import pandas as pd


def calculate_total_return(equity: pd.Series) -> float:
    """
    Calculate total return from an equity curve.
    """
    clean = equity.dropna()

    if len(clean) < 2:
        return 0.0

    start = float(clean.iloc[0])
    end = float(clean.iloc[-1])

    if start == 0:
        return 0.0

    return end / start - 1


def calculate_annualized_return(equity: pd.Series, periods_per_year: int = 252) -> float:
    """
    Calculate annualized return from an equity curve.
    """
    clean = equity.dropna()

    if len(clean) < 2:
        return 0.0

    total_return = calculate_total_return(clean)
    periods = len(clean)

    if periods <= 1:
        return 0.0

    return (1 + total_return) ** (periods_per_year / periods) - 1


def calculate_annualized_volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    """
    Calculate annualized volatility from periodic returns.
    """
    clean = returns.dropna()

    if len(clean) < 2:
        return 0.0

    return float(clean.std() * np.sqrt(periods_per_year))


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Calculate Sharpe ratio.

    risk_free_rate is annualized.
    """
    clean = returns.dropna()

    if len(clean) < 2:
        return 0.0

    periodic_risk_free = risk_free_rate / periods_per_year
    excess_returns = clean - periodic_risk_free

    volatility = clean.std()

    if volatility == 0 or pd.isna(volatility):
        return 0.0

    return float(excess_returns.mean() / volatility * np.sqrt(periods_per_year))


def calculate_max_drawdown(equity: pd.Series) -> float:
    """
    Calculate maximum drawdown from an equity curve.
    """
    clean = equity.dropna()

    if len(clean) < 2:
        return 0.0

    running_peak = clean.cummax()
    drawdown = clean / running_peak - 1

    return float(drawdown.min())


def calculate_calmar_ratio(equity: pd.Series, periods_per_year: int = 252) -> float:
    """
    Calculate Calmar ratio.

    Calmar Ratio = Annualized Return / Absolute Maximum Drawdown
    """
    annualized_return = calculate_annualized_return(equity, periods_per_year)
    max_drawdown = calculate_max_drawdown(equity)

    if max_drawdown == 0:
        return 0.0

    return float(annualized_return / abs(max_drawdown))


def calculate_win_rate(returns: pd.Series) -> float:
    """
    Calculate win rate based on positive return periods.
    """
    clean = returns.dropna()

    if len(clean) == 0:
        return 0.0

    return float((clean > 0).sum() / len(clean))


def classify_risk_level(
    max_drawdown: float,
    volatility: float,
) -> str:
    """
    Classify risk level using drawdown and volatility.
    """
    max_drawdown_abs = abs(max_drawdown)

    if max_drawdown_abs >= 0.30 or volatility >= 0.50:
        return "Very High"
    if max_drawdown_abs >= 0.20 or volatility >= 0.35:
        return "High"
    if max_drawdown_abs >= 0.10 or volatility >= 0.20:
        return "Medium"
    return "Low"


def calculate_strategy_metrics(
    df: pd.DataFrame,
    equity_col: str,
    return_col: str,
    label: str,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> Dict[str, Optional[float]]:
    """
    Calculate a complete metric set for one strategy or benchmark.
    """
    if equity_col not in df.columns:
        raise ValueError(f"Missing equity column: {equity_col}")

    if return_col not in df.columns:
        raise ValueError(f"Missing return column: {return_col}")

    equity = df[equity_col]
    returns = df[return_col]

    total_return = calculate_total_return(equity)
    annualized_return = calculate_annualized_return(equity, periods_per_year)
    annualized_volatility = calculate_annualized_volatility(returns, periods_per_year)
    sharpe_ratio = calculate_sharpe_ratio(returns, risk_free_rate, periods_per_year)
    max_drawdown = calculate_max_drawdown(equity)
    calmar_ratio = calculate_calmar_ratio(equity, periods_per_year)
    win_rate = calculate_win_rate(returns)

    return {
        "label": label,
        "total_return_pct": round(total_return * 100, 4),
        "annualized_return_pct": round(annualized_return * 100, 4),
        "annualized_volatility_pct": round(annualized_volatility * 100, 4),
        "sharpe_ratio": round(sharpe_ratio, 4),
        "max_drawdown_pct": round(max_drawdown * 100, 4),
        "calmar_ratio": round(calmar_ratio, 4),
        "win_rate_pct": round(win_rate * 100, 4),
        "risk_level": classify_risk_level(max_drawdown, annualized_volatility),
    }


def compare_strategy_vs_benchmark(
    df: pd.DataFrame,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> pd.DataFrame:
    """
    Compare strategy metrics against Buy and Hold benchmark.
    """
    strategy_metrics = calculate_strategy_metrics(
        df=df,
        equity_col="strategy_equity",
        return_col="strategy_return",
        label="MA Crossover Strategy",
        risk_free_rate=risk_free_rate,
        periods_per_year=periods_per_year,
    )

    benchmark_metrics = calculate_strategy_metrics(
        df=df,
        equity_col="buy_hold_equity",
        return_col="buy_hold_return",
        label="Buy and Hold",
        risk_free_rate=risk_free_rate,
        periods_per_year=periods_per_year,
    )

    comparison = pd.DataFrame([strategy_metrics, benchmark_metrics])

    return comparison


def generate_risk_commentary(comparison_df: pd.DataFrame) -> str:
    """
    Generate a simple rule-based risk commentary.
    """
    if comparison_df.empty or len(comparison_df) < 2:
        return "Insufficient data to generate risk commentary."

    strategy = comparison_df.iloc[0]
    benchmark = comparison_df.iloc[1]

    strategy_return = strategy["total_return_pct"]
    benchmark_return = benchmark["total_return_pct"]

    strategy_drawdown = strategy["max_drawdown_pct"]
    benchmark_drawdown = benchmark["max_drawdown_pct"]

    strategy_sharpe = strategy["sharpe_ratio"]
    benchmark_sharpe = benchmark["sharpe_ratio"]

    comments = []

    if strategy_return > benchmark_return:
        comments.append("The strategy outperformed the Buy and Hold benchmark on total return.")
    else:
        comments.append("The strategy underperformed the Buy and Hold benchmark on total return.")

    if abs(strategy_drawdown) < abs(benchmark_drawdown):
        comments.append("The strategy showed lower maximum drawdown than the benchmark.")
    else:
        comments.append("The strategy showed higher or similar drawdown risk compared with the benchmark.")

    if strategy_sharpe > benchmark_sharpe:
        comments.append("The strategy achieved a better risk-adjusted return based on Sharpe ratio.")
    else:
        comments.append("The strategy did not improve risk-adjusted return based on Sharpe ratio.")

    comments.append("These results are historical simulations only and do not guarantee future performance.")

    return " ".join(comments)
