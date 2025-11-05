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
sigma_I = 10  # Standard deviation for the input current

# Time array
time = np.arange(0, t_total, dt)

# Input current with variability at each time point
I = np.random.normal(I_const, sigma_I, len(time))

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

# Compute the membrane potential and spike times
V, spike_times = membrane_potential_and_spikes(I, V0)

# Calculate the inter-spike intervals (ISI)
spike_times = np.array(spike_times)  # Convert list to array
ISI = np.diff(spike_times)  # Calculate ISI using the diff of spike times

# Calculate the coefficient of variation (CV)
mean_ISI = np.mean(ISI)
std_ISI = np.std(ISI)
CV = std_ISI / mean_ISI

# Create a figure with subplots
plt.figure(figsize=(10, 8))

# Subplot 1: Membrane potential for the first 100 ms
plt.subplot(2, 1, 1)  # 2 rows, 1 column, 1st subplot
plt.plot(time[:int(100/dt)], V[:int(100/dt)])
plt.title("Membrane Potential vs Time (First 100 ms, I(0) = 1.35, V(0) = -65, σ = 10)")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential (mV)")
plt.grid(True)

# Subplot 2: ISI distribution over 5 seconds with CV in the title
plt.subplot(2, 1, 2)  # 2 rows, 1 column, 2nd subplot
plt.hist(ISI, bins=20, edgecolor='black')
plt.title(f"Inter-Spike Interval (ISI) Distribution (CV = {CV:.2f})")
plt.xlabel("ISI (ms)")
plt.ylabel("Frequency")
plt.grid(True)

# Show both plots in the same window
plt.tight_layout()  # Adjusts spacing between subplots
plt.show()

