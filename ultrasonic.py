import time

from RPi import GPIO as GPIO

#from UltasonicSensor.ulta import ultrasonic


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

    #return
    #           < 0 non movement
    #           = 0 move away
    #           > 0 move close
    def get_direction(self, temperature, humidity) -> int:
        count_out_of_range = 0
        count_no_movement = 0
        count_move_away = 0
        count_move_close = 0

        history = []

        prev_distance = 0
        curr_distance = 0

        while count_out_of_range < 20 and count_no_movement < 20:
            try:
                prev_distance = curr_distance
                curr_distance = self.get_distance(Ultrasonic.get_speed(temperature, humidity))
                if 1 > curr_distance - prev_distance > -1:
                    count_no_movement += 1
                elif curr_distance < prev_distance :
                    count_move_close += 1
                else:
                    count_move_away += 1

                history.append(curr_distance)
            except ValueError :
                count_out_of_range += 1
            time.sleep(0.05)

        print(f"history : {history}\n away = {count_move_away} close = {count_move_close} no mov = {count_no_movement} out = {count_out_of_range}")
        opt = [count_out_of_range, count_no_movement, count_move_away, count_move_close]
        return opt.index(max(opt)) - 2