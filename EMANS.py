import tradingData as td
import twitterBot as bot
import pandas as pd
import numpy as np
import time 
import matplotlib.pyplot as plt
import os
from datetime import datetime

class EMANS:
    #data = None
    def __init__(self, ticker, passdf=None, loops=35, delta=253, getDate=False, getBuyHold=False, getReturn=False, graph=False, df=False, log=False, tweet=False):
        self.ticker = ticker
        # Number of days to add to long/short and
        # iterate through 
        # ex: [1][5,6,7,8...],[2][5,6,7,8...]...
        self.loops = loops
        # Use to pass an already run df to use
        self.passdf = passdf 
        # Total days of historical data to download
        self.delta = delta
        # Toggle to return last buy signal date
        self.getDate = getDate
        # Toggle to return buy and hold return
        self.getBuyHold = getBuyHold
        # Toggle to return best algo return
        self.getReturn = getReturn
        # Toggle to chart best return graph
        self.graph = graph
        # Toggle to return data df
        self.df = df 
        # Toggle to enable console log output
        self.log = log 
        # Toggle to enable tweeting of output
        self.tweet = tweet


    def findBestReturn(self):
        plt.style.use('seaborn')
        global data
        global closes
        # Download price data or use provided
        if isinstance(self.passdf, pd.DataFrame):
            data = self.passdf
        else:    
            data = td.histData.daily(self.ticker, self.delta)
        print("Downloaded Data")
        # Create list to make processing easier 
        closes = data['close'].tolist()
        # Enter starting EMA values
        short, long = 1, 2
        shortMax, longMax =  short + self.loops, long + self.loops
        # Set days to iterate by
        shortIt, longIt = 1, 1
        # Keep track of # of iterations
        runs = 1
        # Track best return values
        highestReturn = 0.0
        bestFast = 0
        bestSlow = 0
        # Loop through combinations, log best fast/slow values
        while short <= (shortMax):
            while long <= (longMax):
                x = self.findReturn(short, long)
                if x > highestReturn:
                    highestReturn = x
                    bestFast = short
                    bestSlow = long
                long += longIt
                runs += 1
            long = 2
            runs += 1
            short += shortIt

        # Flag if no positive returns found and set to defaults
        foundReturns = True
        if bestFast == 0 or bestSlow == 0:
            bestFast = 10
            bestSlow = 20
            foundReturns = False
            print('🚩 No positive returns found')

        # Calculate buy and hold return
        buyAndHold = (closes[-1] - closes[0])/closes[0] * 100

        # Plot best return graph if toggle selected
        # See notes from below
        #print('fast ' + str(bestFast))
        #print('slow ' + str(bestSlow))
        fastEMA = str(bestFast) + " EMA"
        slowEMA = str(bestSlow) + " EMA"
        
        data[fastEMA] = data['close'].ewm(span = bestFast, adjust = False).mean()
        data[slowEMA] = data['close'].ewm(span = bestSlow, adjust = False).mean()

        data['signal'] = 0.0
        data['signal'] = np.where(data[fastEMA] > data[slowEMA], 1.0, 0.0)
        data['position'] = data['signal'].diff()
        data['signalPrices'] = data['position']*data['close']

        # Calculate # days since last buy signal
        returnsList = data['signalPrices'].tolist()
        ls = [i for i, e in enumerate(returnsList) if e != 0]
        lastBuyIndex = max(ls)
        dateList = data.index.tolist()
        lastBuyDate = dateList[lastBuyIndex]
        lastBuyDate = datetime.strptime(str(lastBuyDate)[:10], "%Y-%m-%d")
        todayDate = datetime.today()
        # Add 1 because datetime subtraction is inclusive
        lastBuyDateDelta = ((lastBuyDate - todayDate).days + 1)*-1

        # Console output/tweet if toggle enabled
        logText = '$' + self.ticker
        logText += '\nDelta: ' + str(self.delta)
        logText += '\nTotal runs: ' + str(runs)
        logText += '\nEMA Best Return: ' + str(round(highestReturn, 2)) + "%"
        logText += '\nBuy+Hold Return: '+ str(round(buyAndHold, 2)) + "%"
        logText += "\nBest F,S Window: %d, %d" % (bestFast, bestSlow)
        logText += '\nLast Buy Signal: ' + str(lastBuyDate)
        logText += '\nDays Since Last Buy: ' + str(lastBuyDateDelta)
        if(foundReturns and (lastBuyDateDelta <= 0.5*bestFast or lastBuyDateDelta == 1)):
            logText += '\nBUY ' + str(self.ticker)
        else:
            logText += '\nDO NOT BUY ' + str(self.ticker)

        if self.log:
            print(logText)

        if self.tweet:
            bot.twitterBot(logText).tweet()

        # Plot if toggle enabled
        if self.graph == True:
            plt.figure(figsize = (20,10))
            data['close'].plot(color = 'k', lw = 1, label = 'Close Price')
            data[fastEMA].plot(color = 'b', lw = 1, label = fastEMA)
            data[slowEMA].plot(color = 'g', lw = 1, label = slowEMA)
            plt.plot(data[data['position'] == 1].index, data[fastEMA][data['position'] == 1], '^', markersize = 7, color = 'g', label = 'buy')
            plt.plot(data[data['position'] == -1].index, data[fastEMA][data['position'] == -1], 'v', markersize = 7, color = 'r', label = 'sell')
            plt.ylabel('Price')
            plt.xlabel('Date')
            plt.title(self.ticker + ' EMA Crossover Last ' + str(self.delta) + ' Days')
            plt.legend()
            plt.grid()
            #plt.show()
            today = str(todayDate.strftime("%Y-%m-%d"))
            try:
                os.mkdir('output/' + today)
            except:
                pass 
            fileName = 'output/' + today + '/' + self.ticker + '_' + today + '.png'
            plt.savefig(fileName, bbox_inches='tight')

        returnValues = []
        if self.getDate:
            returnValues.append(lastBuyDate)
        if self.getBuyHold:
            returnValues.append(round(buyAndHold, 2))
        if self.getReturn:
            returnValues.append(round(highestReturn, 2))
        if self.df:
            returnValues.append(data)

        return returnValues
        
    
    def findReturn(self, fast, slow):        
        # Create column names based on input values
        fastEMA = str(fast) + " EMA"
        slowEMA = str(slow) + " EMA"

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
        # TODO
        # if price is less than previous latest, value, don't
        # add it, if statement before adding to list
        r = data['return'].tolist()
        #print(r)
        r = [i for i in r if i != 0]
        lastBuy = 0.0
        initial = 1.0
        gross = 0.0
        holding = False
        # Exponential Moving Average Nought Sell 
        # 
        # Buy at first buy signal.
        # Hold until sell signal:
        #
        # if sell signal > last buy:
        # sell share for profit
        #
        # else if sell signal < last buy:
        # don't sell (capital mitigation)
        #
        # else if buy signal and not holding and have enough cash:
        # buy share
        for price in r:
            if price < 0 and initial == 1.0 and not holding:
                gross += price
                initial = price
                lastBuy = price*-1
                holding = True
            elif price > 0  and holding and price >= gross and price > lastBuy:
                gross += price
                holding = False
                lastBuy = 0.0
            elif price < 0  and not holding and gross >= price*-1:
                gross += price
                holding = True
                lastBuy = price*-1
        
        # If last trade signal a buy, add current price
        # Else if sell, current price not added
        if holding == True:
            gross += closes[-1] - initial
        else:
            gross -= initial

        percent = (gross + initial)/initial * -100

        data.drop(columns=[fastEMA, slowEMA], inplace=True)

        return percent


if __name__ == '__main__':
    startTime = time.time()
    stock = 'SPY'
    print('Calculating on ' + stock + ':')

    EMANS(stock, loops=252, delta=254, graph=True, log=True).findBestReturn()
    
    print('Run time: ' + str(round(time.time() - startTime, 2)) + 's')
    print()

