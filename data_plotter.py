import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Configure serial port
serial_port = 'COM3'  # replace with your port
baud_rate = 115200    # adjust to match your device's baud rate
ser = serial.Serial(serial_port, baud_rate)

# Initialize plot
fig, (ax, gx, mx, tp) = plt.subplots(4, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.5)

# Set up plots for each data type
for axis, title, y_limits in zip(
    [ax, gx, mx, tp], 
    ['Accelerometer', 'Gyroscope', 'Magnetometer', 'Temperature'], 
    [(-2000, 2000), (-1000, 1000), (-100, 100), (0, 100)]  # Customize limits for each subplot
):
    axis.set_title(title)
    axis.set_xlim(0, 100)
    axis.set_ylim(y_limits)  # Set specific y-axis limits
    axis.grid()

# Data storage
data_buffer = {'ax': [], 'ay': [], 'az': [], 'gx': [], 'gy': [], 'gz': [], 'mx': [], 'my': [], 'mz': [], 'tp': []}
plot_lines = {
    'ax': ax.plot([], [], label='ax')[0],
    'ay': ax.plot([], [], label='ay')[0],
    'az': ax.plot([], [], label='az')[0],
    'gx': gx.plot([], [], label='gx')[0],
    'gy': gx.plot([], [], label='gy')[0],
    'gz': gx.plot([], [], label='gz')[0],
    'mx': mx.plot([], [], label='mx')[0],
    'my': mx.plot([], [], label='my')[0],
    'mz': mx.plot([], [], label='mz')[0],
    'tp': tp.plot([], [], label='tp')[0],
}
for axis in [ax, gx, mx, tp]:
    axis.legend(loc='upper right')

# Update function for animation
def update(frame):
    try:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        values = list(map(float, line.split(',')))

        if len(values) == 10:
            keys = list(data_buffer.keys())
            for i, key in enumerate(keys):
                data_buffer[key].append(values[i])

            # Keep buffer size manageable
            for key in data_buffer:
                if len(data_buffer[key]) > 100:
                    data_buffer[key].pop(0)

            # Update plot lines
            for key, line in plot_lines.items():
                line.set_data(range(len(data_buffer[key])), data_buffer[key])

    except (ValueError, serial.SerialException) as e:
        print(f"Error reading data: {e}")

    return plot_lines.values()

# Animation
ani = animation.FuncAnimation(fig, update, blit=True, interval=50)

# Show plot
plt.show()

# Close serial port when done
ser.close()