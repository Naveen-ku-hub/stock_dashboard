import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 1. Setup the Web Page Layout
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📈 Real-Time Stock Market Dashboard")

# 2. Add Sidebar Controls for the User
st.sidebar.header("Stock Settings")

# Dropdown menu to choose a company
ticker_symbol = st.sidebar.selectbox(
    "Select Stock Ticker", 
    ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
)

# Date picking boxes
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2025-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# 3. Pull Live Data from the Internet
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data

st.write(f"### Fetching data for: **{ticker_symbol}**")
df = load_data(ticker_symbol, start_date, end_date)

# If the data is found, show it!
if df.empty:
    st.error("No data found. Please check the dates or ticker symbol.")
else:
    # 4. Extract Key Numbers (Latest Price, Changes)
    latest_close = df['Close'].iloc[-1].item()
    previous_close = df['Close'].iloc[-2].item()
    price_change = latest_close - previous_close
    percent_change = (price_change / previous_close) * 100

    # Display key numbers in neat columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${latest_close:.2f}")
    col2.metric("Price Change (1 Day)", f"${price_change:.2f}", f"{percent_change:.2f}%")
    col3.metric("Trading Volume", f"{df['Volume'].iloc[-1].item():,}")

    # 5. Build an Interactive Financial Chart
    st.write("### Interactive Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Market Data"
    )])
    
    fig.update_layout(
        xaxis_rangeslider_visible=True,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 6. Optional: Checkbox to see raw spreadsheet data
    if st.checkbox("Show Raw Spreadsheet Data"):
        st.write(df.tail(10))