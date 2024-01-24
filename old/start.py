from flask import Flask, render_template, Response, request, redirect, url_for

import paho.mqtt.client as mqtt
import random
import time
from mqttTest import run

app = Flask(__name__)




@app.route('/json')
def json():
    return render_template('json.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Connecting to Mqtt server")
    run()
    return ("nothing")