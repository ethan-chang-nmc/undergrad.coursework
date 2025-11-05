import numpy as np
import matplotlib.pyplot as plt

# Parameters
firing_rate = 10  # spikes per second
total_time = 100  # seconds
time_bin = 0.001  # 1 ms time bin (in seconds)

# Calculate the mean of the exponential distribution for ISIs
mean_isi = 1 / firing_rate  # The mean inter-spike interval is the inverse of the firing rate

# Generate ISIs using exponential distribution
isi_times = []
current_time = 0

# Generate ISIs until we exceed 100 seconds
while current_time < total_time:
    isi = np.random.exponential(mean_isi)
    current_time += isi
    isi_times.append(current_time)

# Convert ISIs into a spike train of 0's and 1's
n_bins = int(total_time / time_bin)
spike_train = np.zeros(n_bins)

# Mark spikes in the corresponding time bin (rounded)
for isi in isi_times:
    if isi < total_time:
        spike_bin = int(isi / time_bin)
        spike_train[spike_bin] = 1

# Count the number of spikes in the first second (first 1000 bins)
spikes_first_second = np.sum(spike_train[:int(1 / time_bin)])

# Plot the spike train (only for the first second)
plt.eventplot(np.where(spike_train[:int(1 / time_bin)] == 1)[0] * time_bin, orientation='horizontal')
plt.title(f'Spike Train (First Second) - {spikes_first_second} spikes')
plt.xlabel('Time (s)')
plt.ylabel('Neuron')
plt.show()

# Output results
print(f"Total spikes in the first second: {spikes_first_second}")
