from yahoo_finance import Share
import re

def getShare(strTick):
    strTick = strTick.strip()
    stock = Share(strTick)
    stock.refresh()
    return stock

def messageMaker(cat, tup1):
    return "The {} for {} is {}".format(cat, tup1[0], tup1[1])

def getCurrent(symb):
    symb.upper()
    stock = getShare(symb)
    return (symb, stock.get_price())

x = input()
name_price = getCurrent(x)
print(name_price)
