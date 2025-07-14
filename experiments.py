import math
from config_manager import ProblemParameters
from ski_rental_algorithms import HybridRandomAlgorithm, AdaptiveHybridRandomAlgorithm, OptimalOfflineAlgorithm

def monte_carlo_simulation(algorithm_class, params: ProblemParameters, num_simulations: int, **kwargs):
    """
    Performs Monte Carlo simulation to estimate the expected cost of a given algorithm.

    @param {class} algorithm_class - The algorithm class to simulate (e.g., HybridRandomAlgorithm).
    @param {ProblemParameters} params - The configuration parameters for the problem.
    @param {int} num_simulations - The number of simulation runs.
    @param {**kwargs} kwargs - Additional keyword arguments to pass to the algorithm's constructor.
    @returns {float} The average cost over all simulations.
    @precondition num_simulations > 0
    @postcondition retval >= 0
    """
    assert num_simulations > 0, "num_simulations must be positive"
    total_simulated_cost = 0.0
    for _ in range(num_simulations):
        alg_instance = algorithm_class(
            b1=params.b1, b2=params.b2, B=params.B, d1=params.d1, d2=params.d2, **kwargs
        )
        total_simulated_cost += alg_instance.run()
    cost = total_simulated_cost / num_simulations
    assert cost >= 0, "Postcondition failed: simulated cost must be non-negative"
    return cost

def run_alpha_sweep_experiment(params: ProblemParameters, scenario_name: str):
    """
    Runs an alpha sweep experiment for a given scenario using the non-adaptive HybridRandomAlgorithm.

    @param {ProblemParameters} params - The configuration parameters for the problem.
    @param {str} scenario_name - A descriptive name for the scenario (e.g., 'Adversarial').
    @precondition params.alpha_values is not None and len(params.alpha_values) > 0
    @postcondition A log file named log_{scenario_name}_alpha_sweep.md is created/updated.
    """
    assert params.alpha_values is not None and len(params.alpha_values) > 0, "alpha_values must be provided for alpha sweep"

    log_file = f"log_{scenario_name}_alpha_sweep.md"
    results = []

    print(f"--- Running Alpha Sweep for {scenario_name} Scenario (Non-Adaptive HybridRandomAlgorithm) ---")
    for alpha in params.alpha_values:
        print(f"  Testing alpha = {alpha}...")
        avg_cost = monte_carlo_simulation(
            HybridRandomAlgorithm, params, params.num_simulations, alpha=alpha
        )
        results.append((alpha, avg_cost))
    
    log_content = f"# Alpha Sweep Results: {scenario_name} Scenario (Non-Adaptive HybridRandomAlgorithm)\n\n"
    log_content += f"**Parameters:**\n"
    log_content += f"- `b1`: {params.b1}, `b2`: {params.b2}, `B`: {params.B}\n"
    log_content += f"- `d1`: {params.d1}, `d2`: {params.d2}\n"
    log_content += f"- `num_simulations`: {params.num_simulations}\n\n"
    log_content += "| Alpha Value | Simulated Average Cost |\n"
    log_content += "|-------------|------------------------|\n"
    for alpha, avg_cost in results:
        log_content += f"| {alpha:<11.1f} | {avg_cost:<22.4f} |\n"

    print(f"\n--- Experiment Results for {scenario_name} (Non-Adaptive) ---")
    print(log_content)

    with open(log_file, 'w') as f:
        f.write(log_content)
    print(f"\nResults saved to {log_file}")

def run_adaptive_hybrid_experiment(params: ProblemParameters, scenario_name: str):
    """
    Runs a simulation for the AdaptiveHybridRandomAlgorithm in a given scenario.

    @param {ProblemParameters} params - The configuration parameters for the problem.
    @param {str} scenario_name - A descriptive name for the scenario (e.g., 'Adversarial').
    @postcondition A log file named log_AdaptiveHybrid_{scenario_name}.md is created/updated.
    """
    log_file = f"log_AdaptiveHybrid_{scenario_name}.md"

    print(f"--- Running Adaptive HybridRandomAlgorithm for {scenario_name} Scenario ---")
    
    # Calculate theoretical optimal cost for this specific scenario
    optimal_alg = OptimalOfflineAlgorithm(params.b1, params.b2, params.B, params.d1, params.d2)
    c_opt = optimal_alg.run()
    print(f"Theoretical Optimal Offline Cost: {c_opt}\n")

    avg_cost = monte_carlo_simulation(
        AdaptiveHybridRandomAlgorithm, params, params.num_simulations
    )

    log_content = f"# Adaptive HybridRandomAlgorithm Results: {scenario_name} Scenario\n\n"
    log_content += f"**Parameters:**\n"
    log_content += f"- `b1`: {params.b1}, `b2`: {params.b2}, `B`: {params.B}\n"
    log_content += f"- `d1`: {params.d1}, `d2`: {params.d2}\n"
    log_content += f"- `num_simulations`: {params.num_simulations}\n\n"
    log_content += f"Theoretical Optimal Offline Cost: {c_opt}\n"
    log_content += f"Simulated Average Cost (Adaptive HybridRandomAlgorithm): {avg_cost:.4f}\n"
    log_content += f"Competitive Ratio (CR): {avg_cost / c_opt:.4f}\n"

    print(f"\n--- Experiment Results for Adaptive HybridRandomAlgorithm ({scenario_name}) ---")
    print(log_content)

    with open(log_file, 'w') as f:
        f.write(log_content)
    print(f"\nResults saved to {log_file}")