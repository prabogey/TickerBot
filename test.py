from yahoo_finance import Share
aapl = Share('APPLE')
stock = aapl.get_price()
print(stock == None)