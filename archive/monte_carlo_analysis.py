import math
import random
from config_manager import ConfigManager, ProblemParameters
from ski_rental_algorithms import CorrelatedRandomAlgorithm, HybridRandomAlgorithm

# --- Monte Carlo Simulation Main Program ---

def monte_carlo_simulation(algorithm_class, params: ProblemParameters, num_simulations: int, **kwargs):
    """
    Performs Monte Carlo simulation to estimate the expected cost of a given algorithm.
    """
    total_simulated_cost = 0.0

    for _ in range(num_simulations):
        # Pass all relevant parameters to the algorithm constructor
        alg_instance = algorithm_class(
            b1=params.b1, b2=params.b2, B=params.B, d1=params.d1, d2=params.d2, **kwargs
        )
        single_run_cost = alg_instance.run()
        total_simulated_cost += single_run_cost
        
    return total_simulated_cost / num_simulations

def run_alpha_exploration_experiment(params: ProblemParameters, log_file="alpha_exploration_log.md"):
    """
    Runs an experiment to explore the effect of different alpha values on HybridRandomAlgorithm's cost.
    Prints the results to the console and saves them to a log file.
    """
    results = []

    print("--- Running Alpha Exploration Experiment for HybridRandomAlgorithm ---")
    for alpha in params.alpha_values:
        print(f"  Testing alpha = {alpha}...")
        avg_cost = monte_carlo_simulation(
            HybridRandomAlgorithm, params, params.num_simulations, alpha=alpha
        )
        results.append((alpha, avg_cost))
    
    # Prepare log content
    log_content = "# Alpha Exploration Results for HybridRandomAlgorithm\n\n"
    log_content += f"**Parameters:**\n"
    log_content += f"- `b1`: {params.b1}\n"
    log_content += f"- `b2`: {params.b2}\n"
    log_content += f"- `B`: {params.B}\n"
    log_content += f"- `d1`: {params.d1}\n"
    log_content += f"- `d2`: {params.d2}\n"
    log_content += f"- `num_simulations`: {params.num_simulations}\n\n"
    log_content += "| Alpha Value | Simulated Average Cost |\n"
    log_content += "|-------------|------------------------|\n"
    for alpha, avg_cost in results:
        log_content += f"| {alpha:<11} | {avg_cost:<22.4f} |\n"

    # Print to console
    print("\n--- Experiment Results ---")
    print(log_content)

    # Save to log file
    with open(log_file, 'w') as f:
        f.write(log_content)
    print(f"\nResults saved to {log_file}")

# --- Main Execution ---

if __name__ == "__main__":
    config_manager = ConfigManager()
    params = config_manager.get_problem_parameters()

    # Run the alpha exploration experiment
    run_alpha_exploration_experiment(params)