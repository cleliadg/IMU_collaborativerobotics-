from pyfirmata import Arduino, util
import time
import math


servo_pin = 9
board = Arduino('/dev/ttyUSB0')  

# Start the iterator for the board
it = util.Iterator(board)
it.start()

servo = board.get_pin('d:{}:s'.format(servo_pin))

def mjtg(current, setpoint, frequency, move_time):
    timefreq = int(move_time * frequency)
    
    for time in range(1, timefreq):
        ##Calculate the position at the current time step using a cubic polynomial with normilized time
        pos = current + (setpoint - current) * (10 * pow(time/timefreq, 3) - 15 * pow(time/timefreq, 4) + 6 * pow(time/timefreq, 5))
        servo.write(pos)
        time.sleep(15 / 1000.0) 

try:
    myServo = 30
    setpoint = 90
    frequency = 500
    move_time = 2
    
    mjtg(myServo, setpoint, frequency, move_time)

except KeyboardInterrupt:
    board.exit()
