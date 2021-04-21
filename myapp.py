import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import yfinance as yf 

st.title("National Stock Exchange (NSE) Stock Price analysis")
st.sidebar.title("Select Stock from below lists")
st.markdown("### This application is purely for educational purpose")
st.sidebar.markdown("Shareprice dashboard to Analyse the stocks")

st.write("""
	Chart 
	""")

st.sidebar.title("Select Stock")
stocksymbol = st.sidebar.text_input('Write stock symbol: ','SBIN').upper()
stocksymbol = stocksymbol+'.NS'
# select = st.sidebar.selectbox('Select stocks', ['DLF.NS','SBIN.NS','ITC.NS'], key='1')
timeframe = st.sidebar.selectbox('Timeframe',['60m', '5m', '15m', '30m', '90m','1d', '5d', '1wk', '1mo'])
period = st.sidebar.slider('select no of days',1,60,5)
period = str(period) + 'd'


# print(stocksymbol)

tickerSymbol = stocksymbol
# print(tickerSymbol)


tickerData = yf.Ticker(tickerSymbol)


tickerDf = tickerData.history(period = period,interval = timeframe)
tickerDf.reset_index(level=0, inplace=True)

tickerDf.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends',
       'Stock Splits']
# build complete timepline from start date to end date
dt_all = pd.date_range(start=tickerDf['Date'].iloc[0],end=tickerDf['Date'].iloc[-1])

# retrieve the dates that ARE in the original datset
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(tickerDf['Date'])]

# define dates with missing values
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]              
# avg_20 = tickerDf.Close.rolling(window=20, min_periods=1).mean()
# avg_50 = tickerDf.Close.rolling(window=50, min_periods=1).mean()
# avg_200 = tickerDf.Close.rolling(window=200, min_periods=1).mean()
# print(avg_20)
set1 = { 'x': tickerDf.Date, 'open': tickerDf.Open, 'close': tickerDf.Close, 'high': tickerDf.High, 'low': tickerDf.Low, 'type': 'candlestick'}
# set2 = { 'x': tickerDf.Date, 'y': avg_20, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'MA 20 periods'}
# set3 = { 'x': tickerDf.Date, 'y': avg_50, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'black' },'name': 'MA 50 periods'}
# set4 = { 'x': tickerDf.Date, 'y': avg_200, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'yellow' },'name': 'MA 200 periods'}
data = [set1]

fig = go.Figure(data=data)
# fig.layout = dict(title=select, xaxis = dict(type="category"))
fig.update_layout(xaxis_rangeslider_visible=False,title= stocksymbol,height = 600, width = 900,autosize = False)
# fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)]) # hide dates with no values

fig.update_xaxes(
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )

# print(tickerData.financials)
st.plotly_chart(fig,use_container_width=False)

st.write(tickerDf.tail(20))