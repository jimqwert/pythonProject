
# !/usr/bin/env python
# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
# 计算BIAS的方法，入参periodList传入周期列表
def calBIAS(df,periodList):
    # 遍历周期，计算6,12,24日BIAS
    for period in periodList:
        df['MA'+str(period)] = df['Close'].rolling(window=period).mean()
        df['MA'+str(period)].fillna(value = df['Close'], inplace = True)
        df['BIAS'+str(period)] = (df['Close'] - df['MA'+str(period)])/df['MA'+str(period)]*100
    return df
filename='stocklist.csv'
df = pd.read_csv(filename,encoding='gbk')
list = [6,12,24]    # 周期列表
# 调用方法计算BIAS
stockDataFrame = calBIAS(df,list)
# print(stockDataFrame) # 可以去掉注释来查看结果
figure = plt.figure()
# 创建子图
(axPrice, axBIAS) = figure.subplots(2, sharex=True)
# 调用方法，在axPrice子图中绘制K线图
candlestick2_ochl(ax = axPrice,
              opens=df["Open"].values, closes=df["Close"].values,
              highs=df["High"].values, lows=df["Low"].values,
              width=0.75, colorup='red', colordown='green')
axPrice.set_title("K线图和均线图")    # 设置子图标题
stockDataFrame['Close'].rolling(window=6).mean().plot(ax=axPrice,color="red",label='6日均线')
stockDataFrame['Close'].rolling(window=12).mean().plot(ax=axPrice,color="blue",label='12日均线')
stockDataFrame['Close'].rolling(window=24).mean().plot(ax=axPrice,color="green",label='24日均线')
axPrice.legend(loc='best')      # 绘制图例
axPrice.set_ylabel("价格（单位：元）")
axPrice.grid(linestyle='-.')    # 带网格线
# 在axBIAS子图中绘制BIAS图形
stockDataFrame['BIAS6'].plot(ax=axBIAS,color="blue",label='BIAS6')
stockDataFrame['BIAS12'].plot(ax=axBIAS,color="green",label='BIAS12')
stockDataFrame['BIAS24'].plot(ax=axBIAS,color="purple",label='BIAS24')
plt.legend(loc='best')          # 绘制图例
plt.rcParams['font.sans-serif']=['SimHei']
axBIAS.set_title("BIAS指标图")  # 设置子图的标题
axBIAS.grid(linestyle='-.')     # 带网格线
# 设置x轴坐标的标签和旋转角度
major_index=stockDataFrame.index[stockDataFrame.index%5==0]
major_xtics=stockDataFrame['Date'][stockDataFrame.index%5==0]
plt.xticks(major_index,major_xtics)
plt.setp(plt.gca().get_xticklabels(), rotation=30)
plt.show()



#!/usr/bin/env python
#coding=utf-8
from django.shortcuts import render
import pandas_datareader
import matplotlib.pyplot as plt
import pandas as pd
from mpl_finance import candlestick2_ochl
import sys
from io import BytesIO
import base64
import importlib
importlib.reload(sys)

def display(request):
    return render(request, 'main.html')

# 计算BIAS的函数
def calBIAS(df,periodList):
    for period in periodList:
        df['MA'+str(period)] = df['Close'].rolling(window=period).mean()
        df['MA'+str(period)].fillna(value = df['Close'], inplace = True)
        df['BIAS'+str(period)] = (df['Close'] - df['MA'+str(period)])/df['MA'+str(period)]*100
    return df

def calBuyPoints(df):
    cnt=0
    buyDate=''
    while cnt<=len(df)-1:
        if(cnt>=30):    # 前几天有误差，从第30天算起
            # 规则1：这天中期BIAS小于或等于-7
            if df.iloc[cnt]['BIAS12']<=-7:
                buyDate = buyDate+df.iloc[cnt]['Date'] + ','
            #规则2：当天BIAS6上穿BIAS24
            if  df.iloc[cnt]['BIAS6']>df.iloc[cnt]['BIAS24'] and df.iloc[cnt-1]['BIAS6']<df.iloc[cnt-1]['BIAS24']:
                buyDate = buyDate+df.iloc[cnt]['Date'] + ','
        cnt=cnt+1
    return buyDate

def calSellPoints(df):
    cnt=0
    sellDate=''
    while cnt<=len(df)-1:
        if(cnt>=30):    #前几天有误差，从第30天算起
            # 规则1：这天中期BIAS大于等于7
            if df.iloc[cnt]['BIAS12']>=7:
                sellDate = sellDate+df.iloc[cnt]['Date'] + ','
            # 规则2：当天BIAS6下穿BIAS24
            if  df.iloc[cnt]['BIAS6']<df.iloc[cnt]['BIAS24'] and df.iloc[cnt-1]['BIAS6']>df.iloc[cnt-1]['BIAS24']:
                sellDate = sellDate+df.iloc[cnt]['Date'] + ','
        cnt=cnt+1
    return sellDate

def draw(request):
    stockCode = request.POST.get('stockCode')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    stock = pandas_datareader.get_data_yahoo(stockCode,startDate,endDate)
    # 删除最后一天多余的股票交易数据
    stock.drop(stock.index[len(stock)-1],inplace=True)
    filename='stockData'+stockCode+startDate+endDate+'.csv'
    stock.to_csv(filename)
    # 从文件中读取指定股票在指定范围内的交易数据
    df = pd.read_csv(filename,encoding='gbk')
    list = [6,12,24]    # 周期列表
    stockDataFrame = calBIAS(df,list)

    figure = plt.figure()
    (axPrice, axBIAS) = figure.subplots(2, sharex=True)
    # 绘制K线
    candlestick2_ochl(ax = axPrice,
              opens=df["Open"].values, closes=df["Close"].values,
              highs=df["High"].values, lows=df["Low"].values,
              width=0.75, colorup='red', colordown='green')
    axPrice.set_title("K线图和均线图")
    stockDataFrame['Close'].rolling(window=6).mean().plot(ax=axPrice,color="red",label='6日均线')
    stockDataFrame['Close'].rolling(window=12).mean().plot(ax=axPrice,color="blue",label='12日均线')
    stockDataFrame['Close'].rolling(window=24).mean().plot(ax=axPrice,color="green",label='24日均线')
    axPrice.legend(loc='best')      # 绘制图例
    axPrice.set_ylabel("价格（单位：元）")
    axPrice.grid(linestyle='-.')
    # 绘制BIAS指标线
    stockDataFrame['BIAS6'].plot(ax=axBIAS,color="blue",label='BIAS6')
    stockDataFrame['BIAS12'].plot(ax=axBIAS,color="green",label='BIAS12')
    stockDataFrame['BIAS24'].plot(ax=axBIAS,color="purple",label='BIAS24')
    plt.legend(loc='best')
    plt.rcParams['font.sans-serif']=['SimHei']
    axBIAS.set_title("BIAS指标图")
    axBIAS.grid(linestyle='-.')
    major_index=stockDataFrame.index[stockDataFrame.index%5==0]
    major_xtics=stockDataFrame['Date'][stockDataFrame.index%5==0]
    plt.xticks(major_index,major_xtics)
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    # 把存储在plt对象中的图形存入到buffer缓存对象中
    buffer = BytesIO()
    plt.savefig(buffer)
    plt.close()
    base64img = base64.b64encode(buffer.getvalue())
    img = "data:image/png;base64,"+base64img.decode()

    buyDate = calBuyPoints(stockDataFrame)
    sellDate = calSellPoints(stockDataFrame)

    return render(request, 'stock.html', {
            'img': img,'stockCode':stockCode,
            'buyDate':buyDate,'sellDate':sellDate
        })




