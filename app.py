#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from pymongo import MongoClient
from os import environ

# Flask app should start in global layout
app = Flask(__name__)

client = MongoClient('mongodb://RadMajik:YUVBnmio5%@ds149481.mlab.com:49481/heroku_bbzbf3l3')
db = client.get_default_database()
find = db.factbook.find()

@app.route('/')
def connect():
    return jsonify(find)

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

    speech = "The cost of shipping to " + zone + " is " + db.factbook.distinct(zone)[0]["accountBalance.txt"] + " euros."

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
