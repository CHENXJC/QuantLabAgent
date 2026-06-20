# QuantLab Agent Local Showcase Checklist

This checklist is used before publishing or updating the GitHub showcase version.

## 1. Dashboard Run Check

Run:

streamlit run app.py

Open:

http://localhost:8501

Check:

- Dashboard opens successfully
- No Streamlit fatal error
- Sidebar is visible
- Language toggle is visible
- Default language is 中文
- English mode can be selected

---

## 2. Chinese Dashboard Check

Recommended setting:

- Language: 中文
- Ticker: SPY
- Period: 1y
- Interval: 1d
- Initial capital: 10000
- Risk-free rate: 0

Check:

- 运行 QuantLab 分析 button works
- 总览 tab works
- 图表 tab works
- 回测与风险 tab works
- AI 总结 tab works
- 原始数据 tab works

---

## 3. Multi-Asset Check

Test tickers:

- SPY
- AAPL
- BTC-USD

For each ticker, check:

- Market Snapshot loads
- Technical Indicator Snapshot loads
- Strategy Signal loads
- Candlestick Snapshot loads
- Charts render
- Risk metrics render
- AI Summary renders

---

## 4. Screenshot Pack Check

Recommended files:

- portfolio/showcase_screenshots/01_cn_overview_spy.png
- portfolio/showcase_screenshots/02_candlestick_chart_spy.png
- portfolio/showcase_screenshots/03_backtest_risk_spy.png
- portfolio/showcase_screenshots/04_ai_summary_spy.png
- portfolio/showcase_screenshots/05_english_overview_spy.png
- portfolio/showcase_screenshots/06_btc_overview_cn.png

Screenshot rules:

- No API keys
- No private tokens
- No personal/private data
- No private local path in visible UI
- Sidebar visible if useful
- Browser zoom around 90% to 100%
- Prefer Chinese screenshots as the main README display

---

## 5. File Safety Check

Check these files before GitHub publishing:

- .env should not be uploaded
- .env.example should contain placeholders only
- outputs/ should not include private reports
- API keys should not appear in README
- Telegram token should not appear in code
- OpenAI API key should not appear in code
- Local personal files should not appear in screenshots

Recommended command:

Select-String -Path *.py,README.md,.env.example -Pattern "OPENAI_API_KEY|TELEGRAM_BOT_TOKEN|sk-|your_api_key"

---

## 6. README Check

Check README includes:

- Project positioning
- Core features
- Dashboard preview section
- Demo flow
- Project structure
- Tech stack
- How to run locally
- Current MVP status
- Future roadmap
- Safety boundary
- Disclaimer

---

## 7. Portfolio Message Check

The project should be described as:

AI-assisted quant research dashboard for educational research, strategy simulation, and portfolio demonstration.

The project should not be described as:

- Trading bot
- Guaranteed return system
- Auto-order execution system
- Personalized financial advisor
- High-frequency trading system

---

## 8. Final Local Status

Current showcase checkpoint:

QUANTLAB-015 - Showcase Screenshot Pack + README Polish

Status:

Ready for screenshot capture and GitHub showcase preparation.
