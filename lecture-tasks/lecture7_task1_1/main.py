import numpy as np
import matplotlib.pyplot as plt

# Enter initial data
v0 = float(input("Enter initial speed (m/s): "))
angle_deg = float(input("Enter the angle between the velocity vector and the horizon line (in degrees): "))
y0 = float(input("Enter the height from which the body was thrown (m): "))
k = float(input("Enter the medium resistence coefficient k (kg/s) "))

# Convert angle to radians
angle_rad = np.deg2rad(angle_deg)

# Initial speeds along the axles
vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)

# Modeling parameters
g = 9.81  # Acceleration of gravity, m/s^2
m = 1.0  # Body weight, kg (can be taken as 1 kg for simplicity)
dt = 0.01  # Time step, s

# Initial conditions
t = [0.0]  # Time
x = [0.0]  # Coordinate x
y = [y0]  # Coordinate y
vx = [vx0]  # Speed in x
vy = [vy0]  # Speed in y

# Motion modeling
while y[-1] >= 0:
    # Current time
    t_curr = t[-1] + dt

    # Current speeds
    vx_curr = vx[-1]
    vy_curr = vy[-1]

    # Speed module
    v = np.sqrt(vx_curr ** 2 + vy_curr ** 2)

    # Forces
    Fx = -k * vx_curr
    Fy = -m * g - k * vy_curr

    # Accelerations
    ax = Fx / m
    ay = Fy / m

    # Speed update (Euler method)
    vx_new = vx_curr + ax * dt
    vy_new = vy_curr + ay * dt

    # Coordinate update
    x_new = x[-1] + vx_curr * dt
    y_new = y[-1] + vy_curr * dt

    # Add new values to lists
    t.append(t_curr)
    vx.append(vx_new)
    vy.append(vy_new)
    x.append(x_new)
    y.append(y_new)

# Convert lists to arrays
t = np.array(t)
x = np.array(x)
y = np.array(y)
vx = np.array(vx)
vy = np.array(vy)
v = np.sqrt(vx ** 2 + vy ** 2)

# Plot graphs
plt.figure(figsize=(12, 8))

# Motion trajectory graph
plt.subplot(2, 2, 1)
plt.plot(x, y)
plt.title("Trajectory of body motion")
plt.xlabel("x (m)")
plt.ylabel("y (m)")

# Speed vs Time graph
plt.subplot(2, 2, 2)
plt.plot(t, v)
plt.title("Dependency of speed on time")
plt.xlabel("t (s)")
plt.ylabel("v (m/s)")

# X vs Time graph
plt.subplot(2, 2, 3)
plt.plot(t, x)
plt.title("X vs Time")
plt.xlabel("t (s)")
plt.ylabel("x (m)")

# Y vs Time graph
plt.subplot(2, 2, 4)
plt.plot(t, y)
plt.title("X vs Time")
plt.xlabel("t (s)")
plt.ylabel("y (m)")

plt.tight_layout()
plt.show()