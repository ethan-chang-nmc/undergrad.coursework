import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

# Parameters
firing_rate = 10  # spikes per second
total_time = 100  # seconds
time_bin = 0.001  # 1 ms time bin
n_bins = int(total_time / time_bin)

# Trial lengths
trial_lengths = [0.5, 0.1]  # seconds

# Function to generate spike train using Bernoulli method
def generate_bernoulli_spike_train(firing_rate, total_time, time_bin):
    p_spike = firing_rate * time_bin
    n_bins = int(total_time / time_bin)
    spike_train = np.random.binomial(1, p_spike, n_bins)
    return spike_train

# Function to generate spike train using Exponential ISI method
def generate_exponential_spike_train(firing_rate, total_time, time_bin):
    spike_train = np.zeros(int(total_time / time_bin))
    current_time = 0
    while current_time < total_time:
        isi = np.random.exponential(1 / firing_rate)  # Generate ISI from exponential distribution
        current_time += isi
        if current_time < total_time:
            spike_bin = int(current_time / time_bin)
            spike_train[spike_bin] = 1
    return spike_train

# Function to calculate spike counts in each trial
def get_spike_counts(spike_train, trial_length, time_bin):
    n_trials = int(total_time / trial_length)
    trial_size = int(trial_length / time_bin)
    spike_counts = [np.sum(spike_train[i * trial_size:(i + 1) * trial_size]) for i in range(n_trials)]
    return spike_counts

# Function to plot histogram and calculate Fano factor
def plot_histogram(spike_counts, trial_length, method_name):
    mean_spikes = np.mean(spike_counts)
    variance_spikes = np.var(spike_counts)
    fano_factor = variance_spikes / mean_spikes
    
    # Poisson distribution with same mean
    poisson_dist = poisson.pmf(np.arange(0, max(spike_counts) + 1), mean_spikes)

    # Plot histogram
    plt.hist(spike_counts, bins=np.arange(0, max(spike_counts) + 1) - 0.5, density=True, alpha=0.75, label="Spike counts")
    plt.plot(np.arange(0, max(spike_counts) + 1), poisson_dist, 'r-', lw=2, label=f'Poisson (mean={mean_spikes:.2f})')
    plt.title(f'{method_name} Trial Length: {trial_length}s, Fano Factor: {fano_factor:.2f}')
    plt.xlabel('Spike Counts')
    plt.ylabel('Probability')
    plt.legend()
    plt.show()

    return fano_factor

# Methods
methods = ["Bernoulli", "Exponential"]

for trial_length in trial_lengths:
    for method in methods:
        if method == "Bernoulli":
            spike_train = generate_bernoulli_spike_train(firing_rate, total_time, time_bin)
        elif method == "Exponential":
            spike_train = generate_exponential_spike_train(firing_rate, total_time, time_bin)

        spike_counts = get_spike_counts(spike_train, trial_length, time_bin)
        fano_factor = plot_histogram(spike_counts, trial_length, method)

        print(f"Method: {method}, Trial Length: {trial_length}s, Fano Factor: {fano_factor:.2f}")
