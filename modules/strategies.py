"""
Strategy module for QuantLab Agent.

This module generates research-oriented trading signals.

Important:
- Signals are for educational research and backtesting only.
- They are not financial advice.
- They do not trigger real trades.
"""

from __future__ import annotations

import pandas as pd


def generate_ma_crossover_signals(
    df: pd.DataFrame,
    short_ma: str = "MA20",
    long_ma: str = "MA50",
) -> pd.DataFrame:
    """
    Generate moving average crossover signals.

    Signal logic:
    - 1 means risk-on / simulated long position
    - 0 means cash / no position
    - Buy signal happens when position changes from 0 to 1
    - Sell signal happens when position changes from 1 to 0
    """
    data = df.copy()

    required_columns = ["Close", short_ma, long_ma]
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns for MA strategy: {missing}")

    data["ma_position"] = 0
    data.loc[data[short_ma] > data[long_ma], "ma_position"] = 1

    data["ma_position"] = data["ma_position"].fillna(0)
    data["ma_signal_change"] = data["ma_position"].diff().fillna(0)

    data["ma_signal"] = "HOLD"
    data.loc[data["ma_signal_change"] == 1, "ma_signal"] = "BUY"
    data.loc[data["ma_signal_change"] == -1, "ma_signal"] = "SELL"

    return data


def get_latest_strategy_signal(df: pd.DataFrame) -> dict:
    """
    Return the latest strategy signal summary.
    """
    if df.empty:
        raise ValueError("Cannot create strategy signal from empty DataFrame.")

    latest = df.iloc[-1]

    signal = latest.get("ma_signal", "HOLD")
    position = int(latest.get("ma_position", 0))

    ma20 = latest.get("MA20")
    ma50 = latest.get("MA50")
    close = latest.get("Close")

    if position == 1:
        position_status = "Simulated risk-on"
    else:
        position_status = "Simulated cash / defensive"

    if pd.notna(ma20) and pd.notna(ma50):
        if ma20 > ma50:
            reason = "MA20 is above MA50, indicating positive trend structure."
        elif ma20 < ma50:
            reason = "MA20 is below MA50, indicating weak trend structure."
        else:
            reason = "MA20 and MA50 are close, indicating neutral trend structure."
    else:
        reason = "Insufficient moving average data."

    return {
        "ticker": latest.get("Ticker"),
        "date": str(latest.get("Date")),
        "close": round(float(close), 4) if pd.notna(close) else None,
        "signal": signal,
        "position": position,
        "position_status": position_status,
        "reason": reason,
    }
