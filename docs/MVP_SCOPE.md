# QuantLab Agent MVP Scope

## Project Goal

QuantLab Agent is an AI-powered quantitative research and market monitoring project.

The MVP is designed as a portfolio-grade project that demonstrates:

- Python financial data analysis
- Quantitative strategy research
- Backtesting logic
- Candlestick visualization
- Risk metric calculation
- AI-style research summaries
- Modular software architecture
- Future Telegram alert integration

---

## MVP Core Modules

### 1. Data Loading Module

File: modules/data_loader.py

Purpose:

- Load historical market data
- Support stocks, ETFs, and crypto tickers
- Clean OHLCV data for analysis

### 2. Indicator Module

File: modules/indicators.py

Purpose:

- Moving averages
- Daily returns
- Volatility
- RSI
- Drawdown helper fields

### 3. Strategy Module

File: modules/strategies.py

Purpose:

- Buy and Hold baseline
- Moving average crossover strategy
- RSI observation strategy
- Buy, Sell, and Hold signal generation

### 4. Backtesting Module

File: modules/backtester.py

Purpose:

- Run historical strategy simulations
- Compare strategy performance with Buy and Hold
- Generate paper trading style trade logs

### 5. Risk Metrics Module

File: modules/risk_metrics.py

Purpose:

- Total return
- Annualized volatility
- Maximum drawdown
- Sharpe ratio
- Win rate
- Risk level classification

### 6. Candlestick Analysis Module

File: modules/candlestick_analyzer.py

Purpose:

- Support candlestick chart visualization
- Add moving average and volume context
- Prepare for future candlestick pattern recognition

### 7. Daily Momentum Watchlist Module

File: modules/momentum_scanner.py

Purpose:

- Identify high-momentum or high-volatility candidates
- Detect price movement and volume expansion
- Generate research watchlists, not buy recommendations

### 8. Long-Term Candidate Pool Module

File: modules/long_term_analyzer.py

Purpose:

- Organize long-term stock and ETF candidates
- Support a 3 to 5 year observation framework
- Classify assets by role, category, and risk level

### 9. AI Summary Module

File: modules/ai_summary.py

Purpose:

- Generate structured research summaries
- Explain backtest results
- Explain market signals
- Add risk reminders and disclaimers

### 10. Alert and Telegram Module

Files:

- modules/alert_engine.py
- modules/telegram_notifier.py

Purpose:

- Prepare future near real-time alert workflow
- Support Telegram push alerts in later versions
- Send market summaries and risk warnings

---

## MVP Exclusions

The MVP will not include:

- Real money trading
- Auto order execution
- Brokerage API trading
- High-frequency trading
- Guaranteed return claims
- Personalized investment advice
- Paid real-time data integration

---

## MVP Success Criteria

The MVP is complete when the project can:

1. Load ticker data
2. Calculate basic indicators
3. Run a simple backtest
4. Show a Streamlit dashboard
5. Display candlestick and performance charts
6. Generate a structured AI-style research summary
7. Include clear risk disclaimers
8. Maintain modular architecture for future upgrades
