import numpy as np
import matplotlib.pyplot as plt

# Parameters
V_rest = -65  # Resting potential in mV
V_thresh = -50  # Spiking threshold in mV
V_reset = -70  # Reset potential in mV
V_spike = 40  # Spike potential in mV
tau = 20  # Decay constant in ms
dt = 0.1  # Time step in ms
t_total = 5000  # Total time in ms for 5 seconds
I_const = 1.35  # Constant input
V0 = -65  # Initial membrane potential

# Time array
time = np.arange(0, t_total, dt)

# Function to simulate the membrane potential over time and extract spike times
def membrane_potential_and_spikes(I, V0):
    V = np.zeros(len(time))  # Membrane potential array
    V[0] = V0  # Initial condition
    spike_times = []  # List to store spike times (in ms)

    for t in range(1, len(time)):
        if V[t-1] == V_spike:
            V[t] = V_reset # Reset after spike
        else:
            dV = ((-dt/tau) * (V[t-1] - V_rest)) + (dt * I[t-1])  # Euler method
            V[t] = V[t-1] + dV

            if V[t-1] == V_spike:
                V[t] = V_reset  # Reset after spike

            if V[t] >= V_thresh:  # Spike condition
                V[t] = V_spike  # Set spike
                spike_times.append(t * dt)  # Store spike time

            if t < len(time) - 1 and V[t] < V_reset:  # Ensure graph doesn't dip below reset
                V[t] = V_reset

    return V, spike_times

# Vary sigma_I and calculate CV and spike rate
sigma_I_values = np.linspace(0, 100, 400)  # Range of sigma_I values to test
CV_values = []
spike_rates = []

for sigma_I in sigma_I_values:
    # Generate input current with variability
    I = np.random.normal(I_const, sigma_I, len(time))

    # Compute membrane potential and spike times
    V, spike_times = membrane_potential_and_spikes(I, V0)

    # Calculate the inter-spike intervals (ISI)
    spike_times = np.array(spike_times)
    ISI = np.diff(spike_times)  # Calculate ISI using the diff of spike times

    if len(ISI) > 0:
        # Calculate the coefficient of variation (CV)
        mean_ISI = np.mean(ISI)
        std_ISI = np.std(ISI)
        CV = std_ISI / mean_ISI
        CV_values.append(CV)

        # Calculate the spike rate (spikes per second)
        spike_rate = len(spike_times) / (t_total / 1000)  # Total spikes / total time in seconds
        spike_rates.append(spike_rate)
    else:
        # In case no spikes occur, set CV and spike rate to 0
        CV_values.append(0)
        spike_rates.append(0)

# Plot CV as a function of σ
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(sigma_I_values, CV_values)
plt.title("CV as a Function of σ")
plt.xlabel("σ")
plt.ylabel("CV")
plt.grid(True)

# Plot Spike Rate as a function of σ
plt.subplot(2, 1, 2)
plt.plot(sigma_I_values, spike_rates, color='orange')
plt.title("Spike Rate as a Function of σ")
plt.xlabel("σ")
plt.ylabel("Spike Rate (spikes/sec)")
plt.grid(True)

plt.tight_layout()
plt.show()
