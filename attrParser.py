#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import base64
import json

from flask import Flask, flash, redirect, url_for, render_template, request, session, abort

app = Flask(__name__)

#Api.ai client access token
CLIENT_ACCESS_TOKEN = '6c41a342e6874b278fd6b8ea0d5391c1'

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai  

@app.route("/query", methods=['GET', 'POST'])
def query(jsonVal=None):
    keyword=None
    if request.method == 'POST':
        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
	apirequest = ai.text_request()
    	apirequest.lang = 'en'  # English
    	apirequest.session_id = base64.b64encode(os.urandom(16)) #unique session id
    	apirequest.query = request.form["query"]
    	response = apirequest.getresponse()
    	responsestr = response.read().decode('utf-8')
    	response_obj = json.loads(responsestr)
        keyword = response_obj["result"]["parameters"]

    return render_template('query.html', jsonVal=str(keyword))

@app.route("/")
def main():
    return redirect(url_for('query'))

if __name__ == '__main__':
    app.run()

