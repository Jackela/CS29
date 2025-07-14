from config_manager import ConfigManager, ProblemParameters
from ski_rental_algorithms import OptimalOfflineAlgorithm, PurelyLocalAlgorithm

def find_worst_case_scenario(
    b1: int, b2: int, B: int, max_d1: int, max_d2: int
) -> dict:
    """
    Finds the demand pair (d1, d2) that maximizes the competitive ratio for PurelyLocalAlgorithm.

    It iterates through all possible demand durations up to max_d1 and max_d2,
    calculates the online and optimal costs, and finds the highest competitive ratio.

    Args:
        b1: The cost of buying item 1.
        b2: The cost of buying item 2.
        B: The cost of buying the bundle.
        max_d1: The maximum demand duration to check for item 1.
        max_d2: The maximum demand duration to check for item 2.
    Returns:
        A dictionary containing the worst-case scenario details.
    """
    max_cr = 0.0
    worst_d1 = -1
    worst_d2 = -1
    c_opt_at_worst = -1
    c_online_at_worst = -1

    for d1 in range(max_d1 + 1):
        for d2 in range(max_d2 + 1):
            # Instantiate algorithms for current d1, d2
            optimal_alg = OptimalOfflineAlgorithm(b1, b2, B, d1, d2)
            purely_local_alg = PurelyLocalAlgorithm(b1, b2, B, d1, d2)

            c_opt = optimal_alg.run()
            c_online = purely_local_alg.run()
            
            if c_opt == 0:
                continue
                
            cr = c_online / c_opt
            
            if cr > max_cr:
                max_cr = cr
                worst_d1 = d1
                worst_d2 = d2
                c_opt_at_worst = c_opt
                c_online_at_worst = c_online

    return {
        "max_cr": max_cr,
        "worst_d1": worst_d1,
        "worst_d2": worst_d2,
        "c_opt_at_worst": c_opt_at_worst,
        "c_online_at_worst": c_online_at_worst,
    }

def print_worst_case_results(params: ProblemParameters, results: dict):
    """
    Prints the worst-case scenario analysis results.
    """
    print("--- Two-Level Ski Rental Problem Analysis ---")
    print(f"Fixed Costs: b1={params.b1}, b2={params.b2}, B={params.B}")
    print(f"Search Range: d1 in [0, {params.max_d1}], d2 in [0, {params.max_d2}]")
    print("\n--- Results ---")
    if results["worst_d1"] != -1:
        print(f"Worst-case scenario found:")
        print(f"  Demand (d1, d2)     = ({results["worst_d1"]}, {results["worst_d2"]})")
        print(f"  Online Algorithm Cost (C_online) = {results["c_online_at_worst"]}")
        print(f"  Optimal Offline Cost (C_opt)   = {results["c_opt_at_worst"]}")
        print(f"  Highest Competitive Ratio (CR)   = {results["max_cr"]:.4f}")
    else:
        print("No valid worst-case scenario found within the specified range.")

if __name__ == "__main__":
    config_manager = ConfigManager()
    params = config_manager.get_problem_parameters()

    worst_case_results = find_worst_case_scenario(
        params.b1, params.b2, params.B, params.max_d1, params.max_d2
    )
    print_worst_case_results(params, worst_case_results)
