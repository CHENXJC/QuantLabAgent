"""
Chart builder module for QuantLab Agent.

This module creates portfolio-grade visual charts for research and dashboard use.

Current MVP chart:
- Candlestick chart
- MA20 / MA50 overlay
- Volume bar chart
- Buy / Sell signal markers
- Strategy equity vs Buy and Hold equity

Important:
- Charts are for research and visualization only.
- They are not trading recommendations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_candlestick_chart(
    df: pd.DataFrame,
    ticker: Optional[str] = None,
    output_path: Optional[str] = None,
) -> go.Figure:
    """
    Build a candlestick chart with MA20, MA50, volume, and buy/sell markers.
    """
    data = df.copy()

    required_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns for candlestick chart: {missing}")

    if ticker is None:
        ticker = str(data["Ticker"].iloc[-1]) if "Ticker" in data.columns else "Ticker"

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.72, 0.28],
        subplot_titles=(
            f"{ticker} Candlestick Chart",
            "Volume",
        ),
    )

    fig.add_trace(
        go.Candlestick(
            x=data["Date"],
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Candlestick",
        ),
        row=1,
        col=1,
    )

    if "MA20" in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["MA20"],
                mode="lines",
                name="MA20",
            ),
            row=1,
            col=1,
        )

    if "MA50" in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["MA50"],
                mode="lines",
                name="MA50",
            ),
            row=1,
            col=1,
        )

    if "ma_signal" in data.columns:
        buy_points = data[data["ma_signal"] == "BUY"]
        sell_points = data[data["ma_signal"] == "SELL"]

        if not buy_points.empty:
            fig.add_trace(
                go.Scatter(
                    x=buy_points["Date"],
                    y=buy_points["Close"],
                    mode="markers",
                    name="BUY Signal",
                    marker=dict(symbol="triangle-up", size=12),
                ),
                row=1,
                col=1,
            )

        if not sell_points.empty:
            fig.add_trace(
                go.Scatter(
                    x=sell_points["Date"],
                    y=sell_points["Close"],
                    mode="markers",
                    name="SELL Signal",
                    marker=dict(symbol="triangle-down", size=12),
                ),
                row=1,
                col=1,
            )

    fig.add_trace(
        go.Bar(
            x=data["Date"],
            y=data["Volume"],
            name="Volume",
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        title=f"QuantLab Agent - {ticker} Price Action and Signals",
        xaxis_rangeslider_visible=False,
        height=800,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(path))

    return fig


def build_equity_curve_chart(
    df: pd.DataFrame,
    ticker: Optional[str] = None,
    output_path: Optional[str] = None,
) -> go.Figure:
    """
    Build a strategy equity curve comparison chart.
    """
    data = df.copy()

    required_columns = ["Date", "strategy_equity", "buy_hold_equity"]
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns for equity curve chart: {missing}")

    if ticker is None:
        ticker = str(data["Ticker"].iloc[-1]) if "Ticker" in data.columns else "Ticker"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["strategy_equity"],
            mode="lines",
            name="MA Crossover Strategy",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["buy_hold_equity"],
            mode="lines",
            name="Buy and Hold",
        )
    )

    fig.update_layout(
        title=f"QuantLab Agent - {ticker} Strategy vs Buy and Hold",
        xaxis_title="Date",
        yaxis_title="Equity Value",
        height=500,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(path))

    return fig


def build_drawdown_chart(
    df: pd.DataFrame,
    ticker: Optional[str] = None,
    output_path: Optional[str] = None,
) -> go.Figure:
    """
    Build a strategy vs benchmark drawdown chart.
    """
    data = df.copy()

    required_columns = ["Date", "strategy_drawdown", "buy_hold_drawdown"]
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns for drawdown chart: {missing}")

    if ticker is None:
        ticker = str(data["Ticker"].iloc[-1]) if "Ticker" in data.columns else "Ticker"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["strategy_drawdown"] * 100,
            mode="lines",
            name="Strategy Drawdown",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["buy_hold_drawdown"] * 100,
            mode="lines",
            name="Buy and Hold Drawdown",
        )
    )

    fig.update_layout(
        title=f"QuantLab Agent - {ticker} Drawdown Comparison",
        xaxis_title="Date",
        yaxis_title="Drawdown (%)",
        height=500,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(path))

    return fig
