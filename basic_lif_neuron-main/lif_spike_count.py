import numpy as np
import matplotlib.pyplot as plt

# Parameters
V_rest = -65  # Resting potential in mV
V_thresh = -50  # Spiking threshold in mV
V_reset = -70  # Reset potential in mV
V_spike = 40  # Spike potential in mV
tau = 20  # Decay constant in ms
dt = 0.1  # Time step in ms
t_total = 1000  # Total time in ms
I_const = 0  # Constant input
I_step = 0.1
I_total = 2.5
V0 = -65  # Initial membrane potential

#Input array
inputs = np.arange(0, I_total, I_step)

# Time array
time = np.arange(0, t_total, dt)

# Input current at each time
I = np.zeros(len(time)) + I_const

# Function to simulate the membrane potential over time
def membrane_potential(I, V0):
    V = np.zeros(len(time))  # Membrane potential array
    V[0] = V0  # Initial condition
    spike_count = 0 #number of spikes

    for t in range(1, len(time)):
        if V[t-1] == V_spike:
            V[t] = V_reset # Reset if previous was spike
        else:
            dV = ((-dt/tau) * (V[t-1] - V_rest)) + (dt * I[t-1])  # Euler method
            V[t] = V[t-1] + dV

            if V[t-1] == V_spike:
                V[t] = V_reset # Reset if previous was spike

            if V[t] >= V_thresh:  # Spike condition
                V[t] = V_spike  # Set spike
                spike_count += 1 # Increases spike count

            if t < len(time) - 1:
                if V[t] < V_reset:  # Ensuring graph does not dip below reset
                    V[t] = V_reset

    return spike_count

#spikes array
inpspike = np.zeros(len(inputs))
# Compute the spikes for each input
for t in range (0, len(inputs)):
    inpspike[t] = membrane_potential(I, V0)
    I_const += I_step
    I = np.zeros(len(time)) + I_const

# Plot the results
plt.plot(inputs, inpspike)
plt.title("Input Current vs Spikes Generated (V(0) = -65)")
plt.xlabel("Input Current (V/s)")
plt.ylabel("Spikes Generated (spikes/second)")
plt.grid(True)
plt.show()
