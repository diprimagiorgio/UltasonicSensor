import time
import adafruit_dht
import board
# from https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
# sudo apt install libgpiod2
# pip3 install adafruit-circuitpython-dht
from UltasonicSensor.ultrasonic import Ultrasonic


def going_out():
    print("going out!!")



def going_in():
    print("going In!!")


def no_movement():
    print("no_movement!!")

    pass

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

        option = {
            -1 : no_movement,
            -2 : no_movement,
             0 : going_in,
             1 : going_out,
        }
        option[ultrasonic.get_direction(temperature, humidity)]()

        time.sleep(0.5)

    GPIO.cleanup()
