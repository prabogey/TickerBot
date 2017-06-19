from yahoo_finance import Share
import re

<<<<<<< HEAD
#aapl = Share('AAPL')
x = input()
message_text = re.sub(r"(?i)market|cap|capitilazation","", x)
stock = Share(message_text.strip())
print(stock.get_market_cap())
=======
aapl = Share('AAPL')
x = input()
if re.search(r"(?i)previous|close", x) != None:
    x = re.sub(r"(?i)previous|close", "", x)
    stock = Share(x.upper())
    print(stock.get_prev_close())
# if
#     print("yes")
>>>>>>> bd7c382b9d5a9e5b156e4bae4a90f6ed8d108728
