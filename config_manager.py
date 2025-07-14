import configparser
from dataclasses import dataclass, field
from typing import List

@dataclass
class ProblemParameters:
    b1: int
    b2: int
    B: int
    d1: int
    d2: int
    num_simulations: int
    alpha_values: List[float] = field(default_factory=list)

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_scenario_parameters(self, scenario_name: str) -> ProblemParameters:
        """
        Loads parameters for a specific scenario from the config file.

        @param {str} scenario_name - The name of the scenario section in config.ini.
        @returns {ProblemParameters} A dataclass object with the scenario parameters.
        @precondition The specified scenario_name exists in the config file.
        """
        assert self.config.has_section(scenario_name), f"Scenario '{scenario_name}' not found in config file."

        b1 = self.config.getint(scenario_name, 'b1')
        b2 = self.config.getint(scenario_name, 'b2')
        B = self.config.getint(scenario_name, 'B')
        d1 = self.config.getint(scenario_name, 'd1')
        d2 = self.config.getint(scenario_name, 'd2')
        
        # Safely get alpha_values, providing an empty list if not found
        alpha_values_str = self.config.get(scenario_name, 'alpha_values', fallback='')
        alpha_values = [float(x.strip()) for x in alpha_values_str.split(',')] if alpha_values_str else []
        
        num_simulations = self.config.getint('General', 'num_simulations')

        return ProblemParameters(
            b1=b1, b2=b2, B=B, d1=d1, d2=d2, 
            num_simulations=num_simulations, alpha_values=alpha_values
        )