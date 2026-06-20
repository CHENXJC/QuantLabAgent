"""
QuantLab Agent Streamlit Dashboard - QUANTLAB-012 Fixed Version
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from modules.ai_summary import generate_chinese_research_summary, save_summary_report
from modules.backtester import generate_trade_log, get_backtest_summary, run_ma_crossover_backtest
from modules.candlestick_analyzer import analyze_latest_candle, generate_candlestick_commentary
from modules.chart_builder import build_candlestick_chart, build_drawdown_chart, build_equity_curve_chart
from modules.data_loader import get_latest_snapshot, load_market_data, load_sample_tickers
from modules.indicators import add_all_indicators, get_latest_indicator_snapshot
from modules.risk_metrics import compare_strategy_vs_benchmark, generate_risk_commentary
from modules.strategies import generate_ma_crossover_signals, get_latest_strategy_signal


st.set_page_config(
    page_title="QuantLab Agent",
    page_icon="📈",
    layout="wide",
)


LANG = {
    "中文": {
        "subtitle": "AI量化研究看板 + 准实时市场提醒 Agent",
        "warning": "仅用于教育研究和作品集展示。不构成投资建议。不执行真实交易。",
        "control_panel": "控制面板",
        "language": "界面语言",
        "select_ticker": "选择标的",
        "custom_ticker": "或输入自定义代码",
        "custom_placeholder": "例如：AMD, META, QQQ, BTC-USD",
        "data_period": "数据周期",
        "data_interval": "数据频率",
        "capital": "模拟初始资金",
        "risk_free_rate": "年化无风险利率（%）",
        "run_button": "运行 QuantLab 分析",
        "mvp_modules": "MVP 模块",
        "market_data": "市场数据",
        "technical_indicators": "技术指标",
        "strategy_backtest": "策略回测",
        "risk_metrics": "风险指标",
        "candlestick_chart": "K线图",
        "ai_summary": "AI 总结",
        "success": "分析完成",
        "overview": "总览",
        "charts": "图表",
        "backtest_risk": "回测与风险",
        "raw_data": "原始数据",
        "market_snapshot": "1. 市场快照",
        "ticker": "标的代码",
        "close": "最新收盘价",
        "daily_change": "日涨跌幅",
        "volume": "成交量",
        "selected_asset": "当前选择标的",
        "latest_close": "最新收盘价格",
        "daily_change_pct": "日涨跌百分比",
        "latest_volume": "最新成交量",
        "indicator_snapshot": "2. 技术指标快照",
        "ma20": "MA20",
        "ma50": "MA50",
        "rsi14": "RSI14",
        "volatility": "20日波动率",
        "drawdown": "当前回撤",
        "ma20_sub": "20日移动均线",
        "ma50_sub": "50日移动均线",
        "rsi_sub": "相对强弱指标",
        "vol_sub": "年化波动率",
        "drawdown_sub": "当前回撤幅度",
        "trend_status": "趋势状态",
        "rsi_status": "RSI 状态",
        "strategy_signal": "3. 策略信号",
        "signal": "信号",
        "position": "仓位",
        "signal_sub": "均线交叉信号",
        "position_sub": "1 = 风险偏好，0 = 防守",
        "position_status": "仓位状态",
        "signal_reason": "信号原因",
        "candlestick_snapshot": "4. K线结构快照",
        "direction": "K线方向",
        "body_ratio": "实体比例",
        "upper_shadow": "上影线比例",
        "lower_shadow": "下影线比例",
        "backtest_summary": "回测摘要",
        "strategy_return": "策略收益",
        "buy_hold_return": "买入持有收益",
        "outperformance": "相对超额收益",
        "strategy_max_dd": "策略最大回撤",
        "strategy_return_sub": "MA交叉策略",
        "buy_hold_sub": "基准收益",
        "outperformance_sub": "策略减基准",
        "max_dd_sub": "最差模拟回撤",
        "risk_comparison": "风险指标对比",
        "risk_commentary": "风险解读",
        "trade_log": "近期模拟交易日志",
        "no_trades": "该区间内没有生成模拟交易。",
        "chinese_summary": "中文 AI 研究总结",
        "download_report": "下载 Markdown 报告",
        "report_saved": "报告已保存到本地",
        "recent_strategy_data": "近期策略数据",
        "showcase_notes": "作品集展示说明",
        "showcase_text": "QuantLab Agent 展示了完整的研究流程：市场数据读取、技术指标、策略模拟、风险指标、K线可视化和AI风格报告。本项目是研究与作品集项目，不是自动交易机器人。",
        "start_info": "选择标的并点击“运行 QuantLab 分析”开始。",
        "current_mvp": "当前 MVP 模块",
        "safety_boundary": "安全边界",
        "safety_text": "QuantLab Agent 不执行真实交易，不连接券商账户，也不提供个性化金融建议。",
        "demo_flow": "推荐演示流程",
        "demo_text": "1. 选择 SPY、AAPL 或 BTC-USD。\n2. 保持周期为 1y，频率为 1d。\n3. 点击运行 QuantLab 分析。\n4. 查看总览、图表、回测与风险、AI总结和原始数据标签页。"
    },
    "English": {
        "subtitle": "AI Quant Research Dashboard + Near Real-time Market Alert Agent",
        "warning": "Educational research and portfolio demonstration only. No financial advice. No real trade execution.",
        "control_panel": "Control Panel",
        "language": "Language",
        "select_ticker": "Select ticker",
        "custom_ticker": "Or enter custom ticker",
        "custom_placeholder": "Example: AMD, META, QQQ, BTC-USD",
        "data_period": "Data period",
        "data_interval": "Data interval",
        "capital": "Initial simulated capital",
        "risk_free_rate": "Annual risk-free rate (%)",
        "run_button": "Run QuantLab Analysis",
        "mvp_modules": "MVP Modules",
        "market_data": "Market Data",
        "technical_indicators": "Technical Indicators",
        "strategy_backtest": "Strategy Backtest",
        "risk_metrics": "Risk Metrics",
        "candlestick_chart": "Candlestick Chart",
        "ai_summary": "AI Summary",
        "success": "Analysis completed for",
        "overview": "Overview",
        "charts": "Charts",
        "backtest_risk": "Backtest & Risk",
        "raw_data": "Raw Data",
        "market_snapshot": "1. Market Snapshot",
        "ticker": "Ticker",
        "close": "Close",
        "daily_change": "Daily Change",
        "volume": "Volume",
        "selected_asset": "Selected asset",
        "latest_close": "Latest close price",
        "daily_change_pct": "Daily change percentage",
        "latest_volume": "Latest trading volume",
        "indicator_snapshot": "2. Technical Indicator Snapshot",
        "ma20": "MA20",
        "ma50": "MA50",
        "rsi14": "RSI14",
        "volatility": "20D Volatility",
        "drawdown": "Drawdown",
        "ma20_sub": "20-day moving average",
        "ma50_sub": "50-day moving average",
        "rsi_sub": "Relative strength index",
        "vol_sub": "Annualized volatility",
        "drawdown_sub": "Current drawdown",
        "trend_status": "Trend Status",
        "rsi_status": "RSI Status",
        "strategy_signal": "3. Strategy Signal",
        "signal": "Signal",
        "position": "Position",
        "signal_sub": "MA crossover signal",
        "position_sub": "1 = risk-on, 0 = defensive",
        "position_status": "Position Status",
        "signal_reason": "Signal Reason",
        "candlestick_snapshot": "4. Candlestick Snapshot",
        "direction": "Direction",
        "body_ratio": "Body Ratio",
        "upper_shadow": "Upper Shadow",
        "lower_shadow": "Lower Shadow",
        "backtest_summary": "Backtest Summary",
        "strategy_return": "Strategy Return",
        "buy_hold_return": "Buy & Hold Return",
        "outperformance": "Outperformance",
        "strategy_max_dd": "Strategy Max Drawdown",
        "strategy_return_sub": "MA crossover strategy",
        "buy_hold_sub": "Benchmark return",
        "outperformance_sub": "Strategy minus benchmark",
        "max_dd_sub": "Worst simulated drawdown",
        "risk_comparison": "Risk Metrics Comparison",
        "risk_commentary": "Risk Commentary",
        "trade_log": "Recent Trade Log",
        "no_trades": "No simulated trades generated in this period.",
        "chinese_summary": "AI-style Chinese Research Summary",
        "download_report": "Download Markdown Report",
        "report_saved": "Report also saved locally to",
        "recent_strategy_data": "Recent Strategy Data",
        "showcase_notes": "Portfolio Showcase Notes",
        "showcase_text": "QuantLab Agent demonstrates a full research workflow: market data loading, technical indicators, strategy simulation, risk metrics, candlestick visualization, and AI-style reporting. This is a research project, not a trading bot.",
        "start_info": "Select a ticker and click 'Run QuantLab Analysis' to start.",
        "current_mvp": "Current MVP Modules",
        "safety_boundary": "Safety Boundary",
        "safety_text": "QuantLab Agent does not execute real trades, does not connect to brokerage accounts, and does not provide personalized financial advice.",
        "demo_flow": "Recommended Demo Flow",
        "demo_text": "1. Select SPY, AAPL, or BTC-USD.\n2. Keep period as 1y and interval as 1d.\n3. Click Run QuantLab Analysis.\n4. Review Overview, Charts, Backtest & Risk, AI Summary, and Raw Data tabs."
    }
}


def tr(key: str) -> str:
    return LANG[st.session_state.get("language", "中文")].get(key, key)


@st.cache_data(show_spinner=False)
def cached_load_market_data(ticker: str, period: str, interval: str):
    return load_market_data(ticker=ticker, period=period, interval=interval)




def compact_number(value) -> str:
    """
    Convert large numbers into compact dashboard format.
    """
    if value is None:
        return "N/A"

    try:
        number = float(value)
    except Exception:
        return str(value)

    abs_number = abs(number)

    if abs_number >= 1_000_000_000_000:
        return f"{number / 1_000_000_000_000:.2f}T"
    if abs_number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f}B"
    if abs_number >= 1_000_000:
        return f"{number / 1_000_000:.2f}M"
    if abs_number >= 1_000:
        return f"{number:,.2f}"

    return f"{number:.2f}"


def format_display_value(value, suffix: str = "") -> str:
    """
    Format values for dashboard cards.
    AI reports and raw data keep full detail; cards use compact display.
    """
    if value is None:
        return "N/A"

    if isinstance(value, str):
        return value

    try:
        number = float(value)
    except Exception:
        return f"{value}{suffix}"

    if suffix == "%":
        return f"{number:.2f}%"

    return compact_number(number)


def render_card(title: str, value, subtitle: str = "", suffix: str = "") -> None:
    """
    Render a clean dashboard card without Streamlit metric truncation.
    """
    display_value = format_display_value(value, suffix=suffix)

    st.markdown(
        f"""
        <div style="
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 14px 14px;
            background: #FFFFFF;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            min-height: 104px;
            overflow: hidden;
        ">
            <div style="font-size: 12px; color: #6B7280; margin-bottom: 8px;">
                {title}
            </div>
            <div style="
                font-size: 18px;
                font-weight: 700;
                color: #111827;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            ">
                {display_value}
            </div>
            <div style="font-size: 11px; color: #9CA3AF; margin-top: 8px;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )





