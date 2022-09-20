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
plt.show

   #histogram shows  trading volume use for loop to processing different color
