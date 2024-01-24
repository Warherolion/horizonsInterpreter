
#mosquitto -v -c "C:\Program Files\mosquitto\mosquitto.conf"


import random
import time

from paho.mqtt import client as mqtt_client

from Horizions import horizonsMainRun

topic = "python/mqtt"
broker = '192.168.86.172'
port = 1883
statusTopic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
clientC = None

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, value):

    msg = horizonsMainRun(value)
    #print(msg)

    result = client.publish(topic, msg)




def onPub(value):
    publish(clientC, value)


def run():
    global clientC
    clientC = connect_mqtt()
    clientC.loop_start()


def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message



def end():
    clientC.disconnect()
    #client.loop_stop()


if __name__ == '__main__':
    run()