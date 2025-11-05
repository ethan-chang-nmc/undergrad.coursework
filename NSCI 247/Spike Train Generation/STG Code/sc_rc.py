# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
from scipy.stats import pearsonr

# Parameters
image_size = (50, 50)
num_images = 10000
mean_spike_rate = 0.2  # Average spike count per image

# Define the RF (Receptive Field) again
sigma_x = 1  # degrees
sigma_y = 2  # degrees
k = 1 / 0.56  # 1/k as given in the problem
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Compute the Gabor function (RF)
RF = (1 / (2 * np.pi * sigma_x * sigma_y)) * np.exp(-(X**2 / (2 * sigma_x**2) + Y**2 / (2 * sigma_y**2))) * np.cos(k * X - np.pi / 2)

# Generate 10,000 white noise images (each pixel value drawn from N(0, 1))
white_noise_images = np.random.normal(0, 1, (num_images, *image_size))

# Compute the firing rate for each image by calculating the dot product with the RF (flattened)
RF_flat = RF.flatten()
firing_rates = np.dot(white_noise_images.reshape(num_images, -1), RF_flat)

# Normalize firing rates so that the mean firing rate is scaled
firing_rates = (firing_rates / np.mean(firing_rates)) * mean_spike_rate

# Ensure that firing rates are non-negative
firing_rates = np.maximum(firing_rates, 0)

# Simulate spiking responses using Poisson process
spikes = poisson.rvs(firing_rates)

# Part 2: Compute the STA (Spike-Triggered Average)
# Select images that produced at least 1 spike
spike_triggered_images = white_noise_images[spikes > 0]

# Compute STA by averaging over these images
STA = np.mean(spike_triggered_images, axis=0)

# Plot the STA and RF (nonlinear) for comparison
plt.figure(figsize=(12, 6))

# Plot the STA
plt.subplot(1, 2, 1)
plt.imshow(STA, cmap='jet', origin='lower')
plt.colorbar(label='STA Intensity')
plt.title('Spike-Triggered Average (STA 10000)')

# Plot the original RF
plt.subplot(1, 2, 2)
plt.imshow(RF, cmap='jet', origin='lower')
plt.colorbar(label='RF Intensity')
plt.title('Original Receptive Field (RF)')

plt.tight_layout()
plt.show()

# Calculate the correlation coefficient between the STA and RF
STA_flat = STA.flatten()
correlation, _ = pearsonr(STA_flat, RF_flat)

# If correlation is negative, flip the sign of the RF
if correlation < 0:
    RF = -RF
    RF_flat = RF.flatten()  # Recompute the flattened RF
    correlation, _ = pearsonr(STA_flat, RF_flat)  # Recalculate correlation

# Print correlation
print(f"Adjusted correlation between STA and RF: {correlation}")


# Print correlation
print(f"Correlation between STA and RF: {correlation}")

# Part 3: Vary the number of white noise images used for STA computation
subset_sizes = [100, 500, 1000, 5000, 10000]
correlations = []

for subset_size in subset_sizes:
    # Compute STA for the subset
    subset_spike_triggered_images = white_noise_images[:subset_size][spikes[:subset_size] > 0]
    subset_STA = np.mean(subset_spike_triggered_images, axis=0)
    
    # Compute the correlation with the original RF
    subset_STA_flat = subset_STA.flatten()
    corr, _ = pearsonr(subset_STA_flat, RF_flat)
    correlations.append(corr)

# Plot the relationship between number of images and correlation
plt.figure(figsize=(8, 5))
plt.plot(subset_sizes, correlations, marker='o')
plt.title('Correlation vs Number of White Noise Images')
plt.xlabel('Number of Images')
plt.ylabel('Correlation with RF')
plt.grid(True)
plt.show()
