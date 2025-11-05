import numpy as np
import matplotlib.pyplot as plt

# Define the parameters
sigma_x = 1  # degrees
sigma_y = 2  # degrees
k = 1 / 0.56  # 1/k as given in the problem
phi = np.pi / 2  # phase shift

# Define the grid: 50x50 image with 1 pixel = 0.2x0.2 degrees
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Compute the Gabor function (RF)
RF = (1 / (2 * np.pi * sigma_x * sigma_y)) * np.exp(-(X**2 / (2 * sigma_x**2) + Y**2 / (2 * sigma_y**2))) * np.cos(k * X - phi)
'''
# Apply the nonlinearity: f(x) = x^2 if x > 0, else 0
RF_nonlinear = np.where(RF > 0, RF**2, 0)
'''
# Function to compute the grating image
def compute_grating_image(k, X, alpha):
    # Compute the vertical grating image I(x, y) = sin(kx - alpha)
    return np.sin(k * X - alpha)
'''
# Function for half-wave squaring nonlinearity
def half_wave_squared(x):
    return np.where(x > 0, x**2, 0)
'''
# Function to compute spike rate
def compute_spike_rate(RF, image, peak_firing_rate=50):
    # Compute the dot product between RF and image (already sums across the pixels)
    response = np.sum(RF * image)

    # Normalize the response to be within [0, peak_firing_rate]
    if response > 0:
        scaled_response = (response / np.max(response)) * peak_firing_rate
    else:
        scaled_response = 0  # No response if response is non-positive

    return scaled_response
    
# Define alpha values for the phase shift
alpha_values = np.linspace(0, 2 * np.pi, 100)

# Calculate the mean spike rate for each phase
spike_rates = []
for alpha in alpha_values:
    # Compute the grating image for the current phase
    grating_image = compute_grating_image(k, X, alpha)
    
    # Compute the spike rate in response to the grating image
    spike_rate = compute_spike_rate(RF, grating_image)
    
    # Store the result
    spike_rates.append(spike_rate)

# Plot the mean spike rate as a function of the phase of the grating
plt.figure(figsize=(8, 5))
plt.plot(alpha_values, spike_rates)
plt.title('Mean Spike Rate vs Phase of Grating')
plt.xlabel('Phase (alpha)')
plt.ylabel('Mean Spike Rate (Hz)')
plt.grid(True)
plt.show()
