import numpy as np
import matplotlib.pyplot as plt

# Parameters
firing_rate = 10  # spikes per second
total_time = 100  # seconds
time_bin = 0.001  # 1 ms time bin (in seconds)
n_bins = int(total_time / time_bin)  # Total number of time bins (100,000)

# Calculate probability of a spike in each time bin
p_spike = firing_rate * time_bin

# Generate spike train using Bernoulli process
spike_train = np.random.binomial(1, p_spike, n_bins)

# Calculate total number of spikes in the first second (first 1000 ms = 1000 bins)
spikes_first_second = np.sum(spike_train[:int(1 / time_bin)])

# Plot the spike train (only for the first second)
plt.eventplot(np.where(spike_train[:int(1 / time_bin)] == 1)[0] * time_bin, orientation='horizontal')
plt.title(f'Spike Train (First Second) - {spikes_first_second} spikes')
plt.xlabel('Time (s)')
plt.ylabel('Neuron')
plt.show()

# Output results
print(f"Total spikes in the first second: {spikes_first_second}")