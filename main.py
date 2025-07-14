import argparse
from config_manager import ConfigManager
from experiments import run_alpha_sweep_experiment, run_adaptive_hybrid_experiment

def main():
    """
    Main entry point for running ski rental problem experiments.
    """
    parser = argparse.ArgumentParser(description="Run ski rental problem experiments.")
    parser.add_argument(
        '--experiment',
        type=str,
        required=True,
        choices=['AdversarialScenario', 'IndependentPurchaseScenario', 'AdaptiveHybridExperiment'],
        help='The name of the experiment scenario to run.'
    )
    parser.add_argument(
        '--scenario',
        type=str,
        help='The specific scenario (e.g., AdversarialScenario, IndependentPurchaseScenario) for AdaptiveHybridExperiment.'
    )
    args = parser.parse_args()

    config_manager = ConfigManager()

    if args.experiment == 'AdaptiveHybridExperiment':
        if not args.scenario:
            print("Error: --scenario is required for AdaptiveHybridExperiment.")
            return
        params = config_manager.get_scenario_parameters(args.scenario)
        run_adaptive_hybrid_experiment(params, args.scenario)
    elif args.experiment in ['AdversarialScenario', 'IndependentPurchaseScenario']:
        params = config_manager.get_scenario_parameters(args.experiment)
        run_alpha_sweep_experiment(params, args.experiment)
    else:
        print(f"Unknown experiment: {args.experiment}")

if __name__ == "__main__":
    main()