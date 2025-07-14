import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm 

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 

# Data for competitive ratios across scenarios (using our latest verified CRs)
scenarios = ["组合购买更优", "独立购买更优", "纯租赁更优", "混合场景"]
competitive_ratios = [1.2304, 1.2399, 1.0000, 1.0000] # Using my latest verified CRs

plt.figure(figsize=(10, 6))
bars = plt.bar(scenarios, competitive_ratios, color=['skyblue', 'lightcoral', 'lightgreen', 'lightgray'])
plt.axhline(y=1.0, color='red', linestyle='--', label='Ideal CR (1.0)')

plt.title('HybridRandomAlgorithm Competitive Ratio Across Different Scenarios')
plt.xlabel('Scenario')
plt.ylabel('Competitive Ratio (CR)')
plt.ylim(0.9, 1.4) # Adjust y-axis limit for better visualization if needed
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()

# Add CR values on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 4), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('adaptive_hybrid_cr_summary.png') # Save as PNG file
# plt.show() # Uncomment to display the plot locally