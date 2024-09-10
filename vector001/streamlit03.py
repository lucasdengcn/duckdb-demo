import streamlit as st
import yfinance as yf
import pandas as pd

st.title('简单股票查看器')

# 用户输入股票代码
ticker_symbol = st.text_input('请输入股票代码(例如: AAPL, GOOGL):', 'AAPL')

# 获取股票数据
ticker_data = yf.Ticker(ticker_symbol)
ticker_df = ticker_data.history(period='1d', start='2010-5-31', end='2023-5-31')

# 显示股票信息
st.write(f"## {ticker_symbol}的股票信息")
st.dataframe(ticker_df)

# 显示股票图表
st.line_chart(ticker_df.Close)

# 显示公司信息
st.write(f"## {ticker_symbol}的公司信息")
st.write(ticker_data.info)