def translate_analysis_text(value) -> str:
    """
    Translate backend English analysis outputs into Chinese when UI language is Chinese.
    English mode keeps original text.
    """
    if value is None:
        return "N/A"

    text_value = str(value)

    if st.session_state.get("language", "中文") != "中文":
        return text_value

    replacements = {
        "Bullish trend": "看涨趋势",
        "Bearish trend": "看跌趋势",
        "Positive but mixed": "偏正面但结构混合",
        "Weak but mixed": "偏弱但结构混合",
        "Neutral": "中性",
        "Weak momentum": "动能偏弱",
        "Positive momentum": "动能偏强",
        "Overbought": "超买",
        "Oversold": "超卖",
        "Insufficient data": "数据不足",

        "Simulated risk-on": "模拟风险偏好仓位",
        "Simulated cash / defensive": "模拟现金 / 防守仓位",

        "BUY": "买入观察",
        "SELL": "卖出观察",
        "HOLD": "持有 / 观望",

        "Bullish candle": "看涨K线",
        "Bearish candle": "看跌K线",
        "Neutral candle": "中性K线",

        "Large real body, showing stronger directional movement.": "实体较大，说明当日方向性波动较强。",
        "Small real body, showing indecision or weaker directional conviction.": "实体较小，说明多空犹豫或方向性不足。",
        "Moderate real body, showing balanced price movement.": "实体中等，说明价格波动相对均衡。",

        "Long upper shadow suggests selling pressure near the high.": "较长上影线说明高位附近存在一定卖压。",
        "Long lower shadow suggests buying support near the low.": "较长下影线说明低位附近存在一定承接。",
        "No dominant shadow structure detected.": "未检测到明显主导影线结构。",

        "MA20 is above MA50, indicating positive trend structure.": "MA20 高于 MA50，说明当前趋势结构偏正面。",
        "MA20 is below MA50, indicating weak trend structure.": "MA20 低于 MA50，说明当前趋势结构偏弱。",
        "MA20 and MA50 are close, indicating neutral trend structure.": "MA20 与 MA50 接近，说明当前趋势结构偏中性。",
        "Insufficient moving average data.": "均线数据不足，暂时无法判断趋势结构。",

        "The strategy outperformed the Buy and Hold benchmark on total return.": "该策略在总收益率上跑赢了买入持有基准。",
        "The strategy underperformed the Buy and Hold benchmark on total return.": "该策略在总收益率上低于买入持有基准。",
        "The strategy showed lower maximum drawdown than the benchmark.": "该策略的最大回撤低于基准，说明历史区间内风险控制更好。",
        "The strategy showed higher or similar drawdown risk compared with the benchmark.": "该策略的回撤风险高于或接近基准。",
        "The strategy achieved a better risk-adjusted return based on Sharpe ratio.": "从夏普比率看，该策略取得了更好的风险调整后收益。",
        "The strategy did not improve risk-adjusted return based on Sharpe ratio.": "从夏普比率看，该策略没有改善风险调整后收益。",
        "These results are historical simulations only and do not guarantee future performance.": "以上结果仅为历史模拟，不代表未来表现。",

        "This is a price action observation only, not a buy or sell recommendation.": "该内容仅为价格行为观察，不构成买入或卖出建议。",
        "Candlestick observation is for research only and should not be used as a standalone trading decision.": "K线观察仅用于研究，不应作为单独交易决策依据。",
    }

    translated = text_value

    for old, new in replacements.items():
        translated = translated.replace(old, new)

    translated = translated.replace("latest candle on", "最新K线日期：")
    translated = translated.replace("The latest candle shows", "最新K线显示")
    translated = translated.replace("price action observation only", "价格行为观察")
    translated = translated.replace("not a buy or sell recommendation", "不构成买入或卖出建议")

    return translated



