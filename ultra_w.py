import RPi.GPIO as GPIO

import time
# from https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
GPIO.setmode(GPIO.BCM)

TRIG = 24

ECHO = 23
print("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)

print("Waiting For Sensor To Settle")

time.sleep(2)
while True:
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
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    if distance > 450 or distance < 2:
        print ("Distance out of range")
    else:
        print(f"Distance:{distance} cm")

    time.sleep(2)

GPIO.cleanup()

