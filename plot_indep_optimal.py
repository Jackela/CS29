import matplotlib.pyplot as plt
import numpy as np

# Data from our alpha sweep for the "Independent Purchase Optimal" scenario
alpha_values_indep = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
simulated_costs_indep = [75.8303, 75.8243, 75.8125, 76.5271, 79.7111, 85.7091, 91.9442]
theoretical_optimal_indep = 60.0 # Optimal cost for this scenario (b1+b2 = 60)

plt.figure(figsize=(10, 6))
plt.plot(alpha_values_indep, simulated_costs_indep, marker='o', linestyle='-', color='purple', label='Simulated Average Cost')
plt.axhline(y=theoretical_optimal_indep, color='red', linestyle='--', label=f'Theoretical Optimal Cost ({theoretical_optimal_indep})')

plt.title('HybridRandomAlgorithm: Alpha vs. Average Cost (Independent Purchase Optimal Scenario)')
plt.xlabel(r'Alpha Value ($\alpha$)') # Corrected LaTeX expression
plt.ylabel('Simulated Average Cost')
plt.xticks(alpha_values_indep)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('alpha_sweep_indep_optimal.png') # Save as PNG file
# plt.show() # Uncomment to display the plot locally
