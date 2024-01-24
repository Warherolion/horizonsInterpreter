from flask import Flask, render_template, Response, request, redirect, url_for

import paho.mqtt.client as mqtt
import random
import time
from paho.mqtt import client as mqtt_client
from CommsClient import run, onPub, end
app = Flask(__name__)





@app.route('/')
def json():
    return render_template('index.html')






#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    run()
    return render_template('index.html')


'''
#background process happening without any refreshing
@app.route('/marsTrack')
def marsTrack():
    onPub()
    return render_template('index.html')

'''

@app.route('/planetChoice/', methods=['GET'])
def planetChoice():
    value = None

    valCheck= None
    if request.method == 'GET':
        valCheck=request.args.get('value');

    if valCheck == 'clest1':
        # Do your stuff
        value = 'Mercury'
    elif valCheck == 'clest2':
    # Do your stuff
        value = 'Moon'
    elif valCheck == 'clest3':
    # Do your stuff
        value = 'Mars'
    elif valCheck == 'clest4':
    # Do your stuff
        value = 'Jupiter'

    elif valCheck == 'clest5':
    # Do your stuff
        value = 'Saturn'

    elif valCheck == 'clest6':
    # Do your stuff
        value = 'Uranus'
    elif valCheck == 'clest7':
        value = "Neptune"

    else:
        value = "error"
        
    onPub(value)
    return render_template('index.html')


@app.route('/mqttDisCon')
def mqttDisCon():
    end()
    return render_template('/index.html')



