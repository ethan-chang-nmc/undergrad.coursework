import numpy as np
import matplotlib.pyplot as plt

# Constants and parameters
N = 100  # Number of neurons
kappa = 1  # Tuning curve width
f_max = 20  # Maximum firing rate (spikes/s)
f0 = 5  # Baseline firing rate (spikes/s)
c = 0.1  # Contrast for the task
phi1 = 0  # Horizontal orientation in radians
phi2 = np.pi / 2  # Vertical orientation in radians
B = np.inf  # Decision bound for Part (a)

# Define preferred orientations of neurons, equally spaced in [0, π)
phi_prefs = np.linspace(0, np.pi, N, endpoint=False)

# Function to compute population response for given orientation and contrast
def get_population_response(c, phi, phi_prefs, kappa, f_max, f0):
    """Calculate mean firing rates based on contrast, stimulus orientation, and neuron preferences."""
    delta_phi = phi - phi_prefs
    f = f0 + c * (f_max - f0) * np.exp(kappa * (np.cos(2 * delta_phi) - 1))
    return f

# Generate mean responses for phi1 (horizontal) and phi2 (vertical)
f1 = get_population_response(c, phi1, phi_prefs, kappa, f_max, f0)
f2 = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)

# Compute the decision variable d (using w = w_fac, as per the instructions)
delta_f = f1 - f2  # Difference in mean response
variances = f1  # Variances for Poisson neurons are equal to the mean rate

# Compute the read-out weights (factorial weights assuming independent neurons)
w_fac = delta_f / variances

# Display the weights as per Part (b) requirements for vertical vs horizontal discrimination task
plt.figure()
plt.plot(phi_prefs, w_fac, label='Factorial Weights (w_fac)')
plt.xlabel('Preferred Orientation (rad)')
plt.ylabel('Read-out Weight')
plt.title('Read-out Weights for Vertical vs Horizontal Discrimination Task')
plt.legend()
plt.show()

# Part (c): Simulate and plot d as a function of time for 10 example trials with vertical stimulus orientation

# Simulation parameters
T = 100  # Total time steps (for a total duration of 1s with 10 ms bins)
time_bins = np.arange(1, T + 1) * 0.01  # Time in seconds
c = 0.0001  # Very difficult task contrast level
B = np.inf  # No bound; we'll let the integration run fully

# Generate mean response for vertical orientation
f_vertical = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)

# Function to simulate the decision variable d over time
def simulate_decision_variable(T, w, f_mean):
    """Simulate the accumulation of the decision variable over T time steps."""
    d_values = np.zeros(T)
    for t in range(T):
        r = np.random.poisson(f_mean)  # Generate Poisson spike counts
        e_t = np.dot(w, r)  # Decision increment at time step t
        d_values[t] = e_t if t == 0 else d_values[t-1] + e_t  # Cumulative sum over time
    return d_values

# Simulate and plot d(t) for 10 example trials
plt.figure(figsize=(10, 6))
for trial in range(10):
    d_values = simulate_decision_variable(T, w_fac, f_vertical)
    plt.plot(time_bins, d_values, label=f'Trial {trial + 1}' if trial < 2 else "")  # Label only first two trials
plt.xlabel('Time (s)')
plt.ylabel('Decision Variable d')
plt.title('Decision Variable d over Time for 10 Trials (Vertical Stimulus, c = 0.0001)')
plt.legend()
plt.show()

# Part (d): Find critical contrast c* and plot d as a function of time

# Parameters for finding critical contrast
n_trials = 100  # Number of trials for each contrast level
target_accuracy = 0.67  # Target accuracy (67% correct)

# Function to check if d reaches the bound B within T time steps
def is_trial_correct(d_values, B):
    return np.any(np.abs(d_values) >= B)

# Function to estimate the critical contrast c* for 67% correct trials
def find_critical_contrast(c_initial, c_step, B, target_accuracy, n_trials):
    c_current = c_initial
    while True:
        correct_trials = 0
        for _ in range(n_trials):
            f_vertical = get_population_response(c_current, phi2, phi_prefs, kappa, f_max, f0)
            d_values = simulate_decision_variable(T, w_fac, f_vertical)
            if is_trial_correct(d_values, B):
                correct_trials += 1
        accuracy = correct_trials / n_trials
        if np.abs(accuracy - target_accuracy) < 0.01:
            return c_current
        c_current += c_step

# Find the critical contrast level c*
c_star = find_critical_contrast(c_initial=0.0001, c_step=0.0001, B=B, target_accuracy=target_accuracy, n_trials=n_trials)
print(f"Critical contrast level c* for 67% correct trials: {c_star}")

