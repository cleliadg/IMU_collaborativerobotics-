import serial
import time
import functions_pool
import threading
import numpy as np
import os



#-------------------------------------- TRAJECTORY RECORDING SINGLE THREAD (WORKING) ----------------------------------------------

# matrix = []
# current_time = 0
# sampling_time = float(input("Inserire la frequenza di campionamento:\n"))
# recording_duration = float(input("Inserire la durata della registrazione:\n"))  # in seconds

# print("Press Enter to start recording...")
# input()

# start_time = time.time()
# while time.time() - start_time < recording_duration:
#     angle = functions_pool.get_euler_angles()
#     if angle is not None:
#         angle_imu = functions_pool.get_angle(angle)
        
#         # Check the angle value and adjust it if necessary
#         if angle_imu < 8:
#             angle_imu = 8
#         elif angle_imu > 140:
#             angle_imu = 140
        
#         matrix.append([current_time, angle_imu])
#         time.sleep(sampling_time)
#         current_time += sampling_time

# print("Recording stopped.")
# print(matrix)

# file_path = 'singlethread_data.txt'

# # Save the matrix to a text file with space as the delimiter
# np.savetxt(file_path, matrix, fmt='%.2f', delimiter=' ')

# print(f"Matrix saved to {file_path}")

#-------------------------------------- TRAJECTORY RECORDING MULTI THREAD (WORKING) -----------------------------------------------------

# matrix = []
# current_time = 0
# recording = False
# sampling_time = float(input("Inserire la frequenza di campionamento:\n"))
# dir_path = os.path.dirname(os.path.realpath(__file__))
# file_path = os.path.join(dir_path, 'multithread_data.txt')

# def record_data():
#     global recording
#     global current_time
#     while True:
#         if recording:
#             angle = functions_pool.get_euler_angles()
#             if angle is not None:
#                 angle_imu = functions_pool.get_angle(angle)
#                 if angle_imu < 8:
#                     angle_imu = 8
#                 elif angle_imu > 140:
#                     angle_imu = 140
#                 matrix.append([current_time, angle_imu])
#                 time.sleep(sampling_time)
#                 current_time += sampling_time

# def save_to_file(matrix):
#     # Save the matrix to a text file with space as the delimiter
#     np.savetxt(file_path, matrix, fmt='%.2f', delimiter=' ')
#     print(f"Matrix saved to {file_path}")

# def listen_for_stop():
#     global recording
#     while True:
#         command = input("Prompt 'START' to start recording or 'STOP' to stop: ")
#         if command == 'STOP':
#             recording = False
#             print("Recording stopped.")
#             save_to_file(matrix)
#             print("Data saved.")
#         elif command == 'START':
#             recording = True
#             print("Recording started...")

# # Create threads
# t1 = threading.Thread(target=record_data)
# t2 = threading.Thread(target=listen_for_stop)

# # Start threads
# t1.start()
# t2.start()

#-------------------------------- TRIGGER + PID (TO CHECK) -----------------------------------------------------

