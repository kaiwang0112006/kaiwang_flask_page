# coding: UTF-8

import os,sys
import json
from flask import Flask, render_template, url_for, request, jsonify
from flask import *
import argparse
import logging, logging.config, yaml
import time

##########################################
## Options and defaults
##########################################
def getOptions():
    parser = argparse.ArgumentParser(description='python *.py [option]')
    parser.add_argument('--ip', dest='ip', help="ip", default='0.0.0.0')
    parser.add_argument('--port', dest='port', help="port", default=8080)
    parser.add_argument('--debug', dest='debug', help="if debug", default='True')
    args = parser.parse_args()

    return args


"""
Flask
"""
app = Flask(__name__,static_folder='static',template_folder='static/html')
"""
log
"""
logging.config.dictConfig(yaml.load(open(os.path.join(sys.path[0], 'logging.conf')),Loader=yaml.FullLoader))
logger = logging.getLogger()

@app.route('/' , methods=['GET'])
def homepage():
    return render_template(r"homepage.html")

@app.route('/certificates' , methods=['GET'])
def certificates():
    return render_template(r"certificates.html")

@app.route('/aboutme' , methods=['GET'])
def aboutme():
    return render_template(r"aboutme.html")


if __name__ == "__main__":
    options = getOptions()
    print(options)
    check = {"False":False,"True":True}
    app.run(host=options.ip, port=options.port,debug=check[options.debug])
