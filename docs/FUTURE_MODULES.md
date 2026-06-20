# Future Modules

This document records future extension ideas for QuantLab Agent.

The project is designed with a modular structure so new functions can be added without rewriting the whole system.

---

## 1. Real-time Market Data Module

Potential files:

- modules/realtime_data_loader.py
- modules/websocket_client.py

Purpose:

- Support real-time or near real-time market data
- Connect to paid market data APIs
- Prepare for WebSocket streaming
- Improve alert quality

---

## 2. Telegram Alert Module

Potential files:

- modules/telegram_notifier.py
- modules/alert_engine.py

Purpose:

- Send daily market summaries
- Send risk alerts
- Send Daily Momentum Watchlist
- Send strategy signal changes

---

## 3. News Sentiment Module

Potential file:

- modules/news_sentiment.py

Purpose:

- Collect public market news
- Summarize catalysts
- Detect sentiment changes
- Explain potential reasons behind momentum moves

---

## 4. ETF Rotation Module

Potential file:

- modules/etf_rotation.py

Purpose:

- Compare ETF momentum
- Rank ETFs by trend and risk
- Support medium-term observation
- Avoid presenting outputs as financial advice

---

## 5. Long-Term Asset Framework

Potential file:

- modules/long_term_analyzer.py

Purpose:

- Build 3 to 5 year observation framework
- Categorize assets as core, satellite, or high-risk
- Compare stocks, ETFs, and crypto assets
- Provide risk-aware research summaries

---

## 6. PDF Report Export

Potential file:

- modules/pdf_exporter.py

Purpose:

- Export research summaries
- Export strategy backtest reports
- Export watchlist summaries
- Improve portfolio presentation

---

## 7. OpenAI Research Summary Extension

Potential file:

- modules/openai_research_writer.py

Purpose:

- Generate deeper AI research summaries
- Explain backtesting results
- Translate technical metrics into readable insights
- Add risk and limitation statements

---

## 8. Cloud Deployment

Potential future direction:

- Deploy dashboard online
- Schedule automatic scans
- Send daily Telegram push alerts
- Keep private credentials outside GitHub

---

## 9. Safety Boundary

Future modules should not include:

- Real-money auto trading
- Guaranteed return systems
- High-frequency trading
- Personalized financial advice
- Hidden brokerage execution
