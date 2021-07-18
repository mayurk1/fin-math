import tradingData as td
import pandas as pd
import numpy as np
import datetime 
import matplotlib.pyplot as plt

def backtest(delta, fast, slow):
    # Create column names based on input values
    fastEMA = str(fast) + " EMA"
    slowEMA = str(slow) + " EMA"

    # Download price data
    data = td.histData.daily(ticker, delta)

    # Calculate and create EMA columns
    data[fastEMA] = data['close'].ewm(span = fast, adjust = False).mean()
    data[slowEMA] = data['close'].ewm(span = slow, adjust = False).mean()

    # Calculate and create signal column such that
    # if fast EMA > slow EMA set value to 1 else 0
    data['signal'] = 0.0
    data['signal'] = np.where(data[fastEMA] > data[slowEMA], 1.0, 0.0)

    # Create position column which is the difference 
    # in signal values between days
    data['position'] = data['signal'].diff()

    # Grab prices at signals
    data['return'] = data['position']*data['close']*-1
    returns = data['return'].sum()
    #print(data['return'])

    r = data['return'].tolist()
    found = False
    i = 0
    initial = 1.0
    while ((i < len(r)) and found == False):
        if r[i] < 0.0:
            initial = r[i]
            found = True
        i += 1

    neg_count = len(list(filter(lambda x: (x < 0), r)))
    pos_count = len(list(filter(lambda x: (x > 0), r)))

    dollars = 0.0
    if neg_count == pos_count:
        dollars = np.nansum(r)
    else:
        chop = 0.0
        for y in r:
            if  not np.isnan(y) and int(y) < 0:
                #print(y)
                chop = y
        dollars = np.nansum(r) - chop
    #print(chop)
    #print(dollars)

    # Console output
    print(ticker)
    print("EMA Delta: " + str(delta))
    percent = dollars / initial * -100
    print('%.2f' % percent + "% Return")

    # Plot close prices and EMAs
    plt.figure(figsize = (20,10))
    data['close'].plot(color = 'k', lw = 1, label = 'Close Price')
    data[fastEMA].plot(color = 'b', lw = 1, label = fastEMA)
    data[slowEMA].plot(color = 'g', lw = 1, label = slowEMA)

    # Plot buy and sell signals
    plt.plot(data[data['position'] == 1].index, data[fastEMA][data['position'] == 1], '^', markersize = 7, color = 'g', label = 'buy')
    plt.plot(data[data['position'] == -1].index, data[fastEMA][data['position'] == -1], 'v', markersize = 7, color = 'r', label = 'sell')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.title(ticker + ' EMA Crossover Last ' + str(delta) + ' Days')
    plt.legend()
    plt.grid()
    plt.show()  
    
ticker = "MRNA"
backtest(200, 20, 50)
