import matplotlib.pyplot as plt
def drawk(open,close,high,low,pos)
    if close > open  #the closing price higher than the opining price, price rise
        myColor='red'
        myHeight=close-open
        myBottom=close
    else:             #the price fall
        myColor='green'
        myHeight=open-close
        myBottom=close
    #use the oping price and closing price to draw a square
    plt.bar(pos, height=myHeight,bottom=myBottom, width)
    #draw the up and down hatch base on the highest and lowest price
    plt.vlines(pos, high, low, myColor)
#define the time range
day = ['20190422','20190423','']
