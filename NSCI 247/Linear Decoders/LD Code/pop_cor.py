# pop_corr.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# Define constants
N = 100  # Number of neurons
kappa = 1
f_max = 20  # spikes/s
f0 = 5  # spikes/s
c = 1  # Contrast
phi1_deg = 5  # degrees
phi2_deg = -5  # degrees
phi1 = np.deg2rad(phi1_deg)
phi2 = np.deg2rad(phi2_deg)
tau = 0.5
rho_max_values = [0.1, 0.3, 0.5, 0.8]
n_trials = 1000

def degrees_to_radians(degrees):
    return degrees * np.pi / 180

def get_population_response(c, phi, phi_prefs, kappa, f_max, f0):
    """
    Returns the mean firing rates f_i for given contrast c and stimulus orientation phi.
    """
    delta_phi = phi - phi_prefs
    f = f0 + c * (f_max - f0) * np.exp(kappa * (np.cos(2 * delta_phi) - 1))
    return f

def compute_correlation_matrix(phi_prefs, rho_max, tau):
    N = len(phi_prefs)
    corr_matrix = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                corr_matrix[i, j] = 1
            else:
                delta_phi = np.abs(phi_prefs[i] - phi_prefs[j])
                delta_phi = (delta_phi + np.pi/2) % np.pi - np.pi/2
                corr_matrix[i, j] = rho_max * np.exp(-np.abs(delta_phi) / tau)
    return corr_matrix

def generate_correlated_responses(mean_rates, cov_matrix):
    # Ensure the covariance matrix is positive definite
    epsilon = 1e-6
    cov_matrix += epsilon * np.eye(len(mean_rates))
    r = multivariate_normal.rvs(mean=mean_rates, cov=cov_matrix)
    r = np.round(r).astype(int)
    r = np.clip(r, 0, None)  # Ensure non-negative spike counts
    return r

def generate_independent_responses(mean_rates):
    r = np.random.poisson(mean_rates)
    return r

# (a) Compute the covariance matrix C_opt
phi_prefs = np.linspace(0, np.pi, N, endpoint=False)  # Preferred orientations

# Variances (Poisson neurons)
f = get_population_response(c, 0, phi_prefs, kappa, f_max, f0)
variances = f

# Compute and plot covariance matrices for rho_max = 0.5
rho_max = 0.5
corr_matrix = compute_correlation_matrix(phi_prefs, rho_max, tau)
C_opt = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        C_opt[i, j] = corr_matrix[i, j] * np.sqrt(variances[i] * variances[j])

plt.figure(figsize=(8,6))
plt.imshow(C_opt, extent=[phi_prefs[0], phi_prefs[-1], phi_prefs[0], phi_prefs[-1]], origin='lower')
plt.colorbar(label='Covariance')
plt.xlabel('Preferred Orientation of Neuron i (rad)')
plt.ylabel('Preferred Orientation of Neuron j (rad)')
plt.title('Covariance Matrix C_opt (rho_max = 0.5)')
plt.show()

# (b) Generate population responses for phi1 and phi2
f1 = get_population_response(c, phi1, phi_prefs, kappa, f_max, f0)
f2 = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)

r1_corr = generate_correlated_responses(f1, C_opt)
r2_corr = generate_correlated_responses(f2, C_opt)

plt.figure()
plt.plot(phi_prefs, r1_corr, label=f'phi1 = {phi1_deg}°')
plt.plot(phi_prefs, r2_corr, label=f'phi2 = {phi2_deg}°')
plt.xlabel('Preferred Orientation (rad)')
plt.ylabel('Spike Count')
plt.title('Correlated Population Responses (Single Trial)')
plt.legend()
plt.show()

# Compare with independent neurons
r1_indep = generate_independent_responses(f1)
r2_indep = generate_independent_responses(f2)

