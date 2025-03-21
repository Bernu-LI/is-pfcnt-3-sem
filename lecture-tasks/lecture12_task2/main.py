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

# Function to calculate the electric field from a single charge
def electric_field(charge, X, Y):
    """
    Calculate the electric field from a single point charge

    :param charge: PointCharge object
    :param X: Grid of X coordinates
    :param Y: Grid of Y coordinates
    :return: Components of the electric field Ex and Ey
    """
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
    """
    Calculate the electric potential from a single point charge

    :param charge: PointCharge object
    :param X: Grid of X coordinates
    :param Y: Grid of Y coordinates
    :return: Potential V
    """
    dx = X - charge.position[0]
    dy = Y - charge.position[1]
    r = np.sqrt(dx**2 + dy**2)
    # Avoid division by zero
    r[r == 0] = 1e-20
    V = k * charge.q / r
    return V

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
        plt.scatter(charge.position[0], charge.position[1], color='red', s=100,
                    label='Positive Charge' if charge == charges[0] else "")
    else:
        plt.scatter(charge.position[0], charge.position[1], color='blue', s=100,
                    label='Negative Charge' if charge == charges[1] else "")

plt.title('Electrostatic Field and Equipotential Lines of Point Charges')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc='upper right')
plt.grid(True)
plt.axis('equal')  # Ensure equal axis scaling
plt.tight_layout()
plt.show()
