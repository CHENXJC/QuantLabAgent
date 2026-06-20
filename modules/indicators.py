"""
Technical indicators module for QuantLab Agent.

This module calculates basic indicators used for quantitative research,
trend analysis, candlestick context, and risk observation.

Indicators included in the MVP:
- Daily return
- Cumulative return
- Moving averages
- Rolling volatility
- RSI
- Drawdown
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np
import pandas as pd


def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add daily return and cumulative return columns.
    """
    data = df.copy()

    if "Close" not in data.columns:
        raise ValueError("Close column is required to calculate returns.")

    data["daily_return"] = data["Close"].pct_change()
    data["cumulative_return"] = (1 + data["daily_return"].fillna(0)).cumprod() - 1

    return data


def add_moving_averages(
    df: pd.DataFrame,
    short_window: int = 20,
    long_window: int = 50,
) -> pd.DataFrame:
    """
    Add moving average columns.
    """
    data = df.copy()

    if "Close" not in data.columns:
        raise ValueError("Close column is required to calculate moving averages.")

    data[f"MA{short_window}"] = data["Close"].rolling(window=short_window).mean()
    data[f"MA{long_window}"] = data["Close"].rolling(window=long_window).mean()

    return data


def add_volatility(
    df: pd.DataFrame,
    window: int = 20,
    annualization_factor: int = 252,
) -> pd.DataFrame:
    """
    Add rolling annualized volatility.
    """
    data = df.copy()

    if "daily_return" not in data.columns:
        data = add_returns(data)

    data[f"volatility_{window}d"] = (
        data["daily_return"].rolling(window=window).std() * np.sqrt(annualization_factor)
    )

    return data


def add_rsi(
    df: pd.DataFrame,
    window: int = 14,
) -> pd.DataFrame:
    """
    Add Relative Strength Index.
    """
    data = df.copy()

    if "Close" not in data.columns:
        raise ValueError("Close column is required to calculate RSI.")

    delta = data["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    data[f"RSI{window}"] = 100 - (100 / (1 + rs))

    data[f"RSI{window}"] = data[f"RSI{window}"].fillna(50)

    return data


def add_drawdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add running peak and drawdown columns.
    """
    data = df.copy()

    if "Close" not in data.columns:
        raise ValueError("Close column is required to calculate drawdown.")

    data["running_peak"] = data["Close"].cummax()
    data["drawdown"] = data["Close"] / data["running_peak"] - 1

    return data


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add all MVP indicators to the market data DataFrame.
    """
    data = df.copy()

    data = add_returns(data)
    data = add_moving_averages(data, short_window=20, long_window=50)
    data = add_volatility(data, window=20)
    data = add_rsi(data, window=14)
    data = add_drawdown(data)

    return data


def classify_trend(row: pd.Series) -> str:
    """
    Classify trend based on MA20 and MA50.
    """
    ma20 = row.get("MA20")
    ma50 = row.get("MA50")
    close = row.get("Close")

    if pd.isna(ma20) or pd.isna(ma50) or pd.isna(close):
        return "Insufficient data"

    if close > ma20 > ma50:
        return "Bullish trend"
    if close < ma20 < ma50:
        return "Bearish trend"
    if ma20 > ma50:
        return "Positive but mixed"
    if ma20 < ma50:
        return "Weak but mixed"

    return "Neutral"


def classify_rsi(row: pd.Series) -> str:
    """
    Classify RSI condition.
    """
    rsi = row.get("RSI14")

    if pd.isna(rsi):
        return "Insufficient data"

    if rsi >= 70:
        return "Overbought"
    if rsi <= 30:
        return "Oversold"
    if rsi >= 55:
        return "Positive momentum"
    if rsi <= 45:
        return "Weak momentum"

    return "Neutral"


def get_latest_indicator_snapshot(df: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    Return the latest indicator snapshot.
    """
    if df.empty:
        raise ValueError("Cannot create indicator snapshot from empty DataFrame.")

    latest = df.iloc[-1]

    snapshot = {
        "ticker": latest.get("Ticker"),
        "date": str(latest.get("Date")),
        "close": round(float(latest["Close"]), 4) if pd.notna(latest.get("Close")) else None,
        "daily_return_pct": round(float(latest["daily_return"]) * 100, 4) if pd.notna(latest.get("daily_return")) else None,
        "cumulative_return_pct": round(float(latest["cumulative_return"]) * 100, 4) if pd.notna(latest.get("cumulative_return")) else None,
        "MA20": round(float(latest["MA20"]), 4) if pd.notna(latest.get("MA20")) else None,
        "MA50": round(float(latest["MA50"]), 4) if pd.notna(latest.get("MA50")) else None,
        "RSI14": round(float(latest["RSI14"]), 4) if pd.notna(latest.get("RSI14")) else None,
        "volatility_20d_pct": round(float(latest["volatility_20d"]) * 100, 4) if pd.notna(latest.get("volatility_20d")) else None,
        "drawdown_pct": round(float(latest["drawdown"]) * 100, 4) if pd.notna(latest.get("drawdown")) else None,
        "trend_status": classify_trend(latest),
        "rsi_status": classify_rsi(latest),
    }

    return snapshot


if __name__ == "__main__":
    from modules.data_loader import load_market_data

    test_df = load_market_data("SPY", period="6mo", interval="1d")
    indicator_df = add_all_indicators(test_df)
    print(indicator_df.tail())
    print(get_latest_indicator_snapshot(indicator_df))
