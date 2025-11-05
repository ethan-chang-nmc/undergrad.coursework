import numpy as np
import matplotlib.pyplot as plt

# Define constants
N = 100  # Number of neurons
kappa = 1
f_max = 20  # spikes/s
f0 = 5  # spikes/s
n_trials = 1000  # Number of trials for simulations

def degrees_to_radians(degrees):
    return degrees * np.pi / 180

def get_population_response(c, phi, phi_prefs, kappa, f_max, f0):
    """
    Returns the simulated population response (spike counts) and mean firing rates
    for a given contrast c and stimulus orientation phi.
    """
    delta_phi = phi - phi_prefs
    f = f0 + c * (f_max - f0) * np.exp(kappa * (np.cos(2 * delta_phi) - 1))
    r = np.random.poisson(f)  # Simulate Poisson spike counts
    return r, f

# (a) Define preferred orientations
phi_prefs = np.linspace(0, np.pi, N, endpoint=False)

# Part (a)(i): Plot population responses for c = 1 and c = 0.1 at phi = pi/4
phi = np.pi / 4
c_values = [1, 0.1]
responses = []

for c in c_values:
    r, _ = get_population_response(c, phi, phi_prefs, kappa, f_max, f0)
    responses.append(r)

plt.figure()
for i, r in enumerate(responses):
    plt.plot(phi_prefs, r, label=f'c = {c_values[i]}')
plt.xlabel('Preferred Orientation (rad)')
plt.ylabel('Spike Count')
plt.title('Population Responses at phi = π/4 for Different Contrasts')
plt.legend()
plt.show()

# Part (a)(ii): Plot population responses for different Δφ
Delta_phi_degrees_list = [10, 20, 30]
for Delta_phi_degrees in Delta_phi_degrees_list:
    Delta_phi = degrees_to_radians(Delta_phi_degrees)
    phi1 = Delta_phi / 2
    phi2 = -Delta_phi / 2
    r1, _ = get_population_response(1, phi1, phi_prefs, kappa, f_max, f0)
    r2, _ = get_population_response(1, phi2, phi_prefs, kappa, f_max, f0)
    
    plt.figure()
    plt.plot(phi_prefs, r1, label=f'φ₁ = {Delta_phi_degrees/2}°')
    plt.plot(phi_prefs, r2, label=f'φ₂ = {-Delta_phi_degrees/2}°')
    plt.xlabel('Preferred Orientation (rad)')
    plt.ylabel('Spike Count')
    plt.title(f'Population Responses for Δφ = {Delta_phi_degrees}°')
    plt.legend()
    plt.show()

# (b) Compute covariance matrix assuming independent neurons at φ = 0
_, f = get_population_response(1, 0, phi_prefs, kappa, f_max, f0)
C = np.diag(f)  # Variance equals mean rate for Poisson neurons

# (c) Compute read-out weights w^{fac} and plot against preferred orientations
for Delta_phi_degrees in Delta_phi_degrees_list:
    Delta_phi = degrees_to_radians(Delta_phi_degrees)
    phi1 = Delta_phi / 2
    phi2 = -Delta_phi / 2
    _, f1 = get_population_response(1, phi1, phi_prefs, kappa, f_max, f0)
    _, f2 = get_population_response(1, phi2, phi_prefs, kappa, f_max, f0)
    f_prime = (f1 - f2) / (phi1 - phi2)
    w_fac = f_prime / f  # Since C is diagonal
    
    plt.figure()
    plt.plot(phi_prefs, w_fac)
    plt.xlabel('Preferred Orientation (rad)')
    plt.ylabel('Read-out Weight w^{fac}')
    plt.title(f'Read-out Weights for Δφ = {Delta_phi_degrees}°')
    plt.show()

# (d) Simulate decision variable R for φ₁ = 5° and φ₂ = -5°
phi1 = degrees_to_radians(5)
phi2 = degrees_to_radians(-5)

# For contrast c = 1
_, f = get_population_response(1, 0, phi_prefs, kappa, f_max, f0)
_, f1 = get_population_response(1, phi1, phi_prefs, kappa, f_max, f0)
_, f2 = get_population_response(1, phi2, phi_prefs, kappa, f_max, f0)
f_prime = (f1 - f2) / (phi1 - phi2)
w_fac = f_prime / f

R1 = []
R2 = []
for _ in range(n_trials):
    r1, _ = get_population_response(1, phi1, phi_prefs, kappa, f_max, f0)
    R1.append(np.dot(w_fac, r1))
    r2, _ = get_population_response(1, phi2, phi_prefs, kappa, f_max, f0)
    R2.append(np.dot(w_fac, r2))

R1 = np.array(R1)
R2 = np.array(R2)
d_prime = (np.mean(R1) - np.mean(R2)) / np.sqrt(0.5 * (np.var(R1) + np.var(R2)))