def clean_report_text_for_language(value) -> str:
    """
    Clean AI Summary Markdown report for Chinese UI mode.
    English UI mode keeps original report text.
    """
    if value is None:
        return "N/A"

    report = str(value)

    if st.session_state.get("language", "中文") != "中文":
        return report

    replacements = {
        "HOLD": "持有 / 观望",
        "BUY": "买入观察",
        "SELL": "卖出观察",

        "Simulated risk-on": "模拟风险偏好仓位",
        "Simulated cash / defensive": "模拟现金 / 防守仓位",

        "Positive but mixed": "偏正面但结构混合",
        "Bearish trend": "看跌趋势",
        "Bullish trend": "看涨趋势",
        "Weak momentum": "动能偏弱",
        "Positive momentum": "动能偏强",
        "Neutral": "中性",

        "Bearish candle": "看跌K线",
        "Bullish candle": "看涨K线",
        "Neutral candle": "中性K线",

        "MA20 is above MA50, indicating positive trend structure.": "MA20 高于 MA50，说明当前趋势结构偏正面。",
        "MA20 is below MA50, indicating weak trend structure.": "MA20 低于 MA50，说明当前趋势结构偏弱。",
        "MA20 and MA50 are close, indicating neutral trend structure.": "MA20 与 MA50 接近，说明当前趋势结构偏中性。",

        "The strategy underperformed the Buy and Hold benchmark on total return.": "该策略在总收益率上低于买入持有基准。",
        "The strategy outperformed the Buy and Hold benchmark on total return.": "该策略在总收益率上跑赢买入持有基准。",
        "The strategy showed lower maximum drawdown than the benchmark.": "该策略的最大回撤低于基准，说明历史区间内回撤控制更好。",
        "The strategy showed higher or similar drawdown risk compared with the benchmark.": "该策略的回撤风险高于或接近基准。",
        "The strategy did not improve risk-adjusted return based on Sharpe ratio.": "从夏普比率看，该策略没有改善风险调整后收益。",
        "The strategy achieved a better risk-adjusted return based on Sharpe ratio.": "从夏普比率看，该策略取得了更好的风险调整后收益。",
        "These results are historical simulations only and do not guarantee future performance.": "以上结果仅为历史模拟，不代表未来表现。",

        "Large real body, showing stronger directional movement.": "实体较大，说明当日方向性波动较强。",
        "Small real body, showing indecision or weaker directional conviction.": "实体较小，说明多空犹豫或方向性不足。",
        "Moderate real body, showing balanced price movement.": "实体中等，说明价格波动相对均衡。",
        "Long upper shadow suggests selling pressure near the high.": "较长上影线说明高位附近存在一定卖压。",
        "Long lower shadow suggests buying support near the low.": "较长下影线说明低位附近存在一定承接。",
        "No dominant shadow structure detected.": "未检测到明显主导影线结构。",
        "This is a price action observation only, not a buy or sell recommendation.": "该内容仅为价格行为观察，不构成买入或卖出建议。",

        "MA Crossover Strategy": "MA Crossover Strategy（均线交叉策略）",
        "Buy and Hold": "Buy and Hold（买入持有）",
        "Sharpe Ratio": "Sharpe Ratio（夏普比率）",
        "Low": "低",
        "Medium": "中",
        "High": "高",
    }

    for old, new in replacements.items():
        report = report.replace(old, new)

    report = report.replace("latest candle on", "最新K线日期：")
    report = report.replace("The latest candle shows", "最新K线显示")
    report = report.replace("price action observation only", "价格行为观察")
    report = report.replace("not a buy or sell recommendation", "不构成买入或卖出建议")

    return report

