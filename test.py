from yahoo_finance import Share
import re

#aapl = Share('AAPL')
message_text = input()
if re.search(r"(?i)high", message_text) != None:
    if re.search(r"(?i)year|52|52 wk|52 week", message_text) != None:
        stock_symb = re.sub(r"(?i)high|year|52|52 wk|52 week","", message_text)
        stock = Share(stock_symb.strip())
        stock_price = stock.get_year_high()
        print(stock_price)
        if (stock_price == None):
            message_to_send = "error"
        else:
            message_to_send = "The 52 wk high for {} is {}".format(message_text, stock_price)
#stock = Share(message_text.strip())
#print(stock.get_market_cap())