plt.figure()
plt.hist(R1, bins=30, alpha=0.5, label='φ₁ = 5°')
plt.hist(R2, bins=30, alpha=0.5, label='φ₂ = -5°')
plt.xlabel('Decision Variable R')
plt.ylabel('Frequency')
plt.title(f'Decision Variable Distribution (c = 1), d\' = {d_prime:.2f}')
plt.legend()
plt.show()

# Repeat for contrast c = 0.1
_, f = get_population_response(0.1, 0, phi_prefs, kappa, f_max, f0)
_, f1 = get_population_response(0.1, phi1, phi_prefs, kappa, f_max, f0)
_, f2 = get_population_response(0.1, phi2, phi_prefs, kappa, f_max, f0)
f_prime = (f1 - f2) / (phi1 - phi2)
w_fac = f_prime / f

R1_c01 = []
R2_c01 = []
for _ in range(n_trials):
    r1, _ = get_population_response(0.1, phi1, phi_prefs, kappa, f_max, f0)
    R1_c01.append(np.dot(w_fac, r1))
    r2, _ = get_population_response(0.1, phi2, phi_prefs, kappa, f_max, f0)
    R2_c01.append(np.dot(w_fac, r2))

R1_c01 = np.array(R1_c01)
R2_c01 = np.array(R2_c01)
d_prime_c01 = (np.mean(R1_c01) - np.mean(R2_c01)) / np.sqrt(0.5 * (np.var(R1_c01) + np.var(R2_c01)))

plt.figure()
plt.hist(R1_c01, bins=30, alpha=0.5, label='φ₁ = 5°')
plt.hist(R2_c01, bins=30, alpha=0.5, label='φ₂ = -5°')
plt.xlabel('Decision Variable R')
plt.ylabel('Frequency')
plt.title(f'Decision Variable Distribution (c = 0.1), d\' = {d_prime_c01:.2f}')
plt.legend()
plt.show()

# (e) Dependency of d' on number of neurons N
N_list = [2**i for i in range(1, 11)]  # N from 2 to 1024
d_prime_N = []
c = 0.1

for N in N_list:
    phi_prefs = np.linspace(0, np.pi, N, endpoint=False)
    _, f = get_population_response(c, 0, phi_prefs, kappa, f_max, f0)
    _, f1 = get_population_response(c, phi1, phi_prefs, kappa, f_max, f0)
    _, f2 = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)
    f_prime = (f1 - f2) / (phi1 - phi2)
    w_fac = f_prime / f
    
    R1 = []
    R2 = []
    for _ in range(n_trials):
        r1, _ = get_population_response(c, phi1, phi_prefs, kappa, f_max, f0)
        R1.append(np.dot(w_fac, r1))
        r2, _ = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)
        R2.append(np.dot(w_fac, r2))
    
    d_prime_N.append((np.mean(R1) - np.mean(R2)) / np.sqrt(0.5 * (np.var(R1) + np.var(R2))))

plt.figure()
plt.plot(N_list, d_prime_N, marker='o')
plt.xscale('log')
plt.xlabel('Number of Neurons N')
plt.ylabel('d\'')
plt.title('Dependency of d\' on Number of Neurons (c = 0.1)')
plt.show()

# (f) Dependency of d' on κ (kappa)
kappa_list = np.linspace(0.5, 5, 10)
d_prime_kappa = []
N = 100
phi_prefs = np.linspace(0, np.pi, N, endpoint=False)
c = 1

for kappa_value in kappa_list:
    _, f = get_population_response(c, 0, phi_prefs, kappa_value, f_max, f0)
    _, f1 = get_population_response(c, phi1, phi_prefs, kappa_value, f_max, f0)
    _, f2 = get_population_response(c, phi2, phi_prefs, kappa_value, f_max, f0)
    f_prime = (f1 - f2) / (phi1 - phi2)
    w_fac = f_prime / f
    
    R1 = []
    R2 = []
    for _ in range(n_trials):
        r1, _ = get_population_response(c, phi1, phi_prefs, kappa_value, f_max, f0)
        R1.append(np.dot(w_fac, r1))
        r2, _ = get_population_response(c, phi2, phi_prefs, kappa_value, f_max, f0)
        R2.append(np.dot(w_fac, r2))
    
    d_prime_kappa.append((np.mean(R1) - np.mean(R2)) / np.sqrt(0.5 * (np.var(R1) + np.var(R2))))

plt.figure()
plt.plot(kappa_list, d_prime_kappa, marker='o')
plt.xlabel('κ (kappa)')
plt.ylabel('d\'')
plt.title('Dependency of d\' on κ (N = 100, c = 1)')
plt.show()
