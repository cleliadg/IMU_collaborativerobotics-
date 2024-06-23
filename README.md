# IMU_collaborativerobotics
Welcome to the IMU_CollaborativeRobotics repository, where technology meets compassion to empower individuals with motor disabilities. Our mission? To enabling robots to mirror movements and assist in therapeutic exercises and daily tasks.

## function_pool

This script contains a collection of functions to interact with an IMU (Inertial Measurement Unit) and a servo motor controlled via an Arduino. The functions include conversion of rotation matrices to Euler angles, acquiring Euler angles from the IMU, and calibrating and converting encoder data for servo motors.

## osc_encoder

This Python script provides functionality to decode Open Sound Control (OSC) messages and bundles.

##  record_for_mirroring_movement

This script involves recording trajectory data using an IMU (Inertial Measurement Unit) with both a single-thread and a multi-threading approach.

## control_real_time

This script implements a Proportional-Integral-Derivative controller to control a servo motor based on the angle readings from an IMU (Inertial Measurement Unit) and an encoder. The script runs in a Python environment and communicates with an Arduino board to read encoder values and control the servo motor.

## min_jerk
This script utilizes pyFirmata to control a servo motor connected to an Arduino. It generates a smooth trajectory between two positions using the minimum jerk trajectory generation method.

## admittance control 
THis script is designed to enable force-adaptive servo control using an Arduino and Python.
