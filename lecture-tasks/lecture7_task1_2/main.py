import numpy as np
import matplotlib.pyplot as plt

# Enter expressions for Fx and Fy from the console
Fx_expr = input("Enter the expression for Fx(x, y): ")
Fy_expr = input("Enter the expression for Fy(x, y): ")

# Create functions to calculate Fx and Fy
def Fx(x, y):
    return eval(Fx_expr)

def Fy(x, y):
    return eval(Fy_expr)

# Create a grid of x and y values
x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x, y)

# Calculate Fx and Fy on a grid
Fx_values = Fx(X, Y)
Fy_values = Fy(X, Y)

# Initialization of potential energy U
U = np.zeros_like(X)

# Steps in x and y
dx = x[1] - x[0]
dy = y[1] - y[0]

# Calculate potential energy U(x, y)
# Integrate the force along the x and y axes
for i in range(1, X.shape[0]):
    U[i, 0] = U[i-1, 0] - Fx_values[i-1, 0] * dx
for j in range(1, Y.shape[1]):
    U[:, j] = U[:, j-1] - Fy_values[:, j-1] * dy

# Visualization of potential field U(x, y)
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, U, levels=50, cmap='magma')
plt.colorbar(contour)
plt.title("Distribution of potential energy U(x, y)")
plt.xlabel("x")
plt.ylabel("y")
plt.show()