import RPi.GPIO as GPIO

import time
import adafruit_dht
import board
# from https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
# sudo apt install libgpiod2
# pip3 install adafruit-circuitpython-dht

class Ultrasonic:
    __trigger_pin_second__ = 0.00001
    __min_distance__ = 2
    __max_distance__ = 450
    # making sure the trigger is down, therefore the ultrasonic sensor is nor mesuring Waiting For Sensor To Settle"
    def __init__(self, pin_trig, pin_echo):
        # Setting up pin for ultrasonic sensor
        GPIO.setmode(GPIO.BCM)
        self.TRIG = pin_trig
        self.ECHO = pin_echo
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        GPIO.output(self.TRIG, False)
        time.sleep(2)

    def get_distance(self, speed):
        # send a pulse to start the ranging program, a  10us pulse is needed
        GPIO.output(self.TRIG, True)
        time.sleep(self.__trigger_pin_second__)
        GPIO.output(self.TRIG, False)
        # when the program start echo from low to high
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()
        # is high until the end of the transmission
        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance =  (pulse_duration / 2) * (speed / 10000) * 1000000
        if distance > self.__max_distance__ or distance < self.__min_distance__:
            raise ValueError("Out of range")
        else:
            return distance

    @staticmethod
    def get_speed(temperature, humidity):
        return 331.4 + (0.606 * temperature) + (0.0124 * humidity)

if __name__ == "__main__":
    dht_device = adafruit_dht.DHT11(board.D4)
    ultrasonic = Ultrasonic(pin_trig=24, pin_echo=23)
    while True:
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

        # reading temperature and humidity
        print(f'Temp: {temperature} C  Humidity: {humidity} ')
        #calculate the speed sound in this condition
        try:
            distance = ultrasonic.get_distance(Ultrasonic.get_speed(temperature, humidity))
            distance = round(distance, 2)
            print(f"Distance is : {distance}")
        except ValueError as err:
            print(err)
        time.sleep(0.5)

    GPIO.cleanup()
