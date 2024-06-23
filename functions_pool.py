import serial
from pythonosc import udp_client
import numpy as np
import osc_decoder
import socket

#---------------------------------------- WORKING (to get roll, pitch, yaw mathematically)----------------------------------------------------------------

def rotation_matrix_to_euler_angles(rotation_matrix):
    """
    Converts a 3x3 rotation matrix to roll, pitch, and yaw angles.
    Assumes the rotation order is ZYX.
    """
    sy = np.sqrt(rotation_matrix[0, 0] * 2 + rotation_matrix[1, 0] * 2)

    singular = sy < 1e-6

    if not singular:
        roll = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        pitch = np.arctan2(-rotation_matrix[2, 0], sy)
        yaw = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    else:
        roll = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
        pitch = np.arctan2(-rotation_matrix[2, 0], sy)
        yaw = 0.0

    return np.degrees(roll), np.degrees(pitch), np.degrees(yaw)

#--------------------------------------- WORKING (to get roll, pitch and yaw from NGIMU)----------------------------------------------------------------

def get_euler_angles():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_socket.sendto(bytes("/identify\0\0\0,\0\0\0", "utf-8"), ("192.168.121.153", 9000))

    IMU_client = udp_client.SimpleUDPClient("192.168.121.153", 9000)
    IMU_client.send_message("/rate/matrix", 50)

    receive_ports = [8153]
    receive_sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(len(receive_ports))]

    index = 0
    for receive_socket in receive_sockets:
        receive_socket.bind(("", receive_ports[index]))
        index = index + 1
        receive_socket.setblocking(False)


        for udp_socket in receive_sockets: 
            read=False
            while(read == False):
                try:
                    data, addr = udp_socket.recvfrom(2048)
                except socket.error:
                    pass
                else:
                    read = True
                    for message in osc_decoder.decode(data):
                        time_stamp = message[0]
                        data_type = message[1]              
                        if data_type == '/matrix':
                            Rxx = message[2]
                            Ryx = message[3]
                            Rzx = message[4]
                            Rxy = message[5]
                            Ryy = message[6]
                            Rzy = message[7]
                            Rxz = message[8]
                            Ryz = message[9]
                            Rzz = message[10] 
                           
                            if udp_socket.getsockname()[1] == receive_ports[0]:
                                FA_L_g=np.matrix([[Rxx,Ryx,Rzx],[Rxy ,Ryy, Rzy],[Rxz ,Ryz ,Rzz]])
                                roll,pitch,yaw = rotation_matrix_to_euler_angles(FA_L_g)
                                # print("Done! IMU angle value =", roll)
                                return roll

#------------------------------------ LINEAR MAPPING FOR USE THE RELATIVE ENCODER INFO ---------------------------------------------

# def linear_mapping(angle,a,b,c):
#     if 0 <= angle <= b:
#         mapped_value = (b - a) / 90 * angle + a
#     elif b < angle <= 180:
#         mapped_value = (c - b) / 30 * (angle - 90) + b
#     else:
#         mapped_value = None

#     return mapped_value

#------------------------------------- WORKING - (to get IMU angle with offset) ----------------------------------------

def get_angle(angle):
    
    angle_IMU = angle + 90
    
    # a = None
    # b = None
    # c = None

    # print("Put the IMU at 0 degrees")
    # input("Press Enter to acquire...")
    # while a == None: 
    #     a = get_euler_angles()
    #     a = a + 90
    #     time.sleep(3) 
        
        
    # print("Put the IMU at 90 degrees")
    # input("Press Enter to acquire...")
    # while b == None: 
    #     b = get_euler_angles()
    #     b = b + 90
    #     time.sleep(3)
        
    # print("Put the IMU at 180 degrees")
    # input("Press Enter to acquire...")
    # while c == None: 
    #     c = get_euler_angles()
    #     c = c + 90
    #     time.sleep(3)
        
    return angle_IMU


#----------------------------------------- READ SERVO MOTOR DATA TO CALIBRATE------------------------------------------------------

def calibration_servo():
    # Configura la porta seriale
    ser = serial.Serial('COM3', 115200)  # Sostituisci 'COM3' con la tua porta seriale

    # Configurazione delle variabili
    servo_analog_in_pin = 3
    pos_servo1 = 8
    pos_servo2 = 90
    rep = 3
    counter = 0

    # calcoliamo i digit a 0 e a 90
    ser.write(f"set_position {pos_servo1}\n".encode())
    a_s = ser.read(8)
    ser.write(f"set_position {pos_servo1}\n".encode())
    b_s = ser.read(8)
  
    return a_s, b_s

#----------------------------------- CONVERT ENCODER DATA -------------------------------------------------

def conversion_encoder(a,b,pos_servo):
     
    pos = ((82)/(b-a))*(pos_servo-a)+8
    
    return pos

#------------------------------- SEND COMMAND TO ARDUINO-------------------------------------------------

# def send_command(command):
#     ser.write(command.encode())
#     time.sleep(2)  # Dà il tempo all'Arduino di elaborare il comando