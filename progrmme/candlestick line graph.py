import csv
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
code='META'
stock = pdr.get_data_yahoo(code,'2022-06-01','2022-08-31')
print(stock)
stock.to_csv('stocklist.csv')


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
plt.legend(loc='best') # draw the graph
#set up a x-axis
plt.xticks(range(len(df.index.values)),df.index.values,rotation=30 )
ax.grid(True)#draw the grid line
plt.title("META candlestick line")
plt.show()



import pandas_datareader
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from matplotlib.ticker import MultipleLocator
code='META'
stock = pandas_datareader.get_data_yahoo(code,'2022-06-01','2022-08-31')
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



import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader
from mpl_finance import candlestick2_ochl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter
import tkinter.messagebox
# calculate KDJ
def calKDJ(df):
    df['MinLow'] = df['Low'].rolling(9, min_periods=9).min()
    # input NaN data
    df['MinLow'].fillna(value = df['Low'].expanding().min(), inplace = True)
    df['MaxHigh'] = df['High'].rolling(9, min_periods=9).max()
    df['MaxHigh'].fillna(value = df['High'].expanding().max(), inplace = True)
    df['RSV'] = (df['Close'] - df['MinLow']) / (df['MaxHigh'] - df['MinLow']) * 100
    for i in range(len(df)):
        if i==0:    # first day
            df.loc[i,'K']=50
            df.loc[i,'D']=50
        if i>0:
            df.loc[i,'K']=df.loc[i-1,'K']*2/3 + 1/3*df.loc[i,'RSV']
            df.loc[i,'D']=df.loc[i-1,'D']*2/3 + 1/3*df.loc[i,'K']
        df.loc[i,'J']=3*df.loc[i,'K']-2*df.loc[i,'D']
    return df
# draw KDJ line
def drawKDJAndKLine(stockCode,startDate,endDate):
    filename='stockData'+stockCode+startDate+endDate+'.csv'
    getStockDataFromAPI(stockCode,startDate,endDate)
    df = pd.read_csv(filename,encoding='gbk')
    stockDataFrame = calKDJ(df)
    # create subgraph
    (axPrice, axKDJ) = figure.subplots(2, sharex=True)
    # use candledtick2_ochl to draw the candlestick line in the axPrice graph
    candlestick2_ochl(ax = axPrice,
                  opens=stockDataFrame["Open"].values, closes=stockDataFrame["Close"].values,
                  highs=stockDataFrame["High"].values, lows=stockDataFrame["Low"].values,
                  width=0.75, colorup='red', colordown='green')
    axPrice.set_title("candlestick line and average line")    # set the title of the subgraph
    stockDataFrame['Close'].rolling(window=3).mean().plot(ax=axPrice,color="red",label='3days average line')
    stockDataFrame['Close'].rolling(window=5).mean().plot(ax=axPrice,color="blue",label='5days average line')
    stockDataFrame['Close'].rolling(window=10).mean().plot(ax=axPrice,color="green",label='10days average line')
    axPrice.legend(loc='best')      # draw the graph in the suitable position
    axPrice.set_ylabel("price（unit：dollar）")
    axPrice.grid(linestyle='-.')    # with grid line
    # draw the KDJ in the ax KDJ
    stockDataFrame['K'].plot(ax=axKDJ,color="blue",label='K')
    stockDataFrame['D'].plot(ax=axKDJ,color="green",label='D')
    stockDataFrame['J'].plot(ax=axKDJ,color="purple",label='J')
    plt.legend(loc='best')          # draw the graph
    axKDJ.set_title("KDJ graph")        # set up the title of the KDJ graph
    axKDJ.grid(linestyle='-.')      # with grid line
    major_index=stockDataFrame.index[stockDataFrame.index%5==0]
    major_xtics=stockDataFrame['Date'][stockDataFrame.index%5==0]
    plt.xticks(major_index,major_xtics)
    plt.setp(plt.gca().get_xticklabels(), rotation=30)   # set up x-axis coord and the rotation degrees

def getStockDataFromAPI(stockCode,startDate,endDate):    #get the stock data from the API
    try:
        stock = pandas_datareader.get_data_yahoo(stockCode,startDate,endDate)
        if(len(stock)<1):
            #if didn't get the data, it will be exception
            raise Exception()

        stock.drop(stock.index[len(stock)-1],inplace=True)
         #delete the last stock data line, because the get_data_yahoo will get extra one more data
        filename='stockData'+stockCode+startDate+endDate+'.csv'  #download a copy of the scv file
        stock.to_csv(filename)
    except Exception as e:
        print('Error when getting the data of:' + stockCode)
        print(repr(e))
