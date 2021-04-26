import RPi.GPIO as GPIO

import time
import adafruit_dht
import board
# from https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
# sudo apt install libgpiod2
# pip3 install adafruit-circuitpython-dht

# Setting up pin for ultrasonic sensor
GPIO.setmode(GPIO.BCM)
TRIG = 24
ECHO = 23
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#setting up dh11 using gpio4
dht_device = adafruit_dht.DHT11(board.D4)

#making sure the trigger is down, therefore the ultrasonic sensor is nor mesuring
print("Distance Measurement In Progress")
GPIO.output(TRIG, False)

print("Waiting For Sensor To Settle")
time.sleep(2)
while True:
    # reading temperature and humidity
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
    except RuntimeError as err :
        temperature = 20 
        humidity = 35
        print(f"Error {err}")
    print(f'Temp: {temperature} C  Humidity: {humidity} ')
    #calculate the speed sound in this condition
    speed = 331.4 + (0.606 * temperature) + (0.0124 * humidity)
    # send a pulse to start the ranging program, a  10us pulse is needed
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    # when the program start echo from low to high
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()
    # is high until the end of the trasmission
    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    print(f"Pulse duration is: {pulse_duration}")
    distance = (pulse_duration / 2) * (speed / 10000) * 1000000
    #distance = (pulse_duration / 2) * (speed * 1000)
    distance = round(distance, 2)
    print(f"Distance is : {distance}")
    if distance > 450 or distance < 2:
        print ("Distance out of range")
    else:
        print(f"Distance:{distance} cm")

    time.sleep(2)

GPIO.cleanup()