plt.figure()
plt.plot(phi_prefs, r1_indep, label=f'phi1 = {phi1_deg}° (Independent)')
plt.plot(phi_prefs, r2_indep, label=f'phi2 = {phi2_deg}° (Independent)')
plt.xlabel('Preferred Orientation (rad)')
plt.ylabel('Spike Count')
plt.title('Independent Population Responses (Single Trial)')
plt.legend()
plt.show()

# (c) Compute optimal read-out weights w^{opt}
delta_f = f1 - f2

epsilon = 1e-6
C_opt_inv = np.linalg.inv(C_opt + epsilon * np.eye(N))
w_opt = C_opt_inv @ delta_f

# Compute factorial weights w^{fac}
C_fac = np.diag(variances)
C_fac_inv = np.linalg.inv(C_fac)
w_fac = C_fac_inv @ delta_f

plt.figure()
plt.plot(phi_prefs, w_opt, label='Optimal Weights w^{opt}')
plt.plot(phi_prefs, w_fac, label='Factorial Weights w^{fac}', linestyle='--')
plt.xlabel('Preferred Orientation (rad)')
plt.ylabel('Read-out Weight')
plt.title('Read-out Weights vs Preferred Orientation')
plt.legend()
plt.show()

# (d) Simulate decision variables and compute d'
n_trials = 100

# Generate all correlated responses for all trials in one go (vectorized)
r1_corr_trials = np.array([generate_correlated_responses(f1, C_opt) for _ in range(n_trials)])
r2_corr_trials = np.array([generate_correlated_responses(f2, C_opt) for _ in range(n_trials)])

# Generate all independent responses for all trials in one go (vectorized)
r1_indep_trials = np.random.poisson(f1, (n_trials, len(f1)))
r2_indep_trials = np.random.poisson(f2, (n_trials, len(f2)))

# Compute decision variables for optimal and factorial weights (vectorized)
R1_opt = r1_corr_trials @ w_opt  # Dot product for all trials at once
R2_opt = r2_corr_trials @ w_opt
R1_fac = r1_corr_trials @ w_fac
R2_fac = r2_corr_trials @ w_fac

# Independent neurons for comparison (vectorized)
R1_indep = r1_indep_trials @ w_fac
R2_indep = r2_indep_trials @ w_fac

# Function to safely compute d_prime
def compute_d_prime(R1, R2, epsilon=1e-10):
    variance_sum = 0.5 * (np.var(R1) + np.var(R2))
    if variance_sum < epsilon:
        return np.nan  # Return NaN if variance is too small to avoid invalid d_prime calculation
    return (np.mean(R1) - np.mean(R2)) / np.sqrt(variance_sum)

# Compute d_prime using the new function
d_prime_opt = compute_d_prime(R1_opt, R2_opt)
d_prime_fac = compute_d_prime(R1_fac, R2_fac)
d_prime_indep = compute_d_prime(R1_indep, R2_indep)

# Plot histograms
plt.figure()
plt.hist(R1_opt, bins=30, alpha=0.5, label=f'phi1 = {phi1_deg}°')
plt.hist(R2_opt, bins=30, alpha=0.5, label=f'phi2 = {phi2_deg}°')
plt.xlabel('Decision Variable R')
plt.ylabel('Frequency')
plt.title(f'Decision Variable Distribution with w^opt, d\' = {d_prime_opt:.2f}')
plt.legend()
plt.show()

plt.figure()
plt.hist(R1_fac, bins=30, alpha=0.5, label=f'phi1 = {phi1_deg}°')
plt.hist(R2_fac, bins=30, alpha=0.5, label=f'phi2 = {phi2_deg}°')
plt.xlabel('Decision Variable R')
plt.ylabel('Frequency')
plt.title(f'Decision Variable Distribution with w^fac, d\' = {d_prime_fac:.2f}')
plt.legend()
plt.show()

print(f"d' from independent neurons with w^fac: {d_prime_indep:.2f}")
print(f"d' from correlated neurons with w^opt: {d_prime_opt:.2f}")
print(f"d' from correlated neurons with w^fac: {d_prime_fac:.2f}")


