# 🚀 Binance Futures Trading Bot

## 📌 Overview
A modular Python trading bot for Binance Futures Testnet with CLI interface, logging, validation, and a modern Streamlit dashboard.
---
## ✨ Features
* MARKET & LIMIT orders
* BUY / SELL support
* CLI interface (Typer)
* Input validation
* Structured logging
* Retry mechanism
* Dry-run simulation mode
* Streamlit trading dashboard (bonus UI)
---
## Setup
```bash
git clone <repo-url>
cd trading_bot
pip install -r requirements.txt
```

---
## 🔑 Environment Variables

Create `.env` file:

```
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
```
---
## ▶️ Run CLI

### MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

### LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.01 --price 60000
```

---
## 📊 Run Dashboard

```bash
streamlit run app.py
```
---
## 🧪 Example Output

```
Order request: {...}
API Request: {...}
Response:
{
  orderId: ...
  status: ...
}
```
---
## 🧠 Assumptions
* Binance Futures Testnet is used
* Orders are simulated if API fails
* Network/API instability handled via retries
---
## 📝 Logging
Logs are stored in:

```
logs/trading_bot.log
```
---
### Note on Binance Testnet
The application supports real trading via Binance Futures Testnet.
However, due to inconsistent API authentication issues observed during testing,
a dry-run simulation mode has been implemented to ensure reliable execution
and demonstration of trading logic.
Logs demonstrate correct order construction and execution flow.
---
## 🛠 Tech Stack
* Python
* Streamlit
* Binance API
* Logging module

* <img width="1917" height="913" alt="Screenshot 2026-03-29 191719" src="https://github.com/user-attachments/assets/8df99dfc-a2f3-45f3-8e48-dab1d9b945df" />

