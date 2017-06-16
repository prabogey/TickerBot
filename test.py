from yahoo_finance import Share
import re

aapl = Share('AAPL')
x = input()
if re.search(r"(?i)previous|close", x) != None:
    x = re.sub(r"(?i)previous|close", "", x)
    stock = Share(x.upper())
    print(stock.get_prev_close())
# if
#     print("yes")