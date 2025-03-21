import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Enter radius and center of mass velocity
radius = float(input("Enter the radius of the wheel: "))
velocity = float(input("Enter the center of mass velocity: "))

# Calculate the maximum theta based on the desired number of wheel rotations
num_rotations = 5
theta_max = num_rotations * 2 * np.pi  # Five full rotations

# Time array for animation based on velocity
t_max = theta_max / velocity
frame_count = 1000  # Total frames for animation
time = np.linspace(0, t_max, frame_count)

# Calculate theta and position of the cycloid path
theta = velocity * time

# Create a figure and axes
fig, ax = plt.subplots()
ax.set_xlim((0, num_rotations * 2 * np.pi * radius))
ax.set_ylim((0, 15 * radius))
ax.set_aspect('equal')

# Create the line for the cycloid path
line, = ax.plot([], [], 'b-', lw = 2, label = 'Cycloid Path')

# Add dot for the current position on the wheel
dot, = ax.plot([], [], 'ro', label = 'Point on Wheel')

# Add a circle to represent the wheel itself
wheel, = ax.plot([], [], 'g--', lw = 1, label = 'Wheel')


# Initialize function for the animation
def init():
    line.set_data([], [])
    dot.set_data([], [])
    wheel.set_data([], [])
    return line, dot, wheel


# Update function for the animation
def update(frame):
    # Cycloid path
    x = radius * (theta[:frame + 1] - np.sin(theta[:frame + 1]))
    y = radius * (1 - np.cos(theta[:frame + 1]))
    line.set_data(x, y)

    # Position of dot on the wheel
    x_dot = radius * theta[frame] - radius * np.sin(theta[frame])
    y_dot = radius - radius * np.cos(theta[frame])
    dot.set_data([x_dot], [y_dot])

    # Draw the wheel
    wheel_center_x = radius * theta[frame]
    wheel_center_y = radius
    theta_circle = np.linspace(0, 2 * np.pi, 100)
    wheel_x = wheel_center_x + radius * np.cos(theta_circle)
    wheel_y = wheel_center_y + radius * np.sin(theta_circle)
    wheel.set_data(wheel_x, wheel_y)

    return line, dot, wheel


# Create animation
ani = FuncAnimation(fig, update, frames = frame_count, init_func = init, blit = True, interval = 5)

plt.legend(loc = 'upper right')
plt.show()