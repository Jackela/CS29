import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from config_manager import ConfigManager
from experiments import run_alpha_sweep_experiment, run_adaptive_hybrid_experiment

# Configure logging for better debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ski_rental_experiments.log')
    ]
)
logger = logging.getLogger(__name__)

def main() -> None:
    """
    Main entry point for running ski rental problem experiments.
    
    Provides a command-line interface for executing different experimental scenarios
    with comprehensive error handling and logging.
    
    Raises:
        SystemExit: On argument parsing errors or critical failures
    """
    parser = argparse.ArgumentParser(
        description="Run ski rental problem experiments with comprehensive scenario support.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s --experiment AdversarialScenario
  %(prog)s --experiment AdaptiveHybridExperiment --scenario IndependentPurchaseScenario
  %(prog)s --experiment AdversarialScenario --config custom_config.ini
        """
    )
    
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
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.ini',
        help='Configuration file path (default: config.ini)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging output'
    )
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        logger.error(f"Argument parsing failed: {e}")
        raise

    # Configure logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    logger.info(f"Starting ski rental experiment: {args.experiment}")
    logger.info(f"Configuration file: {args.config}")
    
    try:
        # Validate configuration file exists
        config_path = Path(args.config)
        if not config_path.exists():
            logger.error(f"Configuration file not found: {args.config}")
            sys.exit(1)
            
        # Initialize configuration manager with error handling
        config_manager = ConfigManager(args.config)
        logger.info("Configuration loaded successfully")
        
        # Execute experiment based on type
        if args.experiment == 'AdaptiveHybridExperiment':
            if not args.scenario:
                logger.error("--scenario is required for AdaptiveHybridExperiment")
                parser.print_help()
                sys.exit(1)
                
            logger.info(f"Running adaptive hybrid experiment with scenario: {args.scenario}")
            params = config_manager.get_scenario_parameters(args.scenario)
            run_adaptive_hybrid_experiment(params, args.scenario)
            
        elif args.experiment in ['AdversarialScenario', 'IndependentPurchaseScenario']:
            logger.info(f"Running alpha sweep experiment: {args.experiment}")
            params = config_manager.get_scenario_parameters(args.experiment)
            run_alpha_sweep_experiment(params, args.experiment)
            
        else:
            logger.error(f"Unknown experiment type: {args.experiment}")
            sys.exit(1)
            
        logger.info("Experiment completed successfully")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
        
    except RuntimeError as e:
        logger.error(f"Runtime error during experiment: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.warning("Experiment interrupted by user")
        sys.exit(130)  # Standard exit code for SIGINT
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()