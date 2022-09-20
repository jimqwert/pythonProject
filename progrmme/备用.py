# coding=utf-8
import csv
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
code='META'
stock = pdr.get_data_yahoo(code,'2019-01-02','2019-02-01')
print(stock)
stock.to_csv('stocklist.csv')




# This is the work I have done today





