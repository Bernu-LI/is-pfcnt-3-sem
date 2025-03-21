import numpy as np
import matplotlib.pyplot as plt


def ballisticMotion(h, v0, angle):
    g = 9.81    # Acceleration of gravity, m/s^2
    angleInRadians = np.radians(angle)      # Angle in radians

    # Calculate the initial velocity
    v0_x = v0 * np.cos(angleInRadians)
    v0_y = v0 * np.sin(angleInRadians)

    # Total flight time
    totalFlightTime = (v0_y + np.sqrt(v0_y**2 + 2 * g * h)) / g

    t = np.linspace(0, totalFlightTime, num=500)

    # Coordinates
    x = v0_x * t
    y = h + v0_y * t - 0.5 * g * t**2

    # Velocities
    v_x = (v0_x**2 + (v0_y - g * t) * (v0_y - g * t))**0.5
    v_y = v0_y - g * t

    # Trajectory building
    plt.figure(figsize=(12, 8))

    # Trajectory graph
    plt.subplot(3, 1, 1)
    plt.plot(x, y)
    plt.title('Movement trajectory')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.grid()

    # Speed versus time graph
    plt.subplot(3, 1, 2)
    plt.plot(t, v_x, label='v_x (m/s)')
    plt.plot(t, v_y, label='v_y (m/s)')
    plt.title('Body velocity')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.legend()
    plt.grid()

    # Coordinates versus time graph
    plt.subplot(3, 1, 3)
    plt.plot(t, x, label='x (m)')
    plt.plot(t, y, label='y (m)')
    plt.title('Body coordinates')
    plt.xlabel('Time (s)')
    plt.ylabel('Coordinates (m)')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()


def main():
    h = float(input("Enter height (m): "))
    v0 = float(input("Enter initial velocity (m/s): "))
    angle = float(input("Enter angle (in degrees): "))
    ballisticMotion(h, v0, angle)


if __name__ == "__main__":
    main()