# Plot d over time for multiple runs at the critical contrast level c*
plt.figure(figsize=(10, 6))
for trial in range(10):
    f_vertical = get_population_response(c_star, phi2, phi_prefs, kappa, f_max, f0)
    d_values = simulate_decision_variable(T, w_fac, f_vertical)
    plt.plot(time_bins, d_values, label=f'Trial {trial + 1}' if trial < 2 else "")  # Label only first two trials
plt.xlabel('Time (s)')
plt.ylabel('Decision Variable d')
plt.title(f'Decision Variable d over Time at Critical Contrast c* = {c_star:.4f}')
plt.legend()
plt.show()

# Part (e): Plot the psychometric function as a function of contrast

# Parameters for psychometric function
contrast_levels = np.linspace(0, 3 * c_star, 20)  # 20 contrast levels between 0 and 3 * c_star
n_trials = 100  # Number of trials per contrast level

# Initialize lists to store results
percent_correct = []
error_bars = []

# Loop over contrast levels to calculate percent correct and standard error
for c in contrast_levels:
    correct_trials = 0
    for _ in range(n_trials):
        f_vertical = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)
        d_values = simulate_decision_variable(T, w_fac, f_vertical)
        if is_trial_correct(d_values, B):
            correct_trials += 1
    accuracy = correct_trials / n_trials
    percent_correct.append(accuracy)
    # Calculate the standard error for binomial distribution
    standard_error = np.sqrt(accuracy * (1 - accuracy) / n_trials)
    error_bars.append(standard_error)

# Convert lists to numpy arrays for easier plotting
percent_correct = np.array(percent_correct)
error_bars = np.array(error_bars)

# Plot the psychometric function with error bars
plt.figure(figsize=(10, 6))
plt.errorbar(contrast_levels, percent_correct, yerr=error_bars, fmt='o', capsize=5, label='Percent Correct')
plt.xlabel('Contrast Level')
plt.ylabel('Percent Correct')
plt.title('Psychometric Function (Percent Correct vs. Contrast)')
plt.legend()
plt.show()
# Part (f): Determine B* for about 75% of trials to reach a decision within T and plot reaction time distributions

# Parameters for reaction time simulation
target_accuracy = 0.75  # Target accuracy (75% correct)
n_trials = 100  # Number of trials for estimation
c_star = find_critical_contrast(0.0001, 0.0001, B, 0.67, n_trials)  # Ensure we're using c* from Part (d)

# Function to estimate B* for a target proportion of correct decisions within T
def find_decision_bound(c_star, target_accuracy, n_trials):
    B_current = 0.5  # Initial bound to test
    B_step = 0.1  # Step to adjust the bound
    while True:
        correct_within_T = 0
        for _ in range(n_trials):
            f_vertical = get_population_response(c_star, phi2, phi_prefs, kappa, f_max, f0)
            d_values = simulate_decision_variable(T, w_fac, f_vertical)
            if is_trial_correct(d_values, B_current) and np.max(np.abs(d_values)) < B_current:
                correct_within_T += 1
        accuracy = correct_within_T / n_trials
        if np.abs(accuracy - target_accuracy) < 0.01:
            return B_current
        B_current += B_step

# Find B* for about 75% accuracy
B_star = find_decision_bound(c_star, target_accuracy, n_trials)
print(f"Bound B* for 75% accuracy within time limit: {B_star}")

# Simulate reaction time distributions with B*
reaction_times_correct = []
reaction_times_incorrect = []

for _ in range(n_trials):
    f_vertical = get_population_response(c_star, phi2, phi_prefs, kappa, f_max, f0)
    d_values = simulate_decision_variable(T, w_fac, f_vertical)
    reaction_time = np.where(np.abs(d_values) >= B_star)[0]
    if reaction_time.size > 0:  # Decision reached
        reaction_time = reaction_time[0] * 0.01  # Convert to seconds (10ms bins)
        if is_trial_correct(d_values, B_star):
            reaction_times_correct.append(reaction_time)
        else:
            reaction_times_incorrect.append(reaction_time)

# Plot reaction time distributions for correct and incorrect trials
plt.figure(figsize=(10, 6))
plt.hist(reaction_times_correct, bins=20, alpha=0.5, label='Correct Trials', color='blue')
plt.hist(reaction_times_incorrect, bins=20, alpha=0.5, label='Incorrect Trials', color='red')
plt.xlabel('Reaction Time (s)')
plt.ylabel('Frequency')
plt.title(f'Reaction Time Distribution at Critical Contrast c* = {c_star:.4f} with Bound B* = {B_star}')
plt.legend()
plt.show()

# Part (g): Plot the psychometric function with the finite bound B* and compare to Part (e)

# Initialize lists to store results for the finite bound B*
percent_correct_B_star = []
error_bars_B_star = []

