import os
import re
import sys
import json
from yahoo_finance import Share

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
	# when the endpoint is registered as a webhook, it must echo back
	# the 'hub.challenge' value it receives in the query arguments
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200

	return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

	# endpoint for processing incoming messaging events

	data = request.get_json()
	log(data)  # you may not want to log every incoming message in production, but it's good for testing

	if data["object"] == "page":

		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:

				if messaging_event.get("message"):  # someone sent us a message

					sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
					recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
					message_text = messaging_event["message"]["text"]  # the message's text

					exceptMessage = "Error! Type HELP to get a list of commands"
					error_notfound = "Could not find that stock symbol. Error 01 - please enter a valid stock symbol"
					try:
						if re.search(r"(?i)market|cap|capitilazation", message_text) != None:
							stock_symb = re.sub(r"(?i)market|cap|capitilazation","", message_text)
							try:
								name_price = getMarketCap(message_text)
								if not name_price[1] == None:
									message_to_send = messageMaker("Market Capitilzation", name_price)
								else:
									message_to_send = error_notfound;
							except:
								 message_to_send = exceptMessage
						elif re.search(r"(?i)open|start", message_text) != None:
							try:
								name_price = getMarketCap(message_text)
								if not name_price[1] == None:
									message_to_send = messageMaker("opening price", name_price)
								else:
									message_to_send = error_notfound;
							except:
								 message_to_send = exceptMessage
						elif re.search(r"(?i)high", message_text) != None:
							if re.search(r"(?i)year|52|52 wk|52 week", message_text) != None:
								try:
									name_price = getYearHigh(message_text)
									if not name_price[1] == None:
										message_to_send = messageMaker("Year High", name_price)
									else:
										message_to_send = error_notfound;
								except:
									message_to_send = exceptMessage
							else:
								try:
									name_price = getDayHigh(message_text)
									if not name_price[1] == None:
										message_to_send = messageMaker("Days High", name_price)
									else:
										message_to_send = error_notfound
								except:
									message_to_send = exceptMessage
						elif re.search(r"(?i)close", message_text) != None:
							try:
								name_price = getClose(message_text)
								if not name_price[1] == None:
									message_to_send = messageMaker("previous close", name_price)
								else:
									message_to_send = error_notfound
							except:
								message_to_send = exceptMessage
						elif message_text == "HELP":
							message_to_send = "Here is a list of commands"
						else: # if the input is just a stock symbol
							name_price = getCurrent(message_text)
							if not name_price[1] == None:
								message_to_send = messageMaker("current share price", name_price)
							else:
								message_to_send = error_notfound
					except:
						message_to_send = exceptMessage
					send_message(sender_id, message_to_send)

				if messaging_event.get("delivery"):  # delivery confirmation
					pass

				if messaging_event.get("optin"):  # optin confirmation
					pass

				if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
					pass

	return "ok", 200



def getShare(strTick):
	strTick = strTick.strip()
	stock = Share(strTick)
	stock.refresh()
	return stock

def messageMaker(cat, tup1):
	return "The {} for {} is {}".format(cat, tup1[0].upper().strip(), tup1[1])

def getCurrent(symb):
	symb.upper()
	stock = getShare(symb)
	return (symb, stock.get_price())

def getYearHigh(symb):
	symb = re.sub(r"(?i)high|year|52|52 week|52 wk","",symb).upper()
	stock = getShare(symb)
	return (symb, stock.get_year_high())

def getOpen(symb):
	symb = re.sub(r"(?i)open|start", "", symb)
	stock = getShare(symb)
	return (symb, stock.get_open())

def getClose(symb):
	symb = re.sub(r"(?i)previous|close|for", "", symb).upper()
	stock = getShare(symb)
	return (symb, stock.get_prev_close())

def getDayHigh(symb):
	symb = re.sub(r"(?i)high|days|day","",symb).upper()
	stock = getShare(symb)
	return (symb, stock.get_days_high())

def getMarketCap(symb):
	symb = re.sub(r"(?i)open|start","", symb)
	stock = getShare(symb)
	return (symb, stock.get_market_cap())


def send_message(recipient_id, message_text):
	log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
	params = {
		"access_token": os.environ["PAGE_ACCESS_TOKEN"]
	}
	headers = {
		"Content-Type": "application/json"
	}
	data = json.dumps({
		"recipient": {
			"id": recipient_id
		},
		"message": {
			"text": message_text
		}
	})
	r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
	if r.status_code != 200:
		log(r.status_code)
		log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
	print str(message)
	sys.stdout.flush()

if __name__ == '__main__':
	app.run(debug=True)
