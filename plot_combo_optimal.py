import matplotlib.pyplot as plt
import numpy as np

# Data from our extended alpha sweep for the "Combinational Purchase Optimal" scenario
alpha_values_combo = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 10.0, 20.0]
simulated_costs_combo = [38.7875, 17.3999, 16.3355, 15.5974, 15.0343, 14.6200, 13.5458, 12.4535, 11.7915]
theoretical_optimal_combo = 11.0 # Optimal cost for this scenario (B=11)

plt.figure(figsize=(10, 6))
plt.plot(alpha_values_combo, simulated_costs_combo, marker='o', linestyle='-', color='blue', label='Simulated Average Cost')
plt.axhline(y=theoretical_optimal_combo, color='red', linestyle='--', label=f'Theoretical Optimal Cost ({theoretical_optimal_combo})')

plt.title('HybridRandomAlgorithm: Alpha vs. Average Cost (Combinational Purchase Optimal Scenario)')
plt.xlabel(r'Alpha Value ($\alpha$)') # Corrected LaTeX expression
plt.ylabel('Simulated Average Cost')
plt.xticks(alpha_values_combo)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('alpha_sweep_combo_optimal.png') # Save as PNG file
# plt.show() # Uncomment to display the plot locally