import random
import time
from random import randrange

import paho.mqtt.client as mqtt

"""Random value generator for MQTT implementation"""


def mqtt_publish():
    broker_url = "192.168.86.80"
    broker_port = 1883
    client = mqtt.Client(client_id="AZ")
    client.connect(broker_url, broker_port)
    client.publish(topic='temp', payload=int(temp), qos=0)
    # client.publish(topic='test', payload='Delivered temp', qos=0)
    client.publish(topic='hum', payload=int(hum), qos=0)
    # client.publish(topic='test', payload='Delivered hum', qos=0)
    client.publish(topic='pres', payload=int(pres), qos=0)
    # client.publish(topic='test', payload='Delivered pres', qos=0)
    client.publish(topic='Sent', payload='1', qos=0)


def main():
    for _ in range(0, 10):
        randomizer()
        mqtt_publish()
        time.sleep(5)


def randomizer():
    global temp
    global hum
    global pres
    temp = randrange(40)
    hum = random.randint(0, 500)
    pres = random.randint(0, 500)
    return


main()
