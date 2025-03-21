import numpy as np
import matplotlib.pyplot as plt

# Define constants
k = 8.988e9  # Coulomb coefficient in N*m^2/C^2


# Class for representing a point charge
class PointCharge:
    def __init__(self, q, position):
        """
        Initialization of a point charge

        :param q: Charge in coulombs (C). Positive charges will be red, negative charges will be blue
        :param position: A tuple of (x, y) coordinates of the charge location
        """
        self.q = q
        self.position = np.array(position)


# Function for calculating the electric field from one charge
def electric_field(charge, X, Y):
    """
    Calculation of the electric field from a single point charge

    :param charge: PointCharge object
    :param X: Coordinate grid along the X axis
    :param Y: Coordinate grid along the Y axis
    :return: Electric field components Ex and Ey
    """
    dx = X - charge.position[0]
    dy = Y - charge.position[1]
    r_squared = dx ** 2 + dy ** 2
    r = np.sqrt(r_squared)
    # Avoid division by zero
    r_squared[r_squared == 0] = 1e-20
    Ex = k * charge.q * dx / r_squared ** (3 / 2)
    Ey = k * charge.q * dy / r_squared ** (3 / 2)
    return Ex, Ey


# Create a list of point charges
charges = [
    PointCharge(1e-9, (0, 0)),  # Positive charge at the origin
    PointCharge(-1e-9, (1, 0)),  # Negative charge is shifted along the X axis
    PointCharge(1e-9, (0, 1)),  # Another positive charge
    PointCharge(-1e-9, (-1, 0))  # Another negative charge
]

# Create a grid of points to visualize the field
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)

# Initialize electric field components
Ex_total = np.zeros_like(X)
Ey_total = np.zeros_like(Y)

# Summation of fields from all charges
for charge in charges:
    Ex, Ey = electric_field(charge, X, Y)
    Ex_total += Ex
    Ey_total += Ey

# Normalize field vectors to display directions
E_magnitude = np.sqrt(Ex_total ** 2 + Ey_total ** 2)
# Avoid division by zero
E_magnitude[E_magnitude == 0] = 1e-20
Ex_norm = Ex_total / E_magnitude
Ey_norm = Ey_total / E_magnitude

# Plot a graph
plt.figure(figsize=(8, 8))
plt.streamplot(X, Y, Ex_total, Ey_total, color=np.log(E_magnitude), cmap='inferno', density=1.2, linewidth=1)
plt.colorbar(label='Logarithm of the magnitude of the electric field')

# Display point charges
for charge in charges:
    if charge.q > 0:
        plt.scatter(charge.position[0], charge.position[1], color='red', s=100,
                    label='Positive charge' if charge == charges[0] else "")
    else:
        plt.scatter(charge.position[0], charge.position[1], color='blue', s=100,
                    label='Negative charge' if charge == charges[1] else "")

plt.title('Electrostatic field of point charges')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.axis('equal')  # For equal scale on axes
plt.show()