# Loop over contrast levels to calculate percent correct and standard error with bound B*
for c in contrast_levels:
    correct_trials = 0
    for _ in range(n_trials):
        f_vertical = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)
        d_values = simulate_decision_variable(T, w_fac, f_vertical)
        # Check if decision reached within bound B*
        if is_trial_correct(d_values, B_star):
            correct_trials += 1
    accuracy = correct_trials / n_trials
    percent_correct_B_star.append(accuracy)
    # Calculate the standard error for binomial distribution
    standard_error = np.sqrt(accuracy * (1 - accuracy) / n_trials)
    error_bars_B_star.append(standard_error)

# Convert lists to numpy arrays for easier plotting
percent_correct_B_star = np.array(percent_correct_B_star)
error_bars_B_star = np.array(error_bars_B_star)

# Plot the psychometric function for the finite bound B*
plt.figure(figsize=(10, 6))
plt.errorbar(contrast_levels, percent_correct, yerr=error_bars, fmt='o', capsize=5, label='Infinite Bound (Part e)')
plt.errorbar(contrast_levels, percent_correct_B_star, yerr=error_bars_B_star, fmt='o', capsize=5, color='orange', label=f'Finite Bound B* = {B_star}')
plt.xlabel('Contrast Level')
plt.ylabel('Percent Correct')
plt.title('Psychometric Function Comparison: Infinite Bound vs. Finite Bound B*')
plt.legend()
plt.show()

# Part (h): Compute and plot the psychometric function with trial durations up to 5 seconds

# Update the simulation time limit
T_extended = 500  # Total time steps for 5 seconds (with 10 ms bins)
time_bins_extended = np.arange(1, T_extended + 1) * 0.01  # Time in seconds

# Initialize lists to store results for extended time duration
percent_correct_extended = []
error_bars_extended = []

# Loop over contrast levels to calculate percent correct and standard error with extended time limit
for c in contrast_levels:
    correct_trials = 0
    for _ in range(n_trials):
        f_vertical = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)
        d_values = simulate_decision_variable(T_extended, w_fac, f_vertical)
        # Check if decision reached within bound B*
        if is_trial_correct(d_values, B_star):
            correct_trials += 1
    accuracy = correct_trials / n_trials
    percent_correct_extended.append(accuracy)
    # Calculate the standard error for binomial distribution
    standard_error = np.sqrt(accuracy * (1 - accuracy) / n_trials)
    error_bars_extended.append(standard_error)

# Convert lists to numpy arrays for easier plotting
percent_correct_extended = np.array(percent_correct_extended)
error_bars_extended = np.array(error_bars_extended)

# Plot the psychometric function for the extended time limit
plt.figure(figsize=(10, 6))
plt.errorbar(contrast_levels, percent_correct_B_star, yerr=error_bars_B_star, fmt='o', capsize=5, label=f'Finite Bound B* with T = 1s')
plt.errorbar(contrast_levels, percent_correct_extended, yerr=error_bars_extended, fmt='o', capsize=5, color='green', label='Extended Duration (T = 5s)')
plt.xlabel('Contrast Level')
plt.ylabel('Percent Correct')
plt.title('Psychometric Function with Extended Trial Duration (up to 5 seconds)')
plt.legend()
plt.show()

# Part (i): Plot the median reaction time as a function of contrast with extended duration

# Initialize list to store median reaction times
median_reaction_times = []

# Loop over contrast levels to calculate the median reaction time for each
for c in contrast_levels:
    reaction_times = []
    for _ in range(n_trials):
        f_vertical = get_population_response(c, phi2, phi_prefs, kappa, f_max, f0)
        d_values = simulate_decision_variable(T_extended, w_fac, f_vertical)
        reaction_time = np.where(np.abs(d_values) >= B_star)[0]
        if reaction_time.size > 0:  # Decision reached within the extended time
            reaction_times.append(reaction_time[0] * 0.01)  # Convert to seconds (10ms bins)

    # Calculate median reaction time for the current contrast level
    if reaction_times:  # Ensure there's at least one decision within time
        median_reaction_times.append(np.median(reaction_times))
    else:
        median_reaction_times.append(np.nan)  # No decision reached for this contrast level

# Convert contrast levels to a numpy array for plotting
contrast_levels = np.array(contrast_levels)

# Plot the median reaction time as a function of contrast
plt.figure(figsize=(10, 6))
plt.plot(contrast_levels, median_reaction_times, marker='o', color='purple', label='Median Reaction Time')
plt.xlabel('Contrast Level')
plt.ylabel('Median Reaction Time (s)')
plt.title('Median Reaction Time as a Function of Contrast Level')
plt.legend()
plt.show()
