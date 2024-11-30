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

sample_idx = 0

# instructions = [
#     "Flat",
#     "45rollCW",
#     "90rollCW",
#     "45rollCCW",
#     "90rollCCW",
#     "45pitchCW",
#     "90pitchCW",
#     "45pitchCCW",
#     "90pitchCCW",
#     "Flat", 
#     "Shake",
# ]
instructions = [
    "StayStill",
]
# instructions = [
#     "StayStill",
#     "SquareSide1",
#     "SquareSide2",
#     "SquareSide3",
#     "SquareSide1",
#     "SquareSide2",
#     "SquareSide3",
#     "StayStill",
# ]
# times = [4, 3, 3, 3, 3, 3, 3, 3, 3, 4] #s
# times = [4, 3, 3, 3, 3, 3, 3, 4] #s
times = [10] #s
T = sum(times)
data_buffer = {'ax': np.zeros(T*f), 'ay': np.zeros(T*f), 'az': np.zeros(T*f), 'gx': np.zeros(T*f), 'gy': np.zeros(T*f), 'gz': np.zeros(T*f), 'mx': np.zeros(T*f), 'my':np.zeros(T*f) , 'mz': np.zeros(T*f), 'tp': np.zeros(T*f)}

mode_idx = 0
mode_sample_count = 0

for t, time in enumerate(times): 
    print(f"Position/Movement: {instructions[t]}")
    for s in range(time*f): 
        try: 
            line = ser.readline().decode('utf-8').strip()
            values = list(map(float, line.split(',')))
            
            if len(values) == 10:
                keys = list(data_buffer.keys())
                for i, key in enumerate(keys):
                    data_buffer[key][sample_idx] = values[i]

        except (ValueError, serial.SerialException) as e:
            print(f"Error reading data: {e} at sample {sample_idx}")
        sample_idx +=1


np.savez("10_Seconds_Staying_Still", **data_buffer)

# Close serial port when done
ser.close()