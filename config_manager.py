import configparser
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProblemParameters:
    """Parameters for ski rental problem scenarios."""
    b1: int  # Cost of buying item 1
    b2: int  # Cost of buying item 2
    B: int   # Cost of buying bundle
    d1: int  # Demand duration for item 1
    d2: int  # Demand duration for item 2
    num_simulations: int  # Number of Monte Carlo simulations
    alpha_values: List[float] = field(default_factory=list)  # Alpha values for sweeps
    
    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        if self.b1 <= 0 or self.b2 <= 0 or self.B <= 0:
            raise ValueError("All cost parameters must be positive")
        if self.d1 < 0 or self.d2 < 0:
            raise ValueError("Demand durations must be non-negative")
        if self.num_simulations <= 0:
            raise ValueError("Number of simulations must be positive")

class ConfigManager:
    """Manages configuration loading and parameter validation."""
    
    def __init__(self, config_file: str = 'config.ini') -> None:
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
            
        Raises:
            FileNotFoundError: If config file doesn't exist
        """
        self.config_file = Path(config_file)
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
            
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file)
            logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to read config file {config_file}: {e}") from e

    def get_scenario_parameters(self, scenario_name: str) -> ProblemParameters:
        """
        Load parameters for a specific scenario from the config file.
        
        Args:
            scenario_name: Name of the scenario section in config file
            
        Returns:
            ProblemParameters object with scenario configuration
            
        Raises:
            ValueError: If scenario not found or parameters invalid
            RuntimeError: If configuration parsing fails
        """
        if not self.config.has_section(scenario_name):
            available_sections = list(self.config.sections())
            raise ValueError(
                f"Scenario '{scenario_name}' not found. Available sections: {available_sections}"
            )
        
        try:
            # Load required parameters with validation
            b1 = self._get_positive_int(scenario_name, 'b1', 'Cost b1')
            b2 = self._get_positive_int(scenario_name, 'b2', 'Cost b2')
            B = self._get_positive_int(scenario_name, 'B', 'Bundle cost B')
            d1 = self._get_non_negative_int(scenario_name, 'd1', 'Demand d1')
            d2 = self._get_non_negative_int(scenario_name, 'd2', 'Demand d2')
            
            # Load alpha values with error handling
            alpha_values = self._parse_alpha_values(scenario_name)
            
            # Load simulation count
            num_simulations = self._get_positive_int('General', 'num_simulations', 'Number of simulations')
            
            params = ProblemParameters(
                b1=b1, b2=b2, B=B, d1=d1, d2=d2,
                num_simulations=num_simulations, alpha_values=alpha_values
            )
            
            logger.debug(f"Loaded scenario '{scenario_name}': {params}")
            return params
            
        except Exception as e:
            raise RuntimeError(f"Failed to load scenario '{scenario_name}': {e}") from e
    
    def _get_positive_int(self, section: str, key: str, description: str) -> int:
        """Get positive integer from config with validation."""
        try:
            value = self.config.getint(section, key)
            if value <= 0:
                raise ValueError(f"{description} must be positive, got {value}")
            return value
        except (ValueError, configparser.NoOptionError) as e:
            raise ValueError(f"Invalid {description} in section '{section}': {e}") from e
    
    def _get_non_negative_int(self, section: str, key: str, description: str) -> int:
        """Get non-negative integer from config with validation."""
        try:
            value = self.config.getint(section, key)
            if value < 0:
                raise ValueError(f"{description} must be non-negative, got {value}")
            return value
        except (ValueError, configparser.NoOptionError) as e:
            raise ValueError(f"Invalid {description} in section '{section}': {e}") from e
    
    def _parse_alpha_values(self, scenario_name: str) -> List[float]:
        """Parse alpha values from config string."""
        alpha_str = self.config.get(scenario_name, 'alpha_values', fallback='')
        if not alpha_str.strip():
            return []
        
        try:
            alpha_values = [float(x.strip()) for x in alpha_str.split(',') if x.strip()]
            # Validate alpha values are positive
            for alpha in alpha_values:
                if alpha <= 0:
                    raise ValueError(f"Alpha value must be positive, got {alpha}")
            return alpha_values
        except ValueError as e:
            raise ValueError(f"Invalid alpha_values format in '{scenario_name}': {e}") from e