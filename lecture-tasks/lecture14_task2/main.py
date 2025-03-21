import numpy as np
import matplotlib.pyplot as plt


def solve_refraction_angles(eps1, eps2, E1, theta1_deg):
    """
    Solve the boundary conditions for refraction of the E-field
    between two dielectrics with permittivities eps1, eps2.
    Incident field E1 at angle theta1 (deg) from +y (normal down).
    Returns: (E2, theta2_deg)
    """
    theta1 = np.radians(theta1_deg)

    # Equations:
    # (1) E1 * sin(theta1) = E2 * sin(theta2)
    # (2) eps1 * E1 * cos(theta1) = eps2 * E2 * cos(theta2)
    #
    # From (1) => E2 = E1 * sin(theta1)/sin(theta2).
    # Insert into (2):
    #   eps1 * E1 * cos(theta1) = eps2 * [E1*sin(theta1)/sin(theta2)] * cos(theta2)
    # => eps1*cos(theta1) = eps2*sin(theta1)*[cos(theta2)/sin(theta2)]
    # => eps1*cos(theta1) = eps2*sin(theta1)*cot(theta2)
    # => cot(theta2) = (eps1*cos(theta1)) / (eps2*sin(theta1))
    # => theta2 = arctan( (eps2*sin(theta1)) / (eps1*cos(theta1)) )

    # Watch for edge cases (theta1=0, etc.), but let's keep it general:
    theta2 = np.arctan((eps2 * np.sin(theta1)) / (eps1 * np.cos(theta1)))
    theta2_deg = np.degrees(theta2)

    # E2 from eqn (1):
    sin_t1 = np.sin(theta1)
    sin_t2 = np.sin(theta2)
    if abs(sin_t2) < 1e-14:
        E2 = 0.0
    else:
        E2 = E1 * (sin_t1 / sin_t2)

    return E2, theta2_deg


def main():
    print("=== Dielectric Interface: Streamplot Visualization ===")
    eps1 = float(input("Enter permittivity eps1 (medium 1): "))
    eps2 = float(input("Enter permittivity eps2 (medium 2): "))

    # We'll plot E-field lines
    E1 = float(input("Enter the E1 magnitude in medium 1: "))
    theta1_deg = float(
        input("Enter incidence angle THETA1 (deg) w.r.t. +y-axis (normal down): ")
    )

    # Solve for E2, theta2
    E2, theta2_deg = solve_refraction_angles(eps1, eps2, E1, theta1_deg)

    print(f"\nResults:")
    print(f"  In medium 1: E1 = {E1:.3f}, theta1 = {theta1_deg:.1f} deg")
    print(f"  In medium 2: E2 = {E2:.3f}, theta2 = {theta2_deg:.1f} deg")

    # Convert angles to radians
    t1 = np.radians(theta1_deg)
    t2 = np.radians(theta2_deg)

    # Define the piecewise E-field function over x,y space
    def E_field(x, y):
        """
        Return the (Ex, Ey) vector at position (x,y).
        We assume a piecewise constant field:
          - Medium 1 (y>0): E1 in direction (sin(t1), -cos(t1))
          - Medium 2 (y<0): E2 in direction (sin(t2), -cos(t2))
        """
        if y > 0:
            # medium 1
            Ex = E1 * np.sin(t1)
            Ey = -E1 * np.cos(t1)
        else:
            # medium 2
            Ex = E2 * np.sin(t2)
            Ey = -E2 * np.cos(t2)
        return Ex, Ey

    # Create a grid for streamplot
    x_min, x_max = -2.0, 2.0
    y_min, y_max = -2.0, 2.0

    nx, ny = 200, 200  # resolution
    x_vals = np.linspace(x_min, x_max, nx)
    y_vals = np.linspace(y_min, y_max, ny)
    X, Y = np.meshgrid(x_vals, y_vals)

    # Compute E everywhere
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    for i in range(ny):
        for j in range(nx):
            Ex[i, j], Ey[i, j] = E_field(X[i, j], Y[i, j])

    # Plot
    fig, ax = plt.subplots(figsize=(7, 7))
    strm = ax.streamplot(X, Y, Ex, Ey,
                         density=1.2,
                         linewidth=1,
                         arrowsize=1,
                         color=np.hypot(Ex, Ey),
                         cmap='viridis')

    # Add a colorbar for the field magnitude
    cb = fig.colorbar(strm.lines, ax=ax, orientation='vertical')
    cb.set_label('Field magnitude |E|')

    # Draw the interface y=0
    ax.axhline(0, color='k', linewidth=2)
    ax.text(-1.9, 0.05, 'Interface (y=0)', fontsize=10, ha='left')

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(
        f"E-field refraction\n"
        f"eps1={eps1}, eps2={eps2}, theta1={theta1_deg:.1f}°, theta2={theta2_deg:.1f}°"
    )
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
