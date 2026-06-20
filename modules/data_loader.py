"""
Data loading module for QuantLab Agent.

This module loads historical market data for stocks, ETFs, and crypto tickers.
The MVP uses yfinance as a research and demonstration data source.

Important:
- This module is for educational and research use only.
- Market data may be delayed or incomplete depending on the data provider.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import yfinance as yf


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def _flatten_yfinance_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    yfinance may return MultiIndex columns depending on version and ticker format.
    This helper converts columns back to standard OHLCV names.
    """
    if isinstance(df.columns, pd.MultiIndex):
        known_columns = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}
        new_columns = []

        for col in df.columns:
            parts = [str(part) for part in col if str(part)]
            matched = next((part for part in parts if part in known_columns), parts[-1])
            new_columns.append(matched)

        df = df.copy()
        df.columns = new_columns

    return df


def load_market_data(
    ticker: str = "SPY",
    period: str = "1y",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Load historical market data using yfinance.

    Parameters:
        ticker: Market ticker, for example SPY, QQQ, AAPL, TSLA, BTC-USD.
        period: Data period, for example 1mo, 3mo, 6mo, 1y, 3y, 5y.
        interval: Data interval, for example 1d, 1h, 15m.

    Returns:
        A cleaned pandas DataFrame with Date, Open, High, Low, Close, Adj Close, Volume.
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string.")

    ticker = ticker.strip().upper()

    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
        group_by="column",
    )

    if df is None or df.empty:
        raise ValueError(f"No market data returned for ticker: {ticker}")

    df = _flatten_yfinance_columns(df)

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for {ticker}: {missing_columns}")

    df = df.copy()
    df = df.dropna(subset=["Close"])

    for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.index.name = "Date"
    df = df.reset_index()

    df["Ticker"] = ticker

    return df


def load_sample_tickers(csv_path: str = "data/sample_tickers.csv") -> pd.DataFrame:
    """
    Load the sample ticker universe from CSV.
    """
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Sample ticker file not found: {csv_path}")

    return pd.read_csv(path)


def get_latest_snapshot(df: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    Return a simple latest market snapshot from a market data DataFrame.
    """
    if df.empty:
        raise ValueError("Cannot create snapshot from empty DataFrame.")

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) >= 2 else None

    close_price = float(latest["Close"])
    previous_close = float(previous["Close"]) if previous is not None else None

    daily_change_pct = None
    if previous_close and previous_close != 0:
        daily_change_pct = (close_price / previous_close - 1) * 100

    return {
        "ticker": latest.get("Ticker"),
        "date": str(latest.get("Date")),
        "close": round(close_price, 4),
        "previous_close": round(previous_close, 4) if previous_close else None,
        "daily_change_pct": round(daily_change_pct, 4) if daily_change_pct is not None else None,
        "volume": int(latest["Volume"]) if pd.notna(latest["Volume"]) else None,
    }


if __name__ == "__main__":
    test_df = load_market_data("SPY", period="1mo", interval="1d")
    print(test_df.tail())
    print(get_latest_snapshot(test_df))
