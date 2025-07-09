import numpy as np
import matplotlib.pyplot as plt

# Parameters
V_rest = -65  # Resting potential in mV
V_thresh = -50  # Spiking threshold in mV
V_reset = -70  # Reset potential in mV
V_spike = 40  # Spike potential in mV
tau = 20  # Decay constant in ms
dt = 0.1  # Time step in ms
t_total = 100  # Total time in ms
I_const = 0.76  # Constant input
V0 = -65  # Initial membrane potential

# Time array
time = np.arange(0, t_total, dt)

# Input current at each time
I = np.zeros(len(time)) + I_const

# Function to simulate the membrane potential over time
def membrane_potential(I, V0):
    V = np.zeros(len(time))  # Membrane potential array
    V[0] = V0  # Initial condition

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

            if t < len(time) - 1:
                if V[t] < V_reset:  # Ensuring graph does not dip below reset
                    V[t] = V_reset

    return V

# Compute the membrane potential
V = membrane_potential(I, V0)

# Plot the results
plt.plot(time, V)
plt.title("Membrane Potential vs Time (I(t) = 0.76, V(0) = -65)")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential (mV)")
plt.grid(True)
plt.show()