def run_pipeline(ticker: str, period: str, interval: str, capital: float, risk_free_rate: float):
    df = cached_load_market_data(ticker=ticker, period=period, interval=interval)

    market_snapshot = get_latest_snapshot(df)

    indicator_df = add_all_indicators(df)
    indicator_snapshot = get_latest_indicator_snapshot(indicator_df)

    signal_df = generate_ma_crossover_signals(indicator_df)
    latest_signal = get_latest_strategy_signal(signal_df)

    backtest_df = run_ma_crossover_backtest(signal_df, initial_capital=capital)
    backtest_summary = get_backtest_summary(backtest_df)

    risk_comparison = compare_strategy_vs_benchmark(
        backtest_df,
        risk_free_rate=risk_free_rate,
    )
    risk_commentary = generate_risk_commentary(risk_comparison)

    candle_snapshot = analyze_latest_candle(backtest_df)
    candle_commentary = generate_candlestick_commentary(candle_snapshot)

    trade_log = generate_trade_log(signal_df, initial_capital=capital)

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

    return {
        "backtest_df": backtest_df,
        "market_snapshot": market_snapshot,
        "indicator_snapshot": indicator_snapshot,
        "latest_signal": latest_signal,
        "backtest_summary": backtest_summary,
        "risk_comparison": risk_comparison,
        "risk_commentary": risk_commentary,
        "candle_snapshot": candle_snapshot,
        "candle_commentary": candle_commentary,
        "trade_log": trade_log,
        "summary": summary,
    }