# set up tkinter window
win = tkinter.Tk()
win.geometry('625x600')     # set the size of window
win.title("candlestick line integrate the average line and the KDJ")
# input the controls
tkinter.Label(win,text='stock code：').place(x=10,y=20)
tkinter.Label(win,text='start date：').place(x=10,y=50)
tkinter.Label(win,text='end date：').place(x=10,y=80)
stockCodeVal = tkinter.StringVar()
startDateVal = tkinter.StringVar()
endDateVal = tkinter.StringVar()
stockCodeEntry = tkinter.Entry(win,textvariable=stockCodeVal)
stockCodeEntry.place(x=70,y=20)
stockCodeEntry.insert(0,'META')
startDateEntry = tkinter.Entry(win,textvariable=startDateVal)
startDateEntry.place(x=70,y=50)
startDateEntry.insert(0,'2022-06-01')
endDateEntry = tkinter.Entry(win,textvariable=endDateVal)
endDateEntry.place(x=70,y=80)
endDateEntry.insert(0,'2022-08-31')
def draw():     #draw the handler function of the click button
    plt.clf()   # clean all the graph in the plt
    stockCode=stockCodeVal.get()
    startDate=startDateVal.get()
    endDate=endDateVal.get()
    drawKDJAndKLine(stockCode,startDate,endDate)
    canvas.draw()
tkinter.Button(win,text='draw',width=5,command=draw).place(x=200,y=50)
def reset():
    stockCodeEntry.delete(0,tkinter.END)
    stockCodeEntry.insert(0,'META')
    startDateEntry.delete(0,tkinter.END)
    startDateEntry.insert(0,'2022-06-01')
    endDateEntry.delete(0,tkinter.END)
    endDateEntry.insert(0,'2022-08-31')
    plt.clf()
    canvas.draw()
tkinter.Button(win,text='reset',width=5,command=reset).place(x=200,y=80)
# print out the buy point as the messagebox
def printBuyPoints():
    stockCode=stockCodeVal.get()
    startDate=startDateVal.get()
    endDate=endDateVal.get()
    filename='stockData'+stockCode+startDate+endDate+'.csv'
    getStockDataFromAPI(stockCode,startDate,endDate)
    df = pd.read_csv(filename,encoding='gbk')
    stockDf = calKDJ(df)
    day=0
    buyDate=''
    while day<=len(stockDf)-1:
        if(day>=5):
            #rule1：if the yesterday J value is greater than 10 and the J value of today is smaller than 10 it's the buy point
            if stockDf.iloc[day]['J']<10 and stockDf.iloc[day-1]['J']>10:
                buyDate = buyDate+stockDf.iloc[day]['Date'] + ','
                day=day+1
                continue
             # rule2： if the K,D average value is under 20，the k line will rise and cross the d line
            # it can continue if the rule 1 is satisfied
            if stockDf.iloc[day]['K']>stockDf.iloc[day]['D'] and stockDf.iloc[day-1]['D']>stockDf.iloc[day-1]['K']:

                if stockDf.iloc[day]['K']< 20 and stockDf.iloc[day]['D']<20:
                    # make sure determine the average value of the k and d is smaller than 20 after the k line rise and cross the d line
                    buyDate = buyDate + stockDf.iloc[day]['Date'] + ','
        day=day+1
    # show the buy date with the messagebox
    tkinter.messagebox.showinfo('show the buy point',buyDate)
tkinter.Button(win,text='calculate the buy point',width=15,command=printBuyPoints).place(x=300,y=50)
def printSellPoints():
    stockCode=stockCodeVal.get()
    startDate=startDateVal.get()
    endDate=endDateVal.get()
    filename='stockData'+stockCode+startDate+endDate+'.csv'
    getStockDataFromAPI(stockCode,startDate,endDate)
    df = pd.read_csv(filename,encoding='gbk')
    stockDf = calKDJ(df)
    day=0
    sellDate=''
    while day<=len(stockDf)-1:
        if(day>=5):
            # rule1：if yesterday j value is smaller than 100 and today j value is large than 100, it will be the sell point
            if stockDf.iloc[day]['J']>100 and stockDf.iloc[day-1]['J']<100:
                sellDate = sellDate+stockDf.iloc[day]['Date'] + ','
                day=day+1
                continue
            # rule2：K,D average volue is over80 and the k line go down and cross the d line
            if stockDf.iloc[day]['K']<stockDf.iloc[day]['D'] and stockDf.iloc[day-1]['D']<stockDf.iloc[day-1]['K']:
                # make sure determine the average value of the k and d is greater than 80 after the k line rise and cross the d line
                if stockDf.iloc[day]['K']> 80 and stockDf.iloc[day]['D']>80:
                    sellDate = sellDate + stockDf.iloc[day]['Date'] + ','
        day=day+1
    # show the sell date with the messagebox
    tkinter.messagebox.showinfo('show the sell point',sellDate)
tkinter.Button(win,text='calculate the sell point',width=15,command=printSellPoints).place(x=300,y=80)

# integrate figure and win
figure = plt.figure()
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().config(width=575,height=500)
canvas.get_tk_widget().place(x=0,y=100)
win.mainloop()


