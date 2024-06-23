from pyfirmata import Arduino, util
import time


board = Arduino('/dev/ttyUSB0')  # Replace with your actual serial port
force_sensor_pin = 'A1'
servo_pin = 9
# Start the iterator to continuously listen for events
it = util.Iterator(board)
it.start()


force_sensor = board.get_pin(force_sensor_pin)
servo = board.get_pin('d:{}:s'.format(servo_pin))

# Constants for control 
K_p = 0.8  
K_i = 0.0
K_d = 0.45 

def read_force():
    return force_sensor.read()

# Function to control the servo based on force feedback
def admittance_control(target_force):
    current_force = read_force()
    error = target_force - current_force
    
    # Calculate servo position adjustment 
    position_adjustment = K_p * error + K_i * 0 + K_d * 0  
    

    current_position = servo.read()
    new_position = current_position + position_adjustment
    servo.write(new_position)


try:
    while True:
        
        desired_force = 0.5  
        # Perform admittance control based on desired force
        admittance_control(desired_force)
        
        time.sleep(0.1) 
        
except KeyboardInterrupt:
    board.exit()
