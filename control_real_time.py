import time
import functions_pool
from pyfirmata import Arduino, SERVO, util
import keyboard
import serial

# Initialize Arduino and Servo
port = 'COM3'
pin = 3  # Servo pin
board = Arduino(port)
board.digital[pin].mode = SERVO

# Initialize serial communication for encoder
ser = serial.Serial('COM3', 9600)  # Adjust COM port as necessary

# PID parameters
max_angle = 125
min_angle = 10
kp = 0.5
ki = 0.2
kd = 1.0

# PID control variables
last_error = 0
integral = 0

def pid_control(setpoint, measured_value):
    global last_error, integral
    
    # Calculate error
    error = setpoint - measured_value
    
    # Proportional term
    P_out = kp * error
    
    # Integral term
    integral += error * 0.1  # 0.1 is the time step (dt)
    I_out = ki * integral
    
    # Derivative term
    derivative = (error - last_error) / 0.1
    D_out = kd * derivative
    

    output = P_out + I_out + D_out

    last_error = error
    
    return output

while True:
    angle = functions_pool.get_euler_angles()
        
    if angle is not None:
        angle_imu = functions_pool.get_angle(angle)
        #saturated the angle
        if angle_imu < 8:
            angle_imu = 8
        elif angle_imu > 140:
            angle_imu = 140

    setpoint = angle_imu
    if angle is not None: 
        try:
            # Read encoder value from serial
            if ser.in_waiting > 0:
                encoder_value = ser.readline().decode('utf-8').strip()
                encoder_value = int(encoder_value)
                

                pid_output = pid_control(setpoint, encoder_value)
                
                # Constrain output to servo limits
                servo_angle = max(min_angle, min(max_angle, pid_output))
                
                # Write to servo
                board.digital[pin].write(servo_angle)
                time.sleep(0.1)
            
            # Interrupt and detach the motor
            if keyboard.is_pressed('q'):
                board.digital[pin].detach()
                break
                
        except KeyboardInterrupt:
            board.digital[pin].detach()
            break
