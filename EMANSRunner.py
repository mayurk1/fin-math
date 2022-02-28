import EMANS as algo
import time

if __name__ == '__main__':
    startTime = time.time()
    """
    Takes in a list of stocks to run the EMANS algo on.
    
    Do not use stocks that have split within delta
    time period (API limitation).
    """
    faangs = [
        'SPY',
        'FB',
        'AAPL',
        'AMZN',
        'NFLX',
        'GOOG'
    ]

    print("Running...")
    for ticker in faangs:
        algo.EMANS(ticker, loops=252, delta=254, graph=True).findBestReturn()

    print('Total Run Time: ' + str(round(time.time() - startTime, 2)) + 's')
