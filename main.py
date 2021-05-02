import time
import adafruit_dht
import board
import sys
import RPi.GPIO as GPIO
from UltasonicSensor.ultrasonic import Ultrasonic
from UltasonicSensor.mqtt_message import MyMQTT

def going_out():
    MyMQTT.send("movement","away")
    print("going out!!")

def going_in():
    MyMQTT.send("movement","close")
    print("going In!!")

def no_movement():
    MyMQTT.send("movement","no")
    print("no_movement!!")

if __name__ == "__main__":
    dht_device = adafruit_dht.DHT11(board.D4)
    ultrasonic = Ultrasonic(pin_trig=24, pin_echo=23)
    while True:
        try:
            #reading temperature and in case of error assign a default value
            try:
                temperature = dht_device.temperature
            except RuntimeError as err:
                print(err)
                temperature = 20

            #reading humidity and in case of error assign a default value
            try:
                 humidity =  dht_device.humidity
            except RuntimeError as err:
                print(err)
                humidity =35

            #print(f'Temp: {temperature} C  Humidity: {humidity} ')

            # sort of switch case
            option = {
                -1 : no_movement,
                -2 : no_movement,
                 0 : going_in,
                 1 : going_out,
            }
            option[ultrasonic.get_direction(temperature, humidity)]()

            time.sleep(0.5)
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()