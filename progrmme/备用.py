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
#draw the graph of the trading volume
#histogram shows  trading volume use for loop to processing different color
axVol.set_title("META trading volume") #set up x-axis title
axVol.set_ylim(0,df['Volume'].max()/1000000*1.2)
xmajorLocator =MultipleLocator(5)
axVol.xaxis.set_major_locator(xmajorLocator)
axVol.grid(True) #with the grid line
for xtick in axVol.get_xticklabels():
    xtick.set_rotation(15)
plt.show()




