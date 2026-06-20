"""
Candlestick analysis module for QuantLab Agent.

This module provides simple candlestick observations for research summaries.

Current MVP:
- Candle body direction
- Body size
- Upper shadow
- Lower shadow
- Simple price action commentary

Important:
- Candlestick observations are not trading advice.
- Candlestick patterns should be validated with trend, volume, indicators, and risk metrics.
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


def analyze_latest_candle(df: pd.DataFrame) -> Dict[str, object]:
    """
    Analyze the latest candlestick structure.
    """
    if df.empty:
        raise ValueError("Cannot analyze candlestick from empty DataFrame.")

    required_columns = ["Date", "Open", "High", "Low", "Close"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for candlestick analysis: {missing}")

    latest = df.iloc[-1]

    open_price = float(latest["Open"])
    high_price = float(latest["High"])
    low_price = float(latest["Low"])
    close_price = float(latest["Close"])

    candle_range = high_price - low_price
    body_size = abs(close_price - open_price)

    if candle_range == 0:
        body_ratio = 0.0
        upper_shadow_ratio = 0.0
        lower_shadow_ratio = 0.0
    else:
        body_ratio = body_size / candle_range
        upper_shadow = high_price - max(open_price, close_price)
        lower_shadow = min(open_price, close_price) - low_price
        upper_shadow_ratio = upper_shadow / candle_range
        lower_shadow_ratio = lower_shadow / candle_range

    if close_price > open_price:
        direction = "Bullish candle"
    elif close_price < open_price:
        direction = "Bearish candle"
    else:
        direction = "Neutral candle"

    if body_ratio >= 0.65:
        body_comment = "Large real body, showing stronger directional movement."
    elif body_ratio <= 0.25:
        body_comment = "Small real body, showing indecision or weaker directional conviction."
    else:
        body_comment = "Moderate real body, showing balanced price movement."

    if upper_shadow_ratio >= 0.35:
        shadow_comment = "Long upper shadow suggests selling pressure near the high."
    elif lower_shadow_ratio >= 0.35:
        shadow_comment = "Long lower shadow suggests buying support near the low."
    else:
        shadow_comment = "No dominant shadow structure detected."

    return {
        "ticker": latest.get("Ticker"),
        "date": str(latest.get("Date")),
        "open": round(open_price, 4),
        "high": round(high_price, 4),
        "low": round(low_price, 4),
        "close": round(close_price, 4),
        "direction": direction,
        "body_ratio": round(body_ratio, 4),
        "upper_shadow_ratio": round(upper_shadow_ratio, 4),
        "lower_shadow_ratio": round(lower_shadow_ratio, 4),
        "body_comment": body_comment,
        "shadow_comment": shadow_comment,
        "disclaimer": "Candlestick observation is for research only and should not be used as a standalone trading decision.",
    }


def generate_candlestick_commentary(candle_snapshot: Dict[str, object]) -> str:
    """
    Generate a readable candlestick commentary.
    """
    ticker = candle_snapshot.get("ticker")
    date = candle_snapshot.get("date")
    direction = candle_snapshot.get("direction")
    body_comment = candle_snapshot.get("body_comment")
    shadow_comment = candle_snapshot.get("shadow_comment")

    return (
        f"{ticker} latest candle on {date}: {direction}. "
        f"{body_comment} {shadow_comment} "
        "This is a price action observation only, not a buy or sell recommendation."
    )
