"""
Backtesting module for QuantLab Agent.

This module runs simple research-oriented strategy backtests.

Important:
- Backtests are historical simulations only.
- Results do not guarantee future performance.
- No real trades are executed.
"""

from __future__ import annotations

import pandas as pd


def run_ma_crossover_backtest(
    df: pd.DataFrame,
    initial_capital: float = 10000.0,
    fee_rate: float = 0.0,
) -> pd.DataFrame:
    """
    Run a simple MA crossover backtest.

    Assumption:
    - When ma_position is 1, the strategy holds the asset.
    - When ma_position is 0, the strategy stays in cash.
    - Signal is shifted by 1 day to avoid look-ahead bias.
    """
    data = df.copy()

    required_columns = ["Close", "daily_return", "ma_position"]
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns for backtest: {missing}")

    data["strategy_position"] = data["ma_position"].shift(1).fillna(0)

    data["strategy_return"] = data["strategy_position"] * data["daily_return"]
    data["buy_hold_return"] = data["daily_return"]

    data["strategy_equity"] = initial_capital * (1 + data["strategy_return"].fillna(0)).cumprod()
    data["buy_hold_equity"] = initial_capital * (1 + data["buy_hold_return"].fillna(0)).cumprod()

    data["strategy_running_peak"] = data["strategy_equity"].cummax()
    data["strategy_drawdown"] = data["strategy_equity"] / data["strategy_running_peak"] - 1

    data["buy_hold_running_peak"] = data["buy_hold_equity"].cummax()
    data["buy_hold_drawdown"] = data["buy_hold_equity"] / data["buy_hold_running_peak"] - 1

    return data


def generate_trade_log(
    df: pd.DataFrame,
    initial_capital: float = 10000.0,
) -> pd.DataFrame:
    """
    Generate a simple simulated trade log based on BUY and SELL signals.

    This is paper-trading style output and does not represent real execution.
    """
    data = df.copy()

    required_columns = ["Date", "Close", "ma_signal"]
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns for trade log: {missing}")

    cash = initial_capital
    shares = 0.0
    trades = []

    for _, row in data.iterrows():
        signal = row["ma_signal"]
        price = float(row["Close"])

        if signal == "BUY" and cash > 0 and price > 0:
            shares = cash / price
            cash = 0.0
            action = "BUY"

        elif signal == "SELL" and shares > 0:
            cash = shares * price
            shares = 0.0
            action = "SELL"

        else:
            continue

        portfolio_value = cash + shares * price

        trades.append(
            {
                "Date": row["Date"],
                "Ticker": row.get("Ticker"),
                "Action": action,
                "Price": round(price, 4),
                "Shares": round(shares, 6),
                "Cash": round(cash, 2),
                "Portfolio Value": round(portfolio_value, 2),
            }
        )

    return pd.DataFrame(trades)


def get_backtest_summary(df: pd.DataFrame) -> dict:
    """
    Return a simple backtest summary.
    """
    if df.empty:
        raise ValueError("Cannot summarize empty backtest DataFrame.")

    first = df.iloc[0]
    latest = df.iloc[-1]

    strategy_start = float(first["strategy_equity"])
    strategy_end = float(latest["strategy_equity"])
    buy_hold_start = float(first["buy_hold_equity"])
    buy_hold_end = float(latest["buy_hold_equity"])

    strategy_return_pct = (strategy_end / strategy_start - 1) * 100
    buy_hold_return_pct = (buy_hold_end / buy_hold_start - 1) * 100

    strategy_max_drawdown_pct = float(df["strategy_drawdown"].min()) * 100
    buy_hold_max_drawdown_pct = float(df["buy_hold_drawdown"].min()) * 100

    return {
        "ticker": latest.get("Ticker"),
        "start_date": str(first.get("Date")),
        "end_date": str(latest.get("Date")),
        "strategy_final_equity": round(strategy_end, 2),
        "buy_hold_final_equity": round(buy_hold_end, 2),
        "strategy_return_pct": round(strategy_return_pct, 4),
        "buy_hold_return_pct": round(buy_hold_return_pct, 4),
        "strategy_max_drawdown_pct": round(strategy_max_drawdown_pct, 4),
        "buy_hold_max_drawdown_pct": round(buy_hold_max_drawdown_pct, 4),
        "outperformance_pct": round(strategy_return_pct - buy_hold_return_pct, 4),
    }