# (e) Plot d' vs N for different rho_max values
N_list = [2 ** i for i in range(1, 11)]  # N from 2 to 1024

for rho_max in rho_max_values:
    d_prime_N_opt = []
    d_prime_N_fac = []
    d_prime_N_indep = []
    for N in N_list:
        phi_prefs = np.linspace(0, np.pi, N, endpoint=False)
        f = get_population_response(c, 0, phi_prefs, kappa, f_max, f0)
        f1 = get_population_response(c, phi1, phi_prefs, kappa, f_max, f0)
        f2 = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)
        delta_f = f1 - f2
        variances = f
        
        # Correlation matrix and covariance matrix
        corr_matrix = compute_correlation_matrix(phi_prefs, rho_max, tau)
        C_opt = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                C_opt[i, j] = corr_matrix[i, j] * np.sqrt(variances[i] * variances[j])
        
        # Invert covariance matrices
        epsilon = 1e-6
        C_opt_inv = np.linalg.inv(C_opt + epsilon * np.eye(N))
        w_opt = C_opt_inv @ delta_f
        C_fac_inv = np.linalg.inv(np.diag(variances))
        w_fac = C_fac_inv @ delta_f
        
        # Simulate decision variables
        R1_opt = []
        R2_opt = []
        R1_fac = []
        R2_fac = []
        R1_indep = []
        R2_indep = []
        for _ in range(n_trials):
            # Correlated responses
            r1_corr = generate_correlated_responses(f1, C_opt)
            r2_corr = generate_correlated_responses(f2, C_opt)
            R1_opt.append(np.dot(w_opt, r1_corr))
            R2_opt.append(np.dot(w_opt, r2_corr))
            R1_fac.append(np.dot(w_fac, r1_corr))
            R2_fac.append(np.dot(w_fac, r2_corr))
            # Independent responses
            r1_indep = generate_independent_responses(f1)
            r2_indep = generate_independent_responses(f2)
            R1_indep.append(np.dot(w_fac, r1_indep))
            R2_indep.append(np.dot(w_fac, r2_indep))
        
        # Compute d' values
        R1_opt = np.array(R1_opt)
        R2_opt = np.array(R2_opt)
        d_prime_opt = compute_d_prime(R1_opt, R2_opt)
        d_prime_N_opt.append(d_prime_opt)
        
        R1_fac = np.array(R1_fac)
        R2_fac = np.array(R2_fac)
        d_prime_fac = compute_d_prime(R1_fac, R2_fac)
        d_prime_N_fac.append(d_prime_fac)
        
        R1_indep = np.array(R1_indep)
        R2_indep = np.array(R2_indep)
        d_prime_indep = compute_d_prime(R1_indep, R2_indep)
        d_prime_N_indep.append(d_prime_indep)
    
    # Plotting
    plt.figure()
    plt.plot(N_list, d_prime_N_opt, label='Optimal Decoder w^{opt}', marker='o')
    plt.plot(N_list, d_prime_N_fac, label='Factorial Decoder w^{fac}', marker='s')
    plt.plot(N_list, d_prime_N_indep, label='Independent Neurons', linestyle='--', marker='^')
    plt.xscale('log')
    plt.xlabel('Number of Neurons N')
    plt.ylabel('d\'')
    plt.title(f'd\' vs N (rho_max = {rho_max})')
    plt.legend()
    plt.show()
    
    # Determine N for 95% accuracy (d' = 3.3)
    N_needed_opt = next((N for N, d in zip(N_list, d_prime_N_opt) if d >= 3.3), None)
    N_needed_fac = next((N for N, d in zip(N_list, d_prime_N_fac) if d >= 3.3), None)
    print(f"For rho_max = {rho_max}:")
    print(f"  Optimal Decoder w^opt reaches 95% accuracy at N = {N_needed_opt}")
    print(f"  Factorial Decoder w^fac reaches 95% accuracy at N = {N_needed_fac}")
