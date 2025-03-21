import numpy as np
import matplotlib.pyplot as plt

# Problem constants
r = 0.06       # inner radius in meters
R = 0.13       # outer radius in meters
Vx = 3.5e6     # initial velocity along the x-axis, m/s
L = 0.21       # length of the capacitor along the x-axis, m

e = 1.6e-19    # electron charge, C
m = 9.11e-31   # electron mass, kg


# -----------------------------------------------------------------------------
# 1) Function to calculate the minimum potential difference (as provided)
# -----------------------------------------------------------------------------
def min_potential_difference(r, R, L, Vx, e, m):
    """
    Returns the minimum potential difference dphi_min such that
    the electron does not exit the capacitor, neglecting edge effects.
    """
    t = L / Vx  # travel time along x
    # Minimum electric field (rough estimate from the original approach)
    E_min = (m * r) / (e * t ** 2)
    # Potential difference across a cylindrical capacitor:
    dphi_min = E_min * np.log(R / r)
    return dphi_min


# -----------------------------------------------------------------------------
# 2) Function to integrate motion and produce trajectory + velocities + accel
# -----------------------------------------------------------------------------
def motion_plots(r, R, L, Vx, e, m):
    """
    Perform numerical integration of the electron trajectory in the y-direction,
    plotting y(x), vy(t), ay(t), and y(t).

    Returns
    -------
    t_total : float
        The total flight time = L / Vx
    v_final : float
        Magnitude of the final velocity vector at t = t_total
    """
    # First, find the "minimum" potential difference
    phi_min = min_potential_difference(r, R, L, Vx, e, m)

    # Flight time along the x-axis (assuming the electron stays between plates)
    t_total = L / Vx

    # Create a time grid for integration
    N = 2000  # number of steps
    dt = t_total / N
    t_vals = np.linspace(0, t_total, N + 1)

    # Arrays for y(t) position, y velocity, and y acceleration
    y_vals = np.zeros(N + 1)
    vy_vals = np.zeros(N + 1)
    ay_vals = np.zeros(N + 1)

    # Initial conditions
    y_vals[0] = 0.0     # starts in the middle
    vy_vals[0] = 0.0    # no initial y-velocity

    # Electric field in the radial direction for a cylindrical capacitor
    # E(rho) = [phi_min / ln(R/r)] * (1 / rho)
    def E_rho(rho):
        return (phi_min / np.log(R / r)) * (1.0 / rho)

    # Numerical integration (Euler method for simplicity)
    for i in range(N):
        # Current radius from the cylinder axis
        rho_i = (r + R) / 2 + y_vals[i]

        # a_y = (e/m)*E(rho_i)
        ay_vals[i] = (e / m) * E_rho(rho_i)

        # Update velocity and position
        vy_vals[i + 1] = vy_vals[i] + ay_vals[i] * dt
        y_vals[i + 1] = y_vals[i] + vy_vals[i + 1] * dt

    # Compute acceleration for the final point
    rho_end = (r + R) / 2 + y_vals[-1]
    ay_vals[-1] = (e / m) * E_rho(rho_end)

    # x(t) evolves uniformly (ignoring any deflection in x):
    x_vals = Vx * t_vals

    # --- Plotting ---
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # (1) Trajectory y(x)
    axs[0, 0].plot(x_vals, y_vals, label="y(x)")
    axs[0, 0].set_xlabel("x (m)")
    axs[0, 0].set_ylabel("y (m)")
    axs[0, 0].set_title("Electron Trajectory")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # (2) Velocity Vy(t)
    axs[0, 1].plot(t_vals, vy_vals, label="Vy(t)", color="tab:orange")
    axs[0, 1].set_xlabel("t (s)")
    axs[0, 1].set_ylabel("Vy (m/s)")
    axs[0, 1].set_title("Velocity Along y-axis")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # (3) Acceleration ay(t)
    axs[1, 0].plot(t_vals, ay_vals, label="ay(t)", color="tab:green")
    axs[1, 0].set_xlabel("t (s)")
    axs[1, 0].set_ylabel("ay (m/s²)")
    axs[1, 0].set_title("Acceleration Along y-axis")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # (4) Position y(t)
    axs[1, 1].plot(t_vals, y_vals, label="y(t)", color="tab:red")
    axs[1, 1].set_xlabel("t (s)")
    axs[1, 1].set_ylabel("y (m)")
    axs[1, 1].set_title("Displacement Along y-axis")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()

    # --- Final velocity magnitude ---
    # The x-component is constant (Vx).  The y-component after the last step is vy_vals[-1].
    v_final = np.sqrt(Vx**2 + vy_vals[-1]**2)

    # Return the flight time and final velocity magnitude
    return t_total, v_final


# -----------------------------------------------------------------------------
# 3) Main block: output results and plot
# -----------------------------------------------------------------------------
phi_min = min_potential_difference(r, R, L, Vx, e, m)
print(f"Minimum potential difference: {phi_min:.2f} V")

# Get flight time and final velocity from the motion_plots function
t_flight, V_final = motion_plots(r, R, L, Vx, e, m)

# Print out flight time and final velocity magnitude
print(f"Flight time t = {t_flight:.6e} s")
print(f"Final velocity magnitude Vcon = {V_final:.6e} m/s")