with st.sidebar:
    language = st.radio(
        "界面语言 / Language",
        ["中文", "English"],
        index=0,
        horizontal=True,
        key="language_selector",
    )
    st.session_state["language"] = language

st.title("QuantLab Agent")
st.caption(tr("subtitle"))

st.warning(tr("warning"))

with st.sidebar:
    st.header(tr("control_panel"))

    try:
        sample_tickers = load_sample_tickers()
        ticker_options = sample_tickers["ticker"].tolist()
    except Exception:
        ticker_options = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA", "BTC-USD", "ETH-USD"]

    ticker = st.selectbox(
        tr("select_ticker"),
        ticker_options,
        key="ticker_selector",
    )

    custom_ticker = st.text_input(
        tr("custom_ticker"),
        value="",
        placeholder=tr("custom_placeholder"),
        key="custom_ticker_input",
    )

    selected_ticker = custom_ticker.strip().upper() if custom_ticker.strip() else ticker

    period = st.selectbox(
        tr("data_period"),
        ["3mo", "6mo", "1y", "2y", "3y", "5y"],
        index=2,
        key="period_selector",
    )
    interval = st.selectbox(
        tr("data_interval"),
        ["1d", "1h", "30m", "15m"],
        index=0,
        key="interval_selector",
    )

    capital = st.number_input(
        tr("capital"),
        min_value=1000.0,
        max_value=1000000.0,
        value=10000.0,
        step=1000.0,
        key="capital_input",
    )

    risk_free_rate_pct = st.number_input(
        tr("risk_free_rate"),
        min_value=0.0,
        max_value=20.0,
        value=0.0,
        step=0.25,
        key="risk_free_rate_input",
    )

    run_button = st.button(
        tr("run_button"),
        type="primary",
        key="run_analysis_button",
    )

    st.divider()
    st.caption(tr("mvp_modules"))
    st.write("- " + tr("market_data"))
    st.write("- " + tr("technical_indicators"))
    st.write("- " + tr("strategy_backtest"))
    st.write("- " + tr("risk_metrics"))
    st.write("- " + tr("candlestick_chart"))
    st.write("- " + tr("ai_summary"))


