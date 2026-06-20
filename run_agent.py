"""
Command-line runner for QuantLab Agent MVP.

Current functions:
- Load historical market data.
- Calculate technical indicators.
- Generate MA crossover strategy signals.
- Run a basic backtest.
- Calculate professional risk metrics.
- Generate candlestick chart and equity charts.
- Generate Chinese AI-style research summary.

Example:
python run_agent.py --ticker SPY --period 1y --interval 1d
"""

from __future__ import annotations

import argparse
from pathlib import Path

from modules.ai_summary import generate_chinese_research_summary, save_summary_report
from modules.backtester import (
    generate_trade_log,
    get_backtest_summary,
    run_ma_crossover_backtest,
)
from modules.candlestick_analyzer import (
    analyze_latest_candle,
    generate_candlestick_commentary,
)
from modules.chart_builder import (
    build_candlestick_chart,
    build_drawdown_chart,
    build_equity_curve_chart,
)
from modules.data_loader import get_latest_snapshot, load_market_data, load_sample_tickers
from modules.indicators import add_all_indicators, get_latest_indicator_snapshot
from modules.risk_metrics import compare_strategy_vs_benchmark, generate_risk_commentary
from modules.strategies import generate_ma_crossover_signals, get_latest_strategy_signal


def main() -> None:
    parser = argparse.ArgumentParser(description="QuantLab Agent AI summary test")
    parser.add_argument("--ticker", type=str, default="SPY", help="Ticker symbol, for example SPY, QQQ, AAPL, TSLA, BTC-USD")
    parser.add_argument("--period", type=str, default="1y", help="Data period, for example 6mo, 1y, 3y, 5y")
    parser.add_argument("--interval", type=str, default="1d", help="Data interval, for example 1d, 1h, 15m")
    parser.add_argument("--capital", type=float, default=10000.0, help="Initial simulated capital")
    parser.add_argument("--risk-free-rate", type=float, default=0.0, help="Annualized risk-free rate, for example 0.04")

    args = parser.parse_args()
    ticker = args.ticker.strip().upper()

    print("=" * 80)
    print("QuantLab Agent - AI Summary Test")
    print("=" * 80)

    print("\nSample ticker universe:")
    sample_tickers = load_sample_tickers()
    print(sample_tickers.head(10).to_string(index=False))

    print("\nLoading market data...")
    df = load_market_data(
        ticker=ticker,
        period=args.period,
        interval=args.interval,
    )

    market_snapshot = get_latest_snapshot(df)

    print("\nLatest market snapshot:")
    for key, value in market_snapshot.items():
        print(f"{key}: {value}")

    print("\nCalculating indicators...")
    indicator_df = add_all_indicators(df)
    indicator_snapshot = get_latest_indicator_snapshot(indicator_df)

    print("\nLatest indicator snapshot:")
    for key, value in indicator_snapshot.items():
        print(f"{key}: {value}")

    print("\nGenerating strategy signals...")
    signal_df = generate_ma_crossover_signals(indicator_df)
    latest_signal = get_latest_strategy_signal(signal_df)

    print("\nLatest strategy signal:")
    for key, value in latest_signal.items():
        print(f"{key}: {value}")

    print("\nRunning backtest...")
    backtest_df = run_ma_crossover_backtest(signal_df, initial_capital=args.capital)
    backtest_summary = get_backtest_summary(backtest_df)

    print("\nBacktest summary:")
    for key, value in backtest_summary.items():
        print(f"{key}: {value}")

    print("\nRisk metrics comparison:")
    risk_comparison = compare_strategy_vs_benchmark(
        backtest_df,
        risk_free_rate=args.risk_free_rate,
    )
    print(risk_comparison.to_string(index=False))

    risk_commentary = generate_risk_commentary(risk_comparison)

    print("\nRisk commentary:")
    print(risk_commentary)

    print("\nCandlestick analysis:")
    candle_snapshot = analyze_latest_candle(backtest_df)
    for key, value in candle_snapshot.items():
        print(f"{key}: {value}")

    candle_commentary = generate_candlestick_commentary(candle_snapshot)

    print("\nCandlestick commentary:")
    print(candle_commentary)

    trade_log = generate_trade_log(signal_df, initial_capital=args.capital)

    print("\nRecent trade log:")
    if trade_log.empty:
        print("No simulated trades generated in this period.")
    else:
        print(trade_log.tail(10).to_string(index=False))

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    candlestick_path = output_dir / f"{ticker}_candlestick.html"
    equity_path = output_dir / f"{ticker}_equity_curve.html"
    drawdown_path = output_dir / f"{ticker}_drawdown.html"
    report_path = output_dir / f"{ticker}_research_summary.md"

    print("\nGenerating charts...")
    build_candlestick_chart(backtest_df, ticker=ticker, output_path=str(candlestick_path))
    build_equity_curve_chart(backtest_df, ticker=ticker, output_path=str(equity_path))
    build_drawdown_chart(backtest_df, ticker=ticker, output_path=str(drawdown_path))

    print(f"Candlestick chart saved to: {candlestick_path}")
    print(f"Equity curve chart saved to: {equity_path}")
    print(f"Drawdown chart saved to: {drawdown_path}")

    print("\nGenerating AI-style Chinese research summary...")
    summary = generate_chinese_research_summary(
        market_snapshot=market_snapshot,
        indicator_snapshot=indicator_snapshot,
        strategy_signal=latest_signal,
        backtest_summary=backtest_summary,
        risk_comparison=risk_comparison,
        risk_commentary=risk_commentary,
        candlestick_snapshot=candle_snapshot,
        candlestick_commentary=candle_commentary,
    )

    save_summary_report(summary, str(report_path))

    print(f"Research summary saved to: {report_path}")

    print("\nSummary preview:")
    print(summary[:1200])

    print("\nQUANTLAB-010 AI summary test passed.")


if __name__ == "__main__":
    main()
