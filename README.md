# fin-math
This repository contains the program files for trading algorithms and reference files. The algorithm is based on the Exponential Moving Average crossover leveraged with logic to achieve maximum returns. Additionally, every possible crossover Fast/Slow periods are calculated to determine the maximum return window pairs.

## EMANS.py
Main algorithm file. The program will download the delta days from current date stock data in a pandas df. Moving Average Fast/Slow periods will be calculated iteratively. Based on the crossover, a buy or a sell signal will be sent. After running through all possible combinations, the best Fast/Slow pair will be returned and the buy and hold return will be calculated as well. Percent returns from both methods will be outputted alongside of a recommendation to buy or sell the stock based on if the last buy signal was less than $n/2$ days ago with $n = fast period$.

## EMANSRunner.py
File to run the EMANS algorithm through a list of provided stocks.

## tradingData.py
Price data downloader class. Uses the alpaca trading API.

## twitterBot.py
Twitter bot files to tweet program output for easy user notifications.

## config.py
File to hold API keys.