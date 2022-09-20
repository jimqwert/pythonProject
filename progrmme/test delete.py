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




# !/usr/bin/env python
# coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader
from mpl_finance import candlestick2_ochl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter
# 计算KDJ
def calKDJ(df):
    df['MinLow'] = df['Low'].rolling(9, min_periods=9).min()
    # 填充NaN数据
    df['MinLow'].fillna(value = df['Low'].expanding().min(), inplace = True)
    df['MaxHigh'] = df['High'].rolling(9, min_periods=9).max()
    df['MaxHigh'].fillna(value = df['High'].expanding().max(), inplace = True)
    df['RSV'] = (df['Close'] - df['MinLow']) / (df['MaxHigh'] - df['MinLow']) * 100
    for i in range(len(df)):
        if i==0:    # 第一天
            df.loc[i,'K']=50
            df.loc[i,'D']=50
        if i>0:
            df.loc[i,'K']=df.loc[i-1,'K']*2/3 + 1/3*df.loc[i,'RSV']
            df.loc[i,'D']=df.loc[i-1,'D']*2/3 + 1/3*df.loc[i,'K']
        df.loc[i,'J']=3*df.loc[i,'K']-2*df.loc[i,'D']
    return df
# 绘制KDJ线
def drawKDJAndKLine(stockCode,startDate,endDate):
    filename='stockData'+stockCode+startDate+endDate+'.csv'
    getStockDataFromAPI(stockCode,startDate,endDate)
    df = pd.read_csv(filename,encoding='gbk')
    stockDataFrame = calKDJ(df)
    # 创建子图
    (axPrice, axKDJ) = figure.subplots(2, sharex=True)
    # 调用方法，在axPrice子图中绘制K线图
    candlestick2_ochl(ax = axPrice,
                  opens=stockDataFrame["Open"].values, closes=stockDataFrame["Close"].values,
                  highs=stockDataFrame["High"].values, lows=stockDataFrame["Low"].values,
                  width=0.75, colorup='red', colordown='green')
    axPrice.set_title("candlestick line and average line graph")    # 设置子图标题
    stockDataFrame['Close'].rolling(window=3).mean().plot(ax=axPrice,color="red",label='3日均线')
    stockDataFrame['Close'].rolling(window=5).mean().plot(ax=axPrice,color="blue",label='5日均线')
    stockDataFrame['Close'].rolling(window=10).mean().plot(ax=axPrice,color="green",label='10日均线')
    axPrice.legend(loc='best')      # 绘制图例
    axPrice.set_ylabel("price（unit：dollar）")
    axPrice.grid(linestyle='-.')    # 带网格线
    # 在axKDJ子图中绘制KDJ
    stockDataFrame['K'].plot(ax=axKDJ,color="blue",label='K')
    stockDataFrame['D'].plot(ax=axKDJ,color="green",label='D')
    stockDataFrame['J'].plot(ax=axKDJ,color="purple",label='J')
    plt.legend(loc='best')          # 绘制图例
    axKDJ.set_title("KDJ图")        # 设置子图的标题
    axKDJ.grid(linestyle='-.')      # 带网格线
    # 设置x轴坐标的标签和旋转角度
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
# 设置tkinter窗口
win = tkinter.Tk()
win.geometry('625x600')     # 设置大小
win.title("candlestick line integrate KDJ")
# 放置控件
tkinter.Label(win,text='stockcode：').place(x=10,y=20)
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
startDateEntry.insert(0,'2019-01-05')
endDateEntry = tkinter.Entry(win,textvariable=endDateVal)
endDateEntry.place(x=70,y=80)
endDateEntry.insert(0,'2019-02-05')
def draw():     # 绘制按钮触发的处理函数（或方法）
    plt.clf()   # 先清空所有在plt上的图形
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
# 开始整合figure和win
figure = plt.figure()
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().config(width=575,height=500)
canvas.get_tk_widget().place(x=0,y=100)
win.mainloop()


# 以对话框的形式输出买点
def printBuyPoints():
    stockCode=stockCodeVal.get()
    startDate=startDateVal.get()
    endDate=endDateVal.get()
    filename='stockData'+stockCode+startDate+endDate+'.csv'
    getStockDataFromAPI(stockCode,startDate,endDate)
    df = pd.read_csv(filename,encoding='gbk')
    stockDf = calKDJ(df)
    cnt=0
    buyDate=''
    while cnt<=len(stockDf)-1:
        if(cnt>=5):     # 略过前几天的误差
            #规则1：前一天J值大于10，当天J值小于10，是买点、
            if stockDf.iloc[cnt]['J']<10 and stockDf.iloc[cnt-1]['J']>10:
                buyDate = buyDate+stockDf.iloc[cnt]['Date'] + ','
                cnt=cnt+1
                continue
            # 规则2：K,D均在20之下，出现K线上穿D线的金叉现象
            # 规则1和规则2是“或”的关系，所以当满足规则1时直接continue
            if stockDf.iloc[cnt]['K']>stockDf.iloc[cnt]['D'] and stockDf.iloc[cnt-1]['D']>stockDf.iloc[cnt-1]['K']:
                # 满足上穿条件后再判断K和D均小于20
                if stockDf.iloc[cnt]['K']< 20 and stockDf.iloc[cnt]['D']<20:
                    buyDate = buyDate + stockDf.iloc[cnt]['Date'] + ','
        cnt=cnt+1
    # 完成后，通过对话框的形式显示买入日期
    tkinter.messagebox.showinfo('提示买点',buyDate)
tkinter.Button(win,text='计算买点',width=12,command=printBuyPoints).place(x=300,y=50)
# 开始整合figure和win
figure = plt.figure()
canvas = FigureCanvasTkAgg(figure, win)
canvas.get_tk_widget().config(width=575,height=500)
canvas.get_tk_widget().place(x=0,y=100)
win.mainloop()



