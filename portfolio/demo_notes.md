# QuantLab Agent Demo Notes

## Demo Positioning

QuantLab Agent is a portfolio-grade AI quant research dashboard.

It demonstrates:

- Market data loading（市场数据读取）
- Technical indicators（技术指标）
- MA crossover strategy signal（均线交叉策略信号）
- Basic backtesting（基础回测）
- Risk metrics comparison（风险指标对比）
- Candlestick chart（K线图）
- Strategy equity curve（策略权益曲线）
- Drawdown chart（回撤图）
- AI-style Chinese research summary（AI风格中文研究总结）
- Bilingual dashboard UI（中英文双语界面）
- Portfolio-ready Streamlit product design（作品集级网页产品设计）

---

## Recommended Demo Flow

### Step 1: Open Dashboard

Run:

streamlit run app.py

Open:

http://localhost:8501

---

### Step 2: Chinese Overview Demo

Settings:

- Language: 中文
- Ticker: SPY
- Period: 1y
- Interval: 1d
- Initial capital: 10000
- Risk-free rate: 0

Click:

运行 QuantLab 分析

Show:

- 市场快照
- 技术指标快照
- 策略信号
- K线结构快照

---

### Step 3: Chart Demo

Open:

图表 / Charts

Show:

- Candlestick Chart（K线图）
- MA20 / MA50
- Volume（成交量）
- Buy / Sell markers（买入 / 卖出信号标记）
- Strategy vs Buy and Hold（策略与买入持有对比）
- Drawdown comparison（回撤对比）

---

### Step 4: Backtest and Risk Demo

Open:

回测与风险 / Backtest & Risk

Show:

- Strategy Return（策略收益）
- Buy & Hold Return（买入持有收益）
- Outperformance（相对超额收益）
- Strategy Max Drawdown（策略最大回撤）
- Risk Metrics Comparison（风险指标对比）
- Recent Trade Log（近期模拟交易日志）

---

### Step 5: AI Summary Demo

Open:

AI 总结 / AI Summary

Show:

- Chinese structured research summary（中文结构化研究总结）
- Asset overview（资产概况）
- Technical indicators（技术指标）
- Backtest summary（回测摘要）
- Risk explanation（风险解释）
- Candlestick observation（K线观察）
- Disclaimer（免责声明）

---

### Step 6: English UI Demo

Switch language:

English

Show:

- English sidebar
- English tabs
- English control labels
- Bilingual product readiness

---

### Step 7: Multi-Asset Demo

Test:

- AAPL
- BTC-USD

Purpose:

Show that QuantLab supports stocks, ETFs, and crypto-style tickers.

---

## Portfolio Message

QuantLab Agent is not a trading bot.

It is an AI-assisted quant research and market analysis dashboard for educational research, strategy simulation, and portfolio demonstration.

The project shows the ability to combine:

- Financial data analysis
- Quantitative thinking
- Risk-aware product design
- Streamlit dashboard development
- AI-style report generation
- Bilingual user interface design

---

## Safety Boundary

QuantLab Agent does not:

- Execute real trades
- Connect to brokerage accounts
- Provide personalized financial advice
- Guarantee returns
- Perform high-frequency trading

All outputs are for research and portfolio demonstration only.
