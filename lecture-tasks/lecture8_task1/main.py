import numpy as np
import matplotlib.pyplot as plt

# Input data
m = float(input("Enter the weight of the load (kg): "))
k = float(input("Enter spring stiffness coefficient (N/m): "))
b = float(input("Enter the resistance coefficient of the medium (N*s/m): "))

# Initial conditions
x0 = 1.0  # initial offset (m)
v0 = 0.0  # initial speed (m/s)

# Time parameters
t_max = 20  # maximum time (s)
dt = 0.01  # time step (s)
t = np.arange(0, t_max, dt)  # time grid


# Function for calculating positions and velocities
def oscillate(m, k, b, x0, v0, t):
    # The principle of solving a differential equation
    omega0 = np.sqrt(k / m)
    gamma = b / (2 * m)
    omega_d = np.sqrt(omega0 ** 2 - gamma ** 2)

    A = x0
    B = (v0 + gamma * x0) / omega_d

    # Damped harmonic oscillations
    x = np.exp(-gamma * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))
    v = np.gradient(x, dt)

    return x, v


# Calculating positions and velocities
x, v = oscillate(m, k, b, x0, v0, t)

# Energies
kinetic_energy = 0.5 * m * v ** 2
potential_energy = 0.5 * k * x ** 2
total_energy = kinetic_energy + potential_energy

# Plot graphs
plt.figure(figsize=(12, 8))

plt.plot(t, kinetic_energy, label='Kinetic energy', color='b', linestyle='-')
plt.plot(t, potential_energy, label='Potential energy', color='g', linestyle='-')
plt.plot(t, total_energy, label='Total mechanical energy', color='r', linestyle='-')

plt.title('Energy transformations during oscillation of a load on a spring')
plt.xlabel('Time (s)')
plt.ylabel('Energy (J)')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()