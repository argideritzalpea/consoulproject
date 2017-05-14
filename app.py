#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from pymongo import MongoClient

# Flask app should start in global layout
app = Flask(__name__)
client = MongoClient('mongodb://RadMajik:YUVBnmio5%@cluster0-shard-00-00-b4hqz.mongodb.net:27017,cluster0-shard-00-01-b4hqz.mongodb.net:27017,cluster0-shard-00-02-b4hqz.mongodb.net:27017/chatbot?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')

col = client.chatbot.factbook
print(col)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    
    if req.get("result").get("action") != "ask.question":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("country")

    speech = "The cost of shipping to " + zone + " is " + col.distinct(zone)[0]['airports.txt'] + " euros."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
