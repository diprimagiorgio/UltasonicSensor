#!/usr/bin/python
import adafruit_dht
import board
import paho.mqtt.client as mqtt #import the client1
from time import sleep
dht_device = adafruit_dht.DHT11(board.D4)
# sudo apt install libgpiod2
# pip3 install adafruit-circuitpython-dht
# https://circuitpython.readthedocs.io/projects/dht/en/latest/
while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        mqttc  = mqtt.Client()
        mqttc.connect("localhost", 1883)
        mqttc.publish("temp",f'Temp: {temperature} C  Humidity: {humidity} ')
    except RuntimeError as err :
        print(f"Error {err}")
    #humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    sleep(1)
