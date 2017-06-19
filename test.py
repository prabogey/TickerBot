from yahoo_finance import Share
import re

#aapl = Share('AAPL')
x = input()
message_text = re.sub(r"(?i)market|cap|capitilazation","", x)
stock = Share(message_text.strip())
print(stock.get_market_cap())

