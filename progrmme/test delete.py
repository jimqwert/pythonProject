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

def calKDJ(df):   # caculate the KDJ
    df['MinLow'] = df['Low'].rolling(9, min_periods=9).min()
    # input the NaN data
    df['MinLow'].fillna(value = df['Low'].expanding().min(), inplace = True)
    df['MaxHigh'] = df['High'].rolling(9, min_periods=9).max()
    df['MaxHigh'].fillna(value = df['High'].expanding().max(), inplace = True)
    df['RSV'] = (df['Close'] - df['MinLow']) / (df['MaxHigh'] - df['MinLow']) * 100
    for i in range(len(df)):
        if i==0:    #  the first day
            df.loc[i,'K']=50
            df.loc[i,'D']=50
        if i>0:
            df.loc[i,'K']=df.loc[i-1,'K']*2/3 + 1/3*df.loc[i,'RSV']
            df.loc[i,'D']=df.loc[i-1,'D']*2/3 + 1/3*df.loc[i,'K']
        df.loc[i,'J']=3*df.loc[i,'K']-2*df.loc[i,'D']
    return df

def drawKDJAndKLine(stockCode,startDate,endDate): # draw the KDJ line
    filename='stockData'+stockCode+startDate+endDate+'.csv'
    getStockDataFromAPI(stockCode,startDate,endDate)
    df = pd.read_csv(filename,encoding='gbk')
    stockDataFrame = calKDJ(df)
    (axPrice, axKDJ) = figure.subplots(2, sharex=True) #create a sub graph
    #  use candlestick2_ochl to draw the candlestick line in axPrice  subgraph
    candlestick2_ochl(ax = axPrice,
                  opens=stockDataFrame["Open"].values, closes=stockDataFrame["Close"].values,
                  highs=stockDataFrame["High"].values, lows=stockDataFrame["Low"].values,
                  width=0.75, colorup='red', colordown='green')
    axPrice.set_title("candlestick line and average line graph")    # set up the axPrice graph title
    stockDataFrame['Close'].rolling(window=3).mean().plot(ax=axPrice,color="red",label='3days average line')
    stockDataFrame['Close'].rolling(window=5).mean().plot(ax=axPrice,color="blue",label='5days average line')
    stockDataFrame['Close'].rolling(window=10).mean().plot(ax=axPrice,color="green",label='10days average line')
    axPrice.legend(loc='best')      # draw the graph
    axPrice.set_ylabel("price（unit：dollar）")
    axPrice.grid(linestyle='-.')    # with the grid line
    # draw the KDJ in the axKDJ subgraph
    stockDataFrame['K'].plot(ax=axKDJ,color="blue",label='K')
    stockDataFrame['D'].plot(ax=axKDJ,color="green",label='D')
    stockDataFrame['J'].plot(ax=axKDJ,color="purple",label='J')
    plt.legend(loc='best')          # draw the graph in the suitable location
    axKDJ.set_title("KDJ graph")        # set the title of the graph
    axKDJ.grid(linestyle='-.')      # draw the grid line
    # set up the x-axis scale and the rotation degree
    major_index=stockDataFrame.index[stockDataFrame.index%5==0]
    major_xtics=stockDataFrame['Date'][stockDataFrame.index%5==0]
    plt.xticks(major_index,major_xtics)
    plt.setp(plt.gca().get_xticklabels(), rotation=30)

def getStockDataFromAPI(stockCode,startDate,endDate):#get the stock data from api
    try:

        stock = pandas_datareader.get_data_yahoo(stockCode,startDate,endDate)
        if(len(stock)<1):
            # if didn't get any data feedback, so raise exception
            raise Exception()
        stock.drop(stock.index[len(stock)-1],inplace=True)
        # delete the last line, because get_data_yahoo will get extra one day data
        filename='stockData'+stockCode+startDate+endDate+'.csv'
        stock.to_csv(filename) #download data as csvfile
    except Exception as e:
        print('Error when getting the data of:' + stockCode)
        print(repr(e))
# set up the tkinter window
win = tkinter.Tk()
win.geometry('625x600')     # set up the size
win.title("candlestick line integrate KDJ") #set up the title
tkinter.Label(win,text='stockcode：').place(x=10,y=20)  #set up the controls
tkinter.Label(win,text='startdate：').place(x=10,y=50)
tkinter.Label(win,text='enddate：').place(x=10,y=80)
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
def draw():     # draw the handler function of the click button
    plt.clf()   # delete all the graph in the plt
    stockCode=stockCodeVal.get()
    startDate=startDateVal.get()
    endDate=endDateVal.get()
    drawKDJAndKLine(stockCode,startDate,endDate)
    canvas.draw()
tkinter.Button(win,text='draw',width=12,command=draw).place(x=200,y=50)
def reset():
    stockCodeEntry.delete(0,tkinter.END)
    stockCodeEntry.insert(0,'META')
    startDateEntry.delete(0,tkinter.END)
    startDateEntry.insert(0,'2019-01-05')
    endDateEntry.delete(0,tkinter.END)
    endDateEntry.insert(0,'2019-02-05')
    plt.clf()
    canvas.draw()
tkinter.Button(win,text='reset',width=12,command=reset).place(x=200,y=80)
# integrate the figure and win
figure = plt.figure()
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().config(width=575,height=500)
canvas.get_tk_widget().place(x=0,y=100)
win.mainloop()


#  the buy point will show as the message box
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
                cnt=day+1
                continue
            # rule2： if the K,D average value is under 20，the k line will rise and cross the d line
            # it can continue if the rule 1 is satisfied
            if stockDf.iloc[day]['K']>stockDf.iloc[day]['D'] and stockDf.iloc[day-1]['D']>stockDf.iloc[day-1]['K']:

                if stockDf.iloc[day]['K']< 20 and stockDf.iloc[day]['D']<20:
                    # make sure determine the average value of the k and d is smaller than 20 after the k line rise and cross the d line
                    buyDate = buyDate + stockDf.iloc[day]['Date'] + ','
        day=day+1
    # show the buy date with the messagebox
    tkinter.messagebox.showinfo('buypoint',buyDate)
tkinter.Button(win,text='caculate buy point',width=12,command=printBuyPoints).place(x=300,y=50)
# integrate figure and win
figure = plt.figure()
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().config(width=575,height=500)
canvas.get_tk_widget().place(x=0,y=100)
win.mainloop()



