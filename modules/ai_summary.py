"""
AI-style summary module for QuantLab Agent.

This module generates structured research summaries from market data,
technical indicators, strategy signals, backtest results, risk metrics,
and candlestick analysis.

Current MVP:
- Rule-based Chinese research summary
- No external AI API required
- OpenAI API can be added in a future version

Important:
- This summary is for education, research, and portfolio demonstration only.
- It is not financial advice.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import pandas as pd


def _format_value(value, suffix: str = "") -> str:
    """
    Format values for readable report output.
    """
    if value is None:
        return "N/A"

    try:
        if isinstance(value, float):
            return f"{value:.4f}{suffix}"
        return f"{value}{suffix}"
    except Exception:
        return f"{value}{suffix}"


def _get_metric_row(risk_comparison: pd.DataFrame, label: str) -> Optional[pd.Series]:
    """
    Get a metric row by label from the risk comparison DataFrame.
    """
    if risk_comparison.empty or "label" not in risk_comparison.columns:
        return None

    matched = risk_comparison[risk_comparison["label"] == label]

    if matched.empty:
        return None

    return matched.iloc[0]


def generate_chinese_research_summary(
    market_snapshot: Dict[str, object],
    indicator_snapshot: Dict[str, object],
    strategy_signal: Dict[str, object],
    backtest_summary: Dict[str, object],
    risk_comparison: pd.DataFrame,
    risk_commentary: str,
    candlestick_snapshot: Dict[str, object],
    candlestick_commentary: str,
) -> str:
    """
    Generate a structured Chinese research summary.
    """
    ticker = market_snapshot.get("ticker") or indicator_snapshot.get("ticker") or "N/A"

    strategy_metrics = _get_metric_row(risk_comparison, "MA Crossover Strategy")
    benchmark_metrics = _get_metric_row(risk_comparison, "Buy and Hold")

    strategy_total_return = (
        strategy_metrics.get("total_return_pct") if strategy_metrics is not None else None
    )
    benchmark_total_return = (
        benchmark_metrics.get("total_return_pct") if benchmark_metrics is not None else None
    )
    strategy_sharpe = (
        strategy_metrics.get("sharpe_ratio") if strategy_metrics is not None else None
    )
    benchmark_sharpe = (
        benchmark_metrics.get("sharpe_ratio") if benchmark_metrics is not None else None
    )
    strategy_risk_level = (
        strategy_metrics.get("risk_level") if strategy_metrics is not None else None
    )
    benchmark_risk_level = (
        benchmark_metrics.get("risk_level") if benchmark_metrics is not None else None
    )

    summary = f"""# QuantLab Agent Research Summary - {ticker}

## 1. 资产概况

- 标的代码：{ticker}
- 最新日期：{market_snapshot.get("date")}
- 最新收盘价：{_format_value(market_snapshot.get("close"))}
- 前一交易日收盘价：{_format_value(market_snapshot.get("previous_close"))}
- 当日涨跌幅：{_format_value(market_snapshot.get("daily_change_pct"), "%")}
- 成交量：{market_snapshot.get("volume")}

## 2. 趋势与技术指标

- MA20：{_format_value(indicator_snapshot.get("MA20"))}
- MA50：{_format_value(indicator_snapshot.get("MA50"))}
- RSI14：{_format_value(indicator_snapshot.get("RSI14"))}
- 20日年化波动率：{_format_value(indicator_snapshot.get("volatility_20d_pct"), "%")}
- 当前回撤：{_format_value(indicator_snapshot.get("drawdown_pct"), "%")}
- 趋势状态：{indicator_snapshot.get("trend_status")}
- RSI 状态：{indicator_snapshot.get("rsi_status")}

## 3. 策略信号

- 当前策略信号：{strategy_signal.get("signal")}
- 模拟仓位状态：{strategy_signal.get("position_status")}
- 策略解释：{strategy_signal.get("reason")}

说明：该信号来自 MA20 / MA50 均线交叉规则，仅用于历史研究和模拟回测，不代表真实买卖建议。

## 4. 回测表现

- 回测开始日期：{backtest_summary.get("start_date")}
- 回测结束日期：{backtest_summary.get("end_date")}
- 策略最终权益：{_format_value(backtest_summary.get("strategy_final_equity"))}
- Buy and Hold 最终权益：{_format_value(backtest_summary.get("buy_hold_final_equity"))}
- 策略总收益率：{_format_value(backtest_summary.get("strategy_return_pct"), "%")}
- Buy and Hold 总收益率：{_format_value(backtest_summary.get("buy_hold_return_pct"), "%")}
- 策略相对超额收益：{_format_value(backtest_summary.get("outperformance_pct"), "%")}

## 5. 风险指标对比

### MA Crossover Strategy

- 总收益率：{_format_value(strategy_total_return, "%")}
- Sharpe Ratio：{_format_value(strategy_sharpe)}
- 风险等级：{strategy_risk_level}

### Buy and Hold

- 总收益率：{_format_value(benchmark_total_return, "%")}
- Sharpe Ratio：{_format_value(benchmark_sharpe)}
- 风险等级：{benchmark_risk_level}

### 风险解读

{risk_commentary}

## 6. K线结构观察

- 最新K线方向：{candlestick_snapshot.get("direction")}
- 实体比例：{_format_value(candlestick_snapshot.get("body_ratio"))}
- 上影线比例：{_format_value(candlestick_snapshot.get("upper_shadow_ratio"))}
- 下影线比例：{_format_value(candlestick_snapshot.get("lower_shadow_ratio"))}
- 实体解读：{candlestick_snapshot.get("body_comment")}
- 影线解读：{candlestick_snapshot.get("shadow_comment")}

K线说明：{candlestick_commentary}

## 7. 综合结论

从当前回测结果看，该 MA Crossover 策略提供了一个可解释的趋势跟随框架。  
如果策略收益低于 Buy and Hold，说明在该历史区间内，简单持有可能更有效；如果策略回撤更低，说明该策略可能在部分阶段起到了风险过滤作用。  
因此，该项目更适合作为量化研究、策略模拟、风险观察和教学展示工具，而不是直接交易系统。

## 8. 免责声明

本报告仅用于教育、研究、模拟回测和作品集展示。  
报告中的策略信号、观察清单、K线分析、风险等级和总结内容不构成任何形式的投资建议、交易建议或个性化资产配置建议。  
历史表现不代表未来结果，任何真实投资决策都需要用户自行研究并承担风险。
"""

    return summary


def save_summary_report(
    summary: str,
    output_path: str,
) -> str:
    """
    Save summary report to a markdown file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(summary, encoding="utf-8")
    return str(path)
