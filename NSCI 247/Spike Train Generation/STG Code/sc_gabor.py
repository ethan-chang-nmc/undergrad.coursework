import numpy as np
import matplotlib.pyplot as plt

# Define the parameters
sigma_x = 1  # degrees
sigma_y = 2  # degrees
k = 1 / 0.56  # 1/k in the problem
phi = np.pi / 2  # phase shift

# Define the grid: 50x50 image with 1 pixel = 0.2x0.2 degrees
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Compute the Gabor function
RF = (1 / (2 * np.pi * sigma_x * sigma_y)) * np.exp(-(X**2 / (2 * sigma_x**2) + Y**2 / (2 * sigma_y**2))) * np.cos(k * X - phi)

'''
# Apply the nonlinearity: f(x) = x^2 if x > 0, else 0
RF_nonlinear = np.where(RF > 0, RF**2, 0)
'''
# Plot the 2D receptive field (nonlinear)
plt.figure(figsize=(6, 6))
plt.imshow(RF, extent=(-5, 5, -5, 5), cmap='jet', origin='lower')
plt.colorbar(label='Receptive Field Response')
plt.title('2D Receptive Field')
plt.xlabel('x (degrees)')
plt.ylabel('y (degrees)')
plt.show()

# Plot the cross-section at y = 0 (along the x-axis)
cross_section_y0 = RF[len(y)//2, :]  # middle row, corresponding to y = 0
plt.figure(figsize=(6, 4))
plt.plot(x, cross_section_y0, label='Cross-section at y=0')
plt.title('Cross-section at y = 0')
plt.xlabel('x (degrees)')
plt.ylabel('Receptive Field Response')
plt.grid(True)
plt.legend()
plt.show()
