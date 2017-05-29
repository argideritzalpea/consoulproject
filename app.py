#!/usr/bin/env python
#omg

import urllib
import json
import os
import re

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
    
    if req.get("result").get("action") == "ask.question":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("country")
        characteristic = parameters.get("attribute")
        if str(db.codebook.distinct(characteristic)[0]["Construction"]) == "in":
            speech = "The " + str(db.codebook.distinct(characteristic)[0]["Entity"]) + " in " + zone + " is " + str(db.factbook.distinct(zone)[0][characteristic]) + " " + str(db.codebook.distinct(characteristic)[0]["Units"])
        else:
            speech = "The " + str(db.codebook.distinct(characteristic)[0]["Entity"]) + " of " + zone + " " + str(db.codebook.distinct(characteristic)[0]["Construction"]) + " " + str(db.factbook.distinct(zone)[0][characteristic]) + " " + str(db.codebook.distinct(characteristic)[0]["Units"])
    elif req.get("result").get("action") == "compare":
        result = req.get("result")
        parameters = result.get("parameters")
        
        characteristic = parameters.get("attribute")        
        
        country = parameters.get("country")
        countryfact = re.sub('[$]', '', db.factbook.distinct(country)[0][characteristic])

        country2 = parameters.get("country2")
        country2fact = re.sub('[$]', '', db.factbook.distinct(country2)[0][characteristic])
        
        speech = "The difference of " + country + "'s " + characteristic + " and that of " + country2 + " is " + str(float(countryfact) - float(country2fact)) + " " + str(db.codebook.distinct(characteristic)[0]["Units"])
    else:
        return {}
    
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