if run_button:
    try:
        with st.spinner("Running QuantLab analysis..."):
            result = run_pipeline(
                ticker=selected_ticker,
                period=period,
                interval=interval,
                capital=capital,
                risk_free_rate=risk_free_rate_pct / 100,
            )

        backtest_df = result["backtest_df"]
        market_snapshot = result["market_snapshot"]
        indicator_snapshot = result["indicator_snapshot"]
        latest_signal = result["latest_signal"]
        backtest_summary = result["backtest_summary"]
        risk_comparison = result["risk_comparison"]
        risk_commentary = result["risk_commentary"]
        candle_snapshot = result["candle_snapshot"]
        candle_commentary = result["candle_commentary"]
        trade_log = result["trade_log"]
        summary = result["summary"]

        summary = clean_report_text_for_language(summary)

        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        report_path = output_dir / f"{selected_ticker}_dashboard_summary.md"
        save_summary_report(clean_report_text_for_language(summary), str(report_path))

        st.success(f"{tr('success')} {selected_ticker}")

        overview_tab, charts_tab, risk_tab, report_tab, data_tab = st.tabs(
            [tr("overview"), tr("charts"), tr("backtest_risk"), tr("ai_summary"), tr("raw_data")]
        )

        with overview_tab:
            st.subheader(tr("market_snapshot"))
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                render_card(tr("ticker"), market_snapshot.get("ticker"), tr("selected_asset"))

            with col2:
                render_card(tr("close"), market_snapshot.get("close"), tr("latest_close"))

            with col3:
                render_card(tr("daily_change"), market_snapshot.get("daily_change_pct"), tr("daily_change_pct"), "%")

            with col4:
                render_card(tr("volume"), market_snapshot.get("volume"), tr("latest_volume"))

            st.subheader(tr("indicator_snapshot"))
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                render_card(tr("ma20"), indicator_snapshot.get("MA20"), tr("ma20_sub"))

            with col2:
                render_card(tr("ma50"), indicator_snapshot.get("MA50"), tr("ma50_sub"))

            with col3:
                render_card(tr("rsi14"), indicator_snapshot.get("RSI14"), tr("rsi_sub"))

            with col4:
                render_card(tr("volatility"), indicator_snapshot.get("volatility_20d_pct"), tr("vol_sub"), "%")

            col1, col2, col3 = st.columns(3)

            with col1:
                render_card(tr("drawdown"), indicator_snapshot.get("drawdown_pct"), tr("drawdown_sub"), "%")

            with col2:
                st.markdown(f"**{tr('trend_status')}**")
                st.info(translate_analysis_text(indicator_snapshot.get("trend_status")))

            with col3:
                st.markdown(f"**{tr('rsi_status')}**")
                st.info(translate_analysis_text(indicator_snapshot.get("rsi_status")))

            st.subheader(tr("strategy_signal"))
            col1, col2 = st.columns(2)

            with col1:
                render_card(tr("signal"), translate_analysis_text(latest_signal.get("signal")), tr("signal_sub"))

            with col2:
                render_card(tr("position"), latest_signal.get("position"), tr("position_sub"))

            st.markdown(f"**{tr('position_status')}**")
            st.info(translate_analysis_text(latest_signal.get("position_status")))

            st.markdown(f"**{tr('signal_reason')}**")
            st.write(translate_analysis_text(latest_signal.get("reason")))

            st.subheader(tr("candlestick_snapshot"))
            col1, col2, col3, col4 = st.columns(4)
            render_card(tr("direction"), translate_analysis_text(candle_snapshot.get("direction")), "K线方向")
            col2.metric(tr("body_ratio"), candle_snapshot.get("body_ratio"))
            col3.metric(tr("upper_shadow"), candle_snapshot.get("upper_shadow_ratio"))
            col4.metric(tr("lower_shadow"), candle_snapshot.get("lower_shadow_ratio"))

            st.write(translate_analysis_text(candle_snapshot.get("body_comment")))
            st.write(translate_analysis_text(candle_snapshot.get("shadow_comment")))
            st.caption(translate_analysis_text(candle_commentary))

        with charts_tab:
            st.subheader(tr("candlestick_chart"))
            candlestick_fig = build_candlestick_chart(backtest_df, ticker=selected_ticker)
            st.plotly_chart(candlestick_fig, width="stretch")

            st.subheader("Strategy vs Buy and Hold")
            equity_fig = build_equity_curve_chart(backtest_df, ticker=selected_ticker)
            st.plotly_chart(equity_fig, width="stretch")

            st.subheader("Drawdown Comparison")
            drawdown_fig = build_drawdown_chart(backtest_df, ticker=selected_ticker)
            st.plotly_chart(drawdown_fig, width="stretch")

        with risk_tab:
            st.subheader(tr("backtest_summary"))
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                render_card(tr("strategy_return"), backtest_summary.get("strategy_return_pct"), tr("strategy_return_sub"), "%")

            with col2:
                render_card(tr("buy_hold_return"), backtest_summary.get("buy_hold_return_pct"), tr("buy_hold_sub"), "%")

            with col3:
                render_card(tr("outperformance"), backtest_summary.get("outperformance_pct"), tr("outperformance_sub"), "%")

            with col4:
                render_card(tr("strategy_max_dd"), backtest_summary.get("strategy_max_drawdown_pct"), tr("max_dd_sub"), "%")

            st.subheader(tr("risk_comparison"))
            st.dataframe(risk_comparison, width="stretch")

            st.subheader(tr("risk_commentary"))
            st.info(translate_analysis_text(risk_commentary))

            st.subheader(tr("trade_log"))
            if trade_log.empty:
                st.write(tr("no_trades"))
            else:
                st.dataframe(trade_log.tail(20), width="stretch")

        with report_tab:
            st.subheader(tr("chinese_summary"))
            st.markdown(clean_report_text_for_language(summary))

            st.download_button(
                label=tr("download_report"),
                data=clean_report_text_for_language(summary),
                file_name=f"{selected_ticker}_research_summary.md",
                mime="text/markdown",
            )

            st.caption(f"{tr('report_saved')}: {report_path}")

        with data_tab:
            st.subheader(tr("recent_strategy_data"))
            display_columns = [
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "MA20",
                "MA50",
                "RSI14",
                "ma_signal",
                "ma_position",
                "strategy_equity",
                "buy_hold_equity",
                "strategy_drawdown",
                "Ticker",
            ]
            available_columns = [col for col in display_columns if col in backtest_df.columns]
            st.dataframe(backtest_df[available_columns].tail(100), width="stretch")

        st.divider()
        st.subheader(tr("showcase_notes"))
        st.write(tr("showcase_text"))

    except Exception as exc:
        st.error("QuantLab analysis failed.")
        st.exception(exc)

else:
    st.info(tr("start_info"))

    st.subheader(tr("current_mvp"))
    st.write(
        """
        - Market data loading（市场数据读取）
        - Technical indicators（技术指标）
        - MA crossover strategy signal（均线交叉策略信号）
        - Basic backtesting（基础回测）
        - Risk metrics comparison（风险指标对比）
        - Candlestick chart（K线图）
        - Strategy equity curve（策略权益曲线）
        - Drawdown chart（回撤图）
        - AI-style Chinese research summary（AI风格中文研究总结）
        """
    )

    st.subheader(tr("safety_boundary"))
    st.write(tr("safety_text"))

    st.subheader(tr("demo_flow"))
    st.write(tr("demo_text"))
