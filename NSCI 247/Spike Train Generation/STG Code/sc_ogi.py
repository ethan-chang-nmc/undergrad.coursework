import numpy as np
import matplotlib.pyplot as plt

# Define a function to compute the oriented grating image
def compute_oriented_grating_image(k, X, Y, theta):
    # Compute the oriented grating image I(x, y, theta) = sin(k[x cos(theta) - y sin(theta)])
    return np.sin(k * (X * np.cos(theta) - Y * np.sin(theta)))

# Define a function for half-wave squaring nonlinearity
def half_wave_squared(x):
    return np.where(x > 0, x**2, 0)

# Define the spike rate function
def compute_spike_rate(RF, image, peak_firing_rate=50):
    # Flatten both the RF and image
    RF_flat = RF.flatten()
    image_flat = image.flatten()

    # Compute the dot product between RF and image
    response = np.dot(RF_flat, image_flat)

    # Scale the output so that the peak firing rate is 50 Hz
    max_response = np.max(response)
    if max_response > 0:
        scaled_response = (response / max_response) * peak_firing_rate
    else:
        scaled_response = 0  # If no positive response, no firing

    return scaled_response

# Define orientations for vertical and horizontal gratings
theta_vertical = 0  # Vertical orientation
theta_horizontal = np.pi / 2  # Horizontal orientation

# Reuse previously defined variables for k, X, and Y
sigma_x = 1  # degrees
sigma_y = 2  # degrees
k = 1 / 0.56  # 1/k as given in the problem
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Compute the grating images for vertical and horizontal orientations
grating_image_vertical = compute_oriented_grating_image(k, X, Y, theta_vertical)
grating_image_horizontal = compute_oriented_grating_image(k, X, Y, theta_horizontal)

# Plot the vertical and horizontal grating images
plt.figure(figsize=(12, 5))

# Plot vertical grating
plt.subplot(1, 2, 1)
plt.imshow(grating_image_vertical, extent=(-5, 5, -5, 5), cmap='gray', origin='lower')
plt.colorbar(label='Intensity')
plt.title('Vertical Grating (θ = 0)')
plt.xlabel('x (degrees)')
plt.ylabel('y (degrees)')

# Plot horizontal grating
plt.subplot(1, 2, 2)
plt.imshow(grating_image_horizontal, extent=(-5, 5, -5, 5), cmap='gray', origin='lower')
plt.colorbar(label='Intensity')
plt.title('Horizontal Grating (θ = π/2)')
plt.xlabel('x (degrees)')
plt.ylabel('y (degrees)')

plt.tight_layout()
plt.show()

# Now compute the tuning curve for different orientations
theta_values = np.linspace(0, np.pi, 100)  # Orientations from 0 to π (vertical to horizontal and back)
spike_rates = []

# Define the previously computed RF_nonlinear or the receptive field (nonlinear Gabor function)
RF = (1 / (2 * np.pi * sigma_x * sigma_y)) * np.exp(-(X**2 / (2 * sigma_x**2) + Y**2 / (2 * sigma_y**2))) * np.cos(k * X - np.pi / 2)

# Compute spike rate for each orientation
for theta in theta_values:
    # Compute the oriented grating image for the current orientation
    grating_image = compute_oriented_grating_image(k, X, Y, theta)
    
    # Compute the spike rate in response to the grating image
    spike_rate = compute_spike_rate(RF, grating_image)
    
    # Store the result
    spike_rates.append(spike_rate)

# Plot the tuning curve (spike rate vs orientation)
plt.figure(figsize=(8, 5))
plt.plot(theta_values, spike_rates)
plt.title('Tuning Curve: Spike Rate vs Orientation')
plt.xlabel('Orientation (θ)')
plt.ylabel('Spike Rate (Hz)')
plt.grid(True)
plt.show()
