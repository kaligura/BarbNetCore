import json
import time

import paho.mqtt.client as mqtt

broker_url = "192.168.86.80"
broker_port = 1883


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code: {}".format(rc))


def on_disconnect(client, userdata, rc):
    print("Client Got Disconnected")


def on_message_from_BarbNet(client, userdata, message):
    print("Received Data: " + message.payload.decode())
    global payload

    payload = json.loads(message.payload.decode("utf-8"))
    print(payload)


def on_message_from_BarbNet_Sent(client, userdata, message):
    global sent
    sent = json.loads(message.payload.decode("utf-8"))
    if sent == 1:
        AZ = {}
        AZ['Arbeitszimmer'] = []
        AZ['Arbeitszimmer'].append({
            'Temp': int(temp),
            'Hum': int(hum),
            'Pres': int(pres)
        })
        with open('24h_log.json', 'w', encoding='utf8', errors='ignore') as json_file:
            json.dump(AZ, json_file)
        time.sleep(6)
        return


client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker_url, broker_port)

client.subscribe('BarbNet', qos=1)
client.message_callback_add('BarbNet', on_message_from_BarbNet)
client.message_callback_add('Sent', on_message_from_BarbNet_Sent)

client.loop_forever()