import streamlit as st
import requests
import yfinance as yf
import re

BASE_URL = "http://localhost:8000"

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<h1 style='text-align: center;'>🤖 AI Financial Assistant</h1>
<p style='text-align: center; color: gray;'>
Analyze financial reports, stocks, and news using AI
</p>
""", unsafe_allow_html=True)

st.divider()

st.info("""
💡 You can:
- 📈 Analyze stocks → 'Analyze INFY.NS'
- 📄 Upload reports → 'Summarize this report'
- ⚠️ Risk analysis → 'What are the risks?'
- 💰 Investment advice → 'Should I invest?'
- 📰 News → 'Show latest news'
""")

# -------------------------------
# SIDEBAR STOCK
# -------------------------------
st.sidebar.header("📊 Stock Analysis")

ticker = st.sidebar.text_input("Enter Stock Symbol (e.g. INFY.NS)")

if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")

        if not hist.empty:
            close_prices = hist["Close"].dropna()

            if not close_prices.empty:
                current_price = close_prices.iloc[-1]
                first_price = close_prices.iloc[0]
                change = current_price - first_price
                percent = (change / first_price) * 100

                col1, col2 = st.sidebar.columns(2)
                col1.metric("💰 Price", f"₹{current_price:.2f}")
                col2.metric("📉 Change", f"{change:.2f} ({percent:.2f}%)")

                st.sidebar.subheader("📈 Price Trend")
                st.sidebar.line_chart(close_prices)

                if change > 0:
                    st.sidebar.success("📈 Uptrend")
                else:
                    st.sidebar.error("📉 Downtrend")

    except Exception:
        st.sidebar.error("❌ Invalid stock symbol")

# -------------------------------
# FILE UPLOAD
# -------------------------------
st.sidebar.markdown("### 📂 Upload Financial Reports")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF / TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if "uploaded_names" not in st.session_state:
    st.session_state.uploaded_names = set()

if uploaded_files:
    for file in uploaded_files:
        if file.name in st.session_state.uploaded_names:
            continue

        try:
            with st.sidebar.spinner(f"Processing {file.name}..."):
                response = requests.post(
                    f"{BASE_URL}/upload",
                    files={"file": (file.name, file.getvalue(), file.type)},
                    timeout=60
                )

                if response.status_code == 200:
                    st.sidebar.success(f"✅ {file.name} uploaded")
                    st.session_state.uploaded_names.add(file.name)
                else:
                    st.sidebar.error(f"❌ Failed: {file.name}")

        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "processing" not in st.session_state:
    st.session_state.processing = False

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.processing = False
    st.rerun()

# -------------------------------
# EMPTY STATE
# -------------------------------
if (
    not st.session_state.messages
    and not st.session_state.uploaded_names
    and not ticker
):
    st.warning("⚠️ Upload a report or analyze a stock to begin")

# -------------------------------
# DISPLAY CHAT
# -------------------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------------
# CHAT INPUT
# -------------------------------
query = st.chat_input("Ask something...")

if query and not st.session_state.processing:

    st.session_state.processing = True

    st.chat_message("user").write(query)

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[-5:]
    ]

    st.markdown("### 🤖 AI Response")

    with st.spinner("🔍 Analyzing with AI..."):
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"question": query, "history": history},
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()
                answer = data["data"]["answer"]
                sources = data["data"].get("sources", [])
            else:
                answer = "⚠️ Server error"
                sources = []

        except Exception as e:
            answer = f"❌ Error: {e}"
            sources = []

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": answer})

    st.chat_message("assistant").write(answer)

    # -------------------------------
    # SIGNAL UI (FIXED PROPERLY)
    # -------------------------------
    match = re.search(r"Investment Signal:\s*(.*)", answer)

    if match:
        signal_text = match.group(1).lower()

        if "strong" in signal_text:
            st.success("🟢 Strong Investment Signal")
        elif "moderate" in signal_text:
            st.warning("🟡 Moderate Investment Signal")
        elif "weak" in signal_text:
            st.error("🔴 Weak Investment Signal")

    # -------------------------------
    # SOURCES
    # -------------------------------
    if sources:
        st.divider()
        with st.expander("📄 Sources"):
            for s in sources:
                if isinstance(s, dict):
                    st.markdown(f"📄 **{s.get('source')}**")
                else:
                    st.markdown(f"🌐 {s}")

    st.session_state.processing = False