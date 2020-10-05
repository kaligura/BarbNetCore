"""########################################################"""
"""############_______________________________#############"""
"""############||BARBNET SENSOR FIRMWARE 1.0||#############"""
"""############||29.09.2020                 ||#############"""
"""#############------------------------------#############"""
"""########################################################"""

global client_id
client_id = 'DEV'

"""IMPORTS"""

from time import sleep

import urequests as requests
from machine import Pin, I2C

import BME280


def config_fetch(key):
    response = requests.get('http://192.168.86.80/config.json')
    config_data = response.json()
    val = config_data[key]
    return val


def dummy_sensor():
    temp = '22.34'
    hum = '86'
    pres = '1252'
    print('Temperature: ', temp)
    print('Humidity: ', hum)
    print('Pressure: ', pres)
    print('STATIC VALUES')
    return


def sensor_routine():
    test_mode = config_fetch('test_mode')
    hum_enable = config_fetch('hum_enable')
    pres_enable = config_fetch('pres_enable')
    if test_mode == '1':
        print('!TESTING!')
        temp = '22'
        print(temp)
        if hum_enable == '1':
            hum = '2523'
            print(hum)
        if pres_enable == '1':
            pres = '351'
            print(pres)
        return
    else:
        i2c = I2C(scl=Pin(4), sda=Pin(5), freq=10000)
        bme = BME280.BME280(i2c=i2c)
        temp = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        temp_enable = config_fetch('temp_enable')
        hum_enable = config_fetch('hum_enable')
        pres_enable = config_fetch('pres_enable')

        if temp_enable == '0':
            temp = 'DISABLED'
        else:
            temp = bme.temperature

        if hum_enable == '0':
            hum = 'DISABLED'
        else:
            hum = bme.humidity

        if pres_enable == '0':
            pres = 'DISABLED'
        else:
            pres = bme.pressure
        mqtt_state = config_fetch('mqtt_enable')
        if mqtt_state == '1':
            mqtt_publish(temp, hum, pres)
        else:
            print('MQTT-PUBLISHING DISABLED!')
        return


def run_loop(enable):
    while enable == '1':
        print('RUNNING SENSOR ROUTINE')
        sensor_routine()
        print('SENSOR ROUTINE FINISHED')
        sleep_time = float(config_fetch('refresh_rate'))
        print('GOING TO SLEEP', sleep_time)
        sleep(sleep_time)
        return

    else:
        print('SENSOR DISABLED')
        print('PLEASE UPDATE CONFIG AND RESTART')
        raise SystemExit()


def mqtt_publish(temp, hum, pres):
    from umqtt.simple import MQTTClient

    SERVER = config_fetch('mqtt_host')
    client = MQTTClient("umqtt_client", SERVER)
    mqtt_topic = config_fetch('mqtt_topic')
    topic = mqtt_topic + '/' + client_id
    payload = "Temp=" + str(temp) + "Humidity=" + str(hum) + "Pressure=" + str(pres)
    client.connect()
    client.publish(topic, payload)
    client.disconnect()


while True:
    run_loop(enable=config_fetch('sensor_enabled'))
