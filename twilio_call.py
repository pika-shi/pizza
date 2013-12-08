# -*- coding: utf-8 -*-


import urllib
import urllib2
from twilio.rest import TwilioRestClient


class TwilioCall(object):
	account_sid = "ACb57f2ba02b0594ac7083a12f5705338f"
	auth_token = "9c2dd01f116a76fc868a864002894efd"
	from_phonenumber = "+815031318968"
	base_url = "http://o-tomox.com/~satoshi/pizza.php"

	def __init__(self):
		self.client = TwilioRestClient(TwilioCall.account_sid, TwilioCall.auth_token)

	def order_pizza(self, order):
		params = {}
		params["k"] = ",".join(map(str, order["kind_list"]))
		params["s"] = ",".join(map(str, order["size_list"]))
		params["n"] = ",".join(map(str, order["num_list"]))
		params["t"] = str(order["dlt"])
		params["name"] = urllib.quote(order["name"])
		params["phonenumber"] = order["tel"]

		url = "{0}?{1}".format(TwilioCall.base_url, "&".join(["{0}={1}".format(key, params[key]) for key in params]))

		print url

		response = urllib2.urlopen(url)

		print response.read()

		# call = self.client.calls.create(url=url, to="+819079383869", from_=TwilioCall.from_phonenumber)

		# print call



if __name__ == '__main__':
	order = {"kind_list": [3], "size_list": [35], "num_list": [1], "dlt": 60, "name": "ぴかし", "tel": "12345678"}
	twilio_call = TwilioCall()
	twilio_call.order_pizza(order)
