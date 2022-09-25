#this is how to spide the stock data from the yahoo and stock as csv file
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
df = pd.read_csv('/Users/pangyifan/pythonProject2/progrmme/stocklist.csv') #read the data from the csv file
fig = plt.figure()
ax = fig.add_subplot(111)   #set up a position for the candlestick line
candlestick2_ochl (ax=ax, opens=df["Open"].values, closes=df["Close"].values, highs=df["High"].values,lows=df["Low"].values,width=0.75, colorup='red', colordown='green')
#use candlestick_ochl to draw the picture
plt.xticks(range(len(df.index.values)),df.index.values,rotation=30 )
ax.grid(True) #set gridlines
plt.title("META candlestick line")  #title for the graph
plt.show()
#start draw the MACD line


import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
df = pd.read_csv('/Users/pangyifan/pythonProject2/progrmme/stocklist.csv')
#read the stock data from the csv file
fig =plt.figure()
ax = fig.add_subplot(111)
#set up the position of the graph
candlestick2_ochl(ax = ax,opens=df["Open"].values, closes=df["Close"].values, highs=df["High"].values, lows=df["Low"].values,width=0.75, colorup='red',colordown='green')
df['Close'].rolling(window=3).mean().plot (color="red",label='3day moving average line')
df['Close'].rolling(window=5).mean().plot (color="red",label='5day moving average line')
df['Close'].rolling(window=10).mean().plot (color="red",label='10day moving average line')
plt.legend(loc='best') # darw the graph
#set up a x-axis
plt.xticks(range(len(df.index.values)),df.index.values,rotation=30 )
ax.grid(True)#draw the grid line
plt.title("META candlestick line")
plt.show()
#this is what i done for the candlestick line and three average line for the stock data
#next graph i need draw is the Volume








