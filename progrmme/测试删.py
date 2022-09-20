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
        if df.iloc[day]['Close']>df.iloc[day+1]['Close'] and df.iloc[day+1]['Close']>df.iloc[day+2]['Close']:
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

