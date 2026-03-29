import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ==============================
# 🎨 CONFIG + DARK THEME
# ==============================
st.set_page_config(page_title="Crypto Trading Dashboard", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.block-container {
    padding-top: 1rem;
}
.card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)
# ==============================
# 📊 STATE
# ==============================
if "positions" not in st.session_state:
    st.session_state.positions = []

if "balance" not in st.session_state:
    st.session_state.balance = 10000

# ==============================
# 📡 DATA
# ==============================
def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        return float(requests.get(url).json()["price"])
    except:
        return 60000

def get_chart_data(symbol, interval):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": 100}
    data = requests.get(url, params=params).json()

    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df[0], unit="ms")
    df["close"] = df[4].astype(float)

    return df[["time", "close"]]

# ==============================
# 🎛 SIDEBAR
# ==============================
st.sidebar.title("⚙ Settings")

symbol = st.sidebar.selectbox("Pair", ["BTCUSDT", "ETHUSDT"], key="pair")
interval = st.sidebar.selectbox("Timeframe", ["1m", "5m", "1h", "1d"], key="tf")

# ==============================
# 📡 FETCH DATA
# ==============================
with st.spinner("Loading market data..."):
    price = get_price(symbol)
    df = get_chart_data(symbol, interval)

# ==============================
# 📈 HEADER
# ==============================
st.title("📈 Crypto Trading Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Price", f"${price:,.2f}")
col2.metric("💼 Balance", f"${st.session_state.balance:,.2f}")
col3.metric("📊 Positions", len(st.session_state.positions))

# ==============================
# 📊 CHART
# ==============================
st.line_chart(df.set_index("time"))

# ==============================
# ⚡ TRADE PANEL
# ==============================
left, right = st.columns([2, 1])

with right:
    st.markdown("### ⚡ Trade Panel")

    st.text_input("Market Price", value=f"{price}", disabled=True, key="market_price")

    trade_price = st.number_input(
        "Price",
        value=float(price),
        key="price_input"
    )

    qty = st.number_input(
        "Quantity",
        min_value=0.001,
        value=0.01,
        key="qty_input"
    )

    stop_loss = st.number_input(
        "Stop Loss",
        value=float(price - 100),
        key="sl_input"
    )

    total = trade_price * qty
    st.markdown(f"**Total:** ${total:.2f}")

    colb1, colb2 = st.columns(2)

    if colb1.button("🟢 BUY", key="buy_btn"):
        st.session_state.positions.append({
            "symbol": symbol,
            "price": trade_price,
            "qty": qty,
            "side": "BUY",
            "pnl": 0
        })
        st.success("Buy executed (simulated)")

    if colb2.button("🔴 SELL", key="sell_btn"):
        st.session_state.positions.append({
            "symbol": symbol,
            "price": trade_price,
            "qty": qty,
            "side": "SELL",
            "pnl": 0
        })
        st.success("Sell executed (simulated)")



        # ==============================
# 📊 LEFT PANEL (MARKET + STATS)
# ==============================
with left:
    st.markdown("### 📊 Market Overview")

    # Price stats
    colA, colB = st.columns(2)

    colA.metric("Current Price", f"${price:,.2f}")

    # Fake 24h change (can improve later)
    change = round((df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0] * 100, 2)
    colB.metric("24h Change", f"{change}%", delta=f"{change}%")

    # High / Low
    high = df["close"].max()
    low = df["close"].min()

    colC, colD = st.columns(2)
    colC.metric("High", f"${high:,.2f}")
    colD.metric("Low", f"${low:,.2f}")

    st.markdown("---")

    # ==============================
    # 📋 OPEN POSITIONS (COMPACT)
    # ==============================
    st.markdown("### 📋 Open Positions")

    if st.session_state.positions:
        for pos in st.session_state.positions[-3:]:  # last 3 trades
            pnl_color = "green" if pos["pnl"] >= 0 else "red"

            st.markdown(f"""
            <div class="card">
                <b>{pos['symbol']}</b> ({pos['side']})<br>
                Qty: {pos['qty']}<br>
                Entry: ${pos['price']}<br>
                <span style="color:{pnl_color}">
                PnL: ${pos['pnl']:.2f}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active trades")

    st.markdown("---")

    # ==============================
    # 💡 QUICK INSIGHTS
    # ==============================
    st.markdown("### 💡 Insights")

    trend = "Bullish 📈" if change > 0 else "Bearish 📉"

    st.markdown(f"""
    <div class="card">
    Trend: <b>{trend}</b><br>
    Volatility: {round(high - low, 2)}<br>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# 📊 SUMMARY
# ==============================
st.markdown("### 📊 Trade Summary")

total_pnl = 0

for pos in st.session_state.positions:
    if pos["side"] == "BUY":
        pnl = (price - pos["price"]) * pos["qty"]
    else:
        pnl = (pos["price"] - price) * pos["qty"]

    pos["pnl"] = pnl
    total_pnl += pnl

pnl_color = "green" if total_pnl >= 0 else "red"

st.markdown(f"""
<div class="card">
    <h3>Total PnL:
    <span style="color:{pnl_color}">
    ${total_pnl:.2f}
    </span></h3>
</div>
""", unsafe_allow_html=True)

# ==============================
# 📋 POSITIONS
# ==============================
if st.session_state.positions:
    st.dataframe(pd.DataFrame(st.session_state.positions))

# ==============================
# ⏱ TIMESTAMP
# ==============================
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")