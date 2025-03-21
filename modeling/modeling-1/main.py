import numpy as np
import matplotlib.pyplot as plt

# Data
g = 9.81  # m/s^2
R = 3.0  # m
mu = 0.01
alpha = (7 * np.pi) / 6  # rad

# Calculate initial velocity
v0_squared = R * (2 * g - g * np.cos(alpha) + 2 * mu * g * alpha)
v0 = np.sqrt(v0_squared)

# Check the value under the root for v(α)
v_alpha_squared = v0_squared - 2 * g * R * (1 - np.cos(alpha)) - 2 * mu * g * R * alpha

# Since v_alpha_squared can be negative due to energy losses, we use the modulus
v_alpha = np.sqrt(abs(v_alpha_squared))

# Angles for arc constructing
theta = np.linspace(0, alpha, 100)
x_arc = R * np.sin(theta)
y_arc = R * (1 - np.cos(theta))

# lift-off point
x0 = R * np.sin(alpha)
y0 = R * (1 - np.cos(alpha))

# Tangent angle at lift-off point
phi = alpha + np.pi / 2
vx = -v_alpha * np.cos(phi)
vy = v_alpha * np.sin(phi)

# Flight time after lift-off
t = np.linspace(0, 0.72, 100)  # time can be adjusted

# Trajectory after lift-off
x_flight = x0 + vx * t
y_flight = y0 + vy * t - 0.5 * g * t**2

# Plot a graph
plt.figure(figsize=(10, 6))
plt.plot(x_arc, y_arc, label='Movement in the arc')
plt.plot(x_flight, y_flight, label='Movement after leaving the arc')
plt.title("Trajectory of the body's motion along the arc and after leaving the arc")
plt.xlabel('x, m')
plt.ylabel('y, m')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()