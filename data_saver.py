import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Configure serial port
serial_port = 'COM3'  # replace with your port
baud_rate = 115200    # adjust to match your device's baud rate
ser = serial.Serial(serial_port, baud_rate)

# Data storage
f = 60 #hz
T = 10 #s



data_buffer = {'ax': np.zeros(T*f), 'ay': np.zeros(T*f), 'az': np.zeros(T*f), 'gx': np.zeros(T*f), 'gy': np.zeros(T*f), 'gz': np.zeros(T*f), 'mx': np.zeros(T*f), 'my':np.zeros(T*f) , 'mz': np.zeros(T*f), 'tp': np.zeros(T*f)}

sample_idx = 0
while True: 
    try: 
        line = ser.readline().decode('utf-8').strip()
        values = list(map(float, line.split(',')))
        
        if len(values) == 10: 

            keys = list(data_buffer.keys())
            for i, key in enumerate(keys):
                data_buffer[key][sample_idx] = values[i]

            sample_idx +=1

    except (ValueError, serial.SerialException) as e:
        print(f"Error reading data: {e}")
        
    if sample_idx >= T*f: 
        break

np.savez("Flat_Square_Flat", **data_buffer)

# Close serial port when done
ser.close()