import csv
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
code='META'
stock = pdr.get_data_yahoo(code,'2022-01-01','2022-08-31')
print(stock)
stock.to_csv('stocklist.csv')


import pandas_datareader
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from matplotlib.ticker import MultipleLocator
code='META'
stock = pandas_datareader.get_data_yahoo(code,'2022-01-01','2022-08-31')
stock.to_csv('stocklist.csv')
df = pd.read_csv('stocklist1.csv',encoding='gbk',index_col=0)
fig, ax = plt.subplots(figsize=(10, 8))
xmajorLocator =MultipleLocator(5)
#set the scale value of x-axis as the multiple of 5
ax.xaxis.set_major_locator(xmajorLocator)
candlestick2_ochl(ax=ax, opens=df["Open"].values,closes=df["Close"].values,
                  highs=df["High"].values, lows=df["Low"].values,width=0.75, colorup='red',
                  colordown='green')
df['Close'].rolling(window=3).mean().plot(color="red",label='3day moving average line')
df['Close'].rolling(window=5).mean().plot (color="blue",label='5day moving average line')
df['Close'].rolling(window=10).mean().plot (color="green",label='10day moving average line')
plt.legend(loc='best')#draw the graph
ax.grid(True)#with grid line
plt.title("Meta candlestick line")
plt.setp(plt.gca().get_xticklabels(), rotation=30)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from matplotlib.ticker import MultipleLocator
df = pd.read_csv('stocklist.csv')
#read the stocklist from the csv file
figure,(axPrice, axVol) = plt.subplots(2, sharex=True, figsize=(15,8))
#set up the size and share the x axis
candlestick2_ochl(ax = axPrice, opens=df["Open"].values,closes=df["Close"].values, highs=df["High"].values, lows=df["Low"].values,
                  width=0.75, colorup='red', colordown='green')
axPrice.set_title("Meta stock candle stick line and the moving average line")
#set up the title
df['Close'].rolling(window=3).mean().plot(ax=axPrice,color="red",label='3day moving average line ')
df['Close'].rolling(window=5).mean().plot (ax=axPrice,color="blue",label='5day moving average line')
df['Close'].rolling(window=10).mean().plot (ax=axPrice,color="green",label='10day moving average line')
axPrice.legend(loc='best')
axPrice.set_ylabel("price(unit:dollar)")
axPrice.grid(True)
#with the grid line
for index, row in df.iterrows():
   if(row['Close'] >= row['Open']):
      axVol.bar(row['Date'],row['Volume']/1000000,width = 0.5,color='red')
   else:
      axVol.bar(row['Date'],row['Volume']/1000000,width = 0.5,color='green')
axVol.set_ylabel("trading volume (unit:ten thousand)")
#set up x-axis title
axVol.set_title("META trading volume")
axVol.set_ylim(0,df['Volume'].max()/1000000*1.2)
xmajorLocator =MultipleLocator(5)
axVol.xaxis.set_major_locator(xmajorLocator)
axVol.grid(True) #with the grid line
for xtick in axVol.get_xticklabels():
    xtick.set_rotation(15)
plt.show()

   #histogram shows  trading volume use for loop to processing different color
 # know we get the trading value and the the 3,5,10 average line, so we can use data frame to


#buy point
import pandas as pd
df = pd.read_csv('stocklist.csv')
#read the data from the stocklist.csv
malist = [3,5,10]
for ma in malist:
    df['MA_' + str(ma)] = df['Close'].rolling(window=ma).mean()
print(df)
day=0
while day<=len(df)-1:
    try:
        if df.iloc[day]['Close']<df.iloc[day+1]['Close'] and df.iloc[day+1]['Close']<df.iloc[day+2]['Close']:
#rule1: closing price keep decrease for 3 days
            if df.iloc[day]['MA_5']<df.iloc[day+1]['MA_5'] and df.iloc[day+1]['MA_5']<df.iloc[day+2]['MA_5']:
                #rule2: 5days average line keep decrease for 3 days
                if df.iloc[day+1]['MA_5']>df.iloc[day]['Close'] and df.iloc[day+2]['MA_5']<df.iloc[day+1]['Close']:
                   #rule3: the third day's closeing price is lower than the 5 days average
                    print("Buy Point on:" + df.iloc[day]['Date'])
    except:
        pass
    day=day+1
#incase there are some days have no five days average lines, so use except to deal with it


#sell point
df = pd.read_csv('stocklist.csv')
#read the data from the stocklist.csv
malist = [3,5,10]
for ma in malist:
    df['MA_' + str(ma)] = df['Close'].rolling(window=ma).mean()
day=0
while day<=len(df)-1:
    try:
        if df.iloc[day]['Close']>df.iloc[day+1]['Close'] and df.iloc[day+1]['Close']<df.iloc[day+2]['Close']:
#rule1: closing price keep decrease for 3 days
            if df.iloc[day]['MA_5']>df.iloc[day+1]['MA_5'] and df.iloc[day+1]['MA_5']>df.iloc[day+2]['MA_5']:
                #rule2: 5days average line keep decrease for 3 days
                if df.iloc[day+1]['MA_5']<df.iloc[day]['Close'] and df.iloc[day+2]['MA_5']>df.iloc[day+1]['Close']:
                   #rule3: the third day's closeing price is lower than the 5 days average
                    print("Sell Point on:" + df.iloc[day]['Date'])
    except:
        pass
    day=day+1
#incase there are some days have no five days average lines, so use except to deal with it


