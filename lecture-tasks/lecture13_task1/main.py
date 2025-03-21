import numpy as np
import matplotlib.pyplot as plt

# Coulomb's constant
k = 8.988e9  # Coulomb's constant in N·m²/C²

# Class to represent a point charge
class PointCharge:
    def __init__(self, q, position):
        """
        Initialize a point charge

        :param q: Charge in coulombs (C). Positive charges will be red, negative charges will be blue
        :param position: Tuple of coordinates (x, y) for the charge location
        """
        self.q = q
        self.position = np.array(position)

# Class to represent a dipole
class Dipole:
    def __init__(self, p, position, orientation):
        """
        Initialize a dipole

        :param p: Dipole moment magnitude (C·m)
        :param position: Center of the dipole (x, y)
        :param orientation: Orientation of the dipole in radians (angle from the positive x-axis)
        """
        self.p = p
        self.position = np.array(position)
        self.orientation = orientation

    def get_charges(self, separation):
        """
        Get the charges of the dipole

        :param separation: Distance between the charges (m)
        :return: A list of PointCharge objects representing the dipole
        """
        half_separation = separation / 2
        dx = half_separation * np.cos(self.orientation)
        dy = half_separation * np.sin(self.orientation)
        positive_charge = PointCharge(self.p / separation, self.position + np.array([dx, dy]))
        negative_charge = PointCharge(-self.p / separation, self.position - np.array([dx, dy]))
        return [positive_charge, negative_charge]

# Function to calculate the electric field from a single charge
def electric_field(charge, X, Y):
    dx = X - charge.position[0]
    dy = Y - charge.position[1]
    r_squared = dx**2 + dy**2
    r = np.sqrt(r_squared)
    # Avoid division by zero
    r_squared[r_squared == 0] = 1e-20
    Ex = k * charge.q * dx / r_squared**(3/2)
    Ey = k * charge.q * dy / r_squared**(3/2)
    return Ex, Ey

# Function to calculate the potential from a single charge
def potential(charge, X, Y):
    dx = X - charge.position[0]
    dy = Y - charge.position[1]
    r = np.sqrt(dx**2 + dy**2)
    # Avoid division by zero
    r[r == 0] = 1e-20
    V = k * charge.q / r
    return V

# Function to calculate the force and torque on a dipole
def force_and_torque(dipole, Ex, Ey):
    """
    Calculate the net force and torque acting on a dipole

    :param dipole: Dipole object
    :param Ex: X-component of the electric field at the dipole's position
    :param Ey: Y-component of the electric field at the dipole's position
    :return: Force vector (Fx, Fy) and torque (T)
    """
    F = dipole.p * np.array([Ex, Ey])
    torque = dipole.p * (Ey * np.cos(dipole.orientation) - Ex * np.sin(dipole.orientation))
    return F, torque

# Create a list of point charges
charges = [
    PointCharge(1e-9, (0, 0)),      # Positive charge at the origin
    PointCharge(-1e-9, (1, 0)),     # Negative charge offset along the X-axis
    PointCharge(1e-9, (0, 1)),      # Another positive charge
    PointCharge(-1e-9, (-1, 0))     # Another negative charge
]

# Create a grid of points for visualizing the field
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)

# Initialize components of the electric field and potential
Ex_total = np.zeros_like(X)
Ey_total = np.zeros_like(Y)
V_total = np.zeros_like(X)

# Sum contributions from all charges
for charge in charges:
    Ex, Ey = electric_field(charge, X, Y)
    V = potential(charge, X, Y)
    Ex_total += Ex
    Ey_total += Ey
    V_total += V

# Normalize the field vectors for visualization of directions
E_magnitude = np.sqrt(Ex_total**2 + Ey_total**2)
# Avoid division by zero
E_magnitude[E_magnitude == 0] = 1e-20
Ex_norm = Ex_total / E_magnitude
Ey_norm = Ey_total / E_magnitude

# Get dipole parameters from the user
dipole_x = float(input("Enter the x-coordinate of the dipole's center: "))
dipole_y = float(input("Enter the y-coordinate of the dipole's center: "))
dipole_p = float(input("Enter the dipole moment magnitude (C·m): "))
dipole_orientation = float(input("Enter the dipole orientation in degrees (angle from the positive x-axis): "))
dipole_orientation = np.radians(dipole_orientation)  # Convert to radians

# Add a dipole to the field
dipole = Dipole(p=dipole_p, position=(dipole_x, dipole_y), orientation=dipole_orientation)
dipole_charges = dipole.get_charges(separation=0.2)

# Calculate the force and torque on the dipole at its position
Ex_dipole = np.interp(dipole.position[0], x, Ex_total[:, np.searchsorted(y, dipole.position[1])])
Ey_dipole = np.interp(dipole.position[1], y, Ey_total[np.searchsorted(x, dipole.position[0]), :])
F, torque = force_and_torque(dipole, Ex_dipole, Ey_dipole)
print(f"Force on the dipole: Fx={F[0]:.3e} N, Fy={F[1]:.3e} N")
print(f"Torque on the dipole: T={torque:.3e} N·m")

# Add the dipole's charges to the visualization
for charge in dipole_charges:
    charges.append(charge)
    Ex, Ey = electric_field(charge, X, Y)
    V = potential(charge, X, Y)
    Ex_total += Ex
    Ey_total += Ey
    V_total += V

# Plotting
plt.figure(figsize=(8, 8))

# Visualize electric field lines
strm = plt.streamplot(X, Y, Ex_total, Ey_total, color=np.log(E_magnitude), cmap='inferno', density=1.2, linewidth=1)

# Add color bar for the field lines
plt.colorbar(strm.lines, label='Logarithm of Electric Field Magnitude')

# Visualize equipotential lines
levels = np.linspace(V_total.min(), V_total.max(), 50)
contours = plt.contour(X, Y, V_total, levels=levels, colors='green', linestyles='dashed', linewidths=0.5)
plt.clabel(contours, inline=1, fontsize=8, fmt='%.1e')

# Display point charges
for charge in charges:
    if charge.q > 0:
        plt.scatter(charge.position[0], charge.position[1], color='red', s=100)
    else:
        plt.scatter(charge.position[0], charge.position[1], color='blue', s=100)

# Add an arrow to indicate the dipole
arrow_dx = 0.3 * np.cos(dipole.orientation)  # Scale for visualization
arrow_dy = 0.3 * np.sin(dipole.orientation)
plt.arrow(dipole.position[0] - 0.15 * arrow_dx, dipole.position[1] - 0.15 * arrow_dy,
          arrow_dx, arrow_dy, head_width=0.1, head_length=0.1, fc='purple', ec='purple', label='Dipole')

# Add legend for charges
plt.scatter([], [], color='red', s=100, label='Positive Charge')
plt.scatter([], [], color='blue', s=100, label='Negative Charge')
plt.legend(loc='upper right')

plt.title('Electrostatic Field and Equipotential Lines with a Dipole')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.axis('equal')  # Ensure equal axis scaling
plt.tight_layout()
plt.show()
