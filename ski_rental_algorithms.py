import math
import random
from abc import ABC, abstractmethod
from typing import Optional, Union
import logging

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkiRentalAlgorithm(ABC):
    """
    Abstract base class for ski rental algorithms.
    """
    def __init__(self, b1: int, b2: int, B: int, d1: int, d2: int) -> None:
        """
        Initialize ski rental algorithm with cost and demand parameters.
        
        Args:
            b1: The cost of buying item 1 (must be positive)
            b2: The cost of buying item 2 (must be positive)
            B: The cost of buying the bundle (must be positive)
            d1: The total demand duration for item 1 (non-negative)
            d2: The total demand duration for item 2 (non-negative)
            
        Raises:
            AssertionError: If any cost parameter is non-positive or demand is negative
        """
        # Enhanced parameter validation with detailed error messages
        if not isinstance(b1, (int, float)) or b1 <= 0:
            raise ValueError(f"b1 must be a positive number, got {b1}")
        if not isinstance(b2, (int, float)) or b2 <= 0:
            raise ValueError(f"b2 must be a positive number, got {b2}")
        if not isinstance(B, (int, float)) or B <= 0:
            raise ValueError(f"B must be a positive number, got {B}")
        if not isinstance(d1, (int, float)) or d1 < 0:
            raise ValueError(f"d1 must be non-negative, got {d1}")
        if not isinstance(d2, (int, float)) or d2 < 0:
            raise ValueError(f"d2 must be non-negative, got {d2}")

        # Store parameters with type conversion for safety
        self.b1 = float(b1)
        self.b2 = float(b2)
        self.B = float(B)
        self.d1 = float(d1)
        self.d2 = float(d2)
        
        logger.debug(f"Initialized algorithm with b1={self.b1}, b2={self.b2}, B={self.B}, d1={self.d1}, d2={self.d2}")

    @abstractmethod
    def run(self) -> float:
        """
        Execute the algorithm and return the calculated cost.
        
        Returns:
            The total cost incurred by the algorithm (guaranteed non-negative)
            
        Raises:
            RuntimeError: If algorithm execution fails
        """
        pass

class OptimalOfflineAlgorithm(SkiRentalAlgorithm):
    """
    Calculates the optimal offline cost for the two-item ski rental problem.
    
    This algorithm has complete knowledge of demand durations and chooses
    the strategy that minimizes total cost.
    """
    def run(self) -> float:
        """
        Calculate the optimal offline cost by evaluating all strategies.
        
        Returns:
            The minimum cost among all possible strategies
        """
        try:
            # Calculate all possible strategy costs
            strategies = {
                'rent_all': self.d1 + self.d2,
                'buy1_rent2': self.b1 + self.d2,
                'rent1_buy2': self.d1 + self.b2,
                'buy_both_separately': self.b1 + self.b2,
                'buy_bundle': self.B
            }
            
            optimal_cost = min(strategies.values())
            optimal_strategy = min(strategies.keys(), key=lambda k: strategies[k])
            
            logger.debug(f"Strategy costs: {strategies}")
            logger.debug(f"Optimal strategy: {optimal_strategy} with cost {optimal_cost}")
            
            if optimal_cost < 0:
                raise RuntimeError(f"Invalid negative cost calculated: {optimal_cost}")
                
            return optimal_cost
            
        except Exception as e:
            logger.error(f"Error in OptimalOfflineAlgorithm.run(): {e}")
            raise RuntimeError(f"Failed to calculate optimal cost: {e}") from e

class PurelyLocalAlgorithm(SkiRentalAlgorithm):
    """
    Implements a purely local online algorithm.
    """
    def run(self) -> float:
        """
        @see SkiRentalAlgorithm.run
        """
        cost1 = min(self.d1, self.b1)
        cost2 = min(self.d2, self.b2)
        cost = cost1 + cost2
        assert cost >= 0, "Postcondition failed: cost must be non-negative"
        return float(cost)

class CorrelatedRandomAlgorithm(SkiRentalAlgorithm):
    """
    Implements the Correlated Random Algorithm for the ski rental problem.
    """
    def __init__(self, b1: int, b2: int, B: int, d1: int, d2: int, x_value: float = None):
        """
        @param {float} x_value - Optional fixed random value for testing (0 to 1).
        @precondition x_value is None or 0 <= x_value <= 1
        """
        super().__init__(b1, b2, B, d1, d2)
        if x_value is not None:
            assert 0 <= x_value <= 1, "x_value must be between 0 and 1"
        self.x_value = x_value

    def run(self) -> float:
        """
        @see SkiRentalAlgorithm.run
        """
        u = random.random() if self.x_value is None else random.random()
        x = math.log(u * (math.e - 1) + 1)

        z1 = x * self.b1
        z2 = x * self.b2
        Z = x * self.B

        INF = float('inf')
        potential_actions = []

        if z1 <= self.d1:
            potential_actions.append((z1, 'A'))

        if z2 <= self.d2:
            potential_actions.append((z2, 'B'))
        
        t_C = Z / 2.0
        if t_C <= self.d1 and t_C <= self.d2:
            potential_actions.append((t_C, 'C'))

        if not potential_actions:
            cost = self.d1 + self.d2
        else:
            t_action, action_type = min(potential_actions)

            if action_type == 'A':
                cost = min(t_action, self.d1) + self.b1 + self.d2
            elif action_type == 'B':
                cost = min(t_action, self.d2) + self.b2 + self.d1
            else: # action_type == 'C'
                cost = min(t_action, self.d1) + min(t_action, self.d2) + self.B
        
        assert cost >= 0, "Postcondition failed: cost must be non-negative"
        return float(cost)

class HybridRandomAlgorithm(SkiRentalAlgorithm):
    """
    Implements the Hybrid Random Algorithm for the ski rental problem.
    
    This algorithm uses randomized thresholds to decide when to purchase items
    or bundles, with an adaptive parameter alpha controlling bundle preference.
    """
    def __init__(self, b1: int, b2: int, B: int, d1: int, d2: int, alpha: float, u_value: Optional[float] = None) -> None:
        """
        Initialize the Hybrid Random Algorithm.
        
        Args:
            b1: Cost of buying item 1
            b2: Cost of buying item 2
            B: Cost of buying the bundle
            d1: Demand duration for item 1
            d2: Demand duration for item 2
            alpha: Adjustment factor for bundle purchase tendency (must be positive)
            u_value: Optional fixed random value for testing (0 to 1)
            
        Raises:
            ValueError: If alpha is not positive or u_value is not in [0,1]
        """
        super().__init__(b1, b2, B, d1, d2)
        
        if not isinstance(alpha, (int, float)) or alpha <= 0:
            raise ValueError(f"alpha must be positive, got {alpha}")
        if u_value is not None and (not isinstance(u_value, (int, float)) or not (0 <= u_value <= 1)):
            raise ValueError(f"u_value must be in [0,1], got {u_value}")
            
        self.alpha = float(alpha)
        self.u_value = u_value

    def run(self) -> float:
        """
        Execute the Hybrid Random Algorithm.
        
        Returns:
            Total cost incurred by the algorithm
        """
        try:
            # Performance optimization: generate random values once
            u = self.u_value if self.u_value is not None else random.random()
            x_S = math.log(u * (math.e - 1) + 1)
            x_B = x_S ** self.alpha
            
            # Pre-calculate thresholds to avoid repeated computation
            z1 = x_S * self.b1
            z2 = x_S * self.b2
            Z = x_B * self.B
            
            logger.debug(f"Thresholds: z1={z1:.3f}, z2={z2:.3f}, Z={Z:.3f}")
            
            # Initialize state variables
            rent_paid_1 = 0.0
            rent_paid_2 = 0.0
            item1_owned = False
            item2_owned = False
            
            max_duration = int(max(self.d1, self.d2))
            if max_duration == 0:
                return 0.0
            
            for t in range(1, max_duration + 1):
                current_day_rent_incurred = 0

                if t <= self.d1 and not item1_owned:
                    rent_paid_1 += 1
                    current_day_rent_incurred += 1
                
                if t <= self.d2 and not item2_owned:
                    rent_paid_2 += 1
                    current_day_rent_incurred += 1

                if (t > self.d1 and t > self.d2) or (item1_owned and item2_owned):
                    continue

                # Calculate purchase option costs
                options = []

                if not item1_owned and rent_paid_1 >= z1:
                    cost_buy1 = rent_paid_1 + self.b1 + max(0, self.d2 - t + 1)
                    options.append(('buy_item1', cost_buy1))

                if not item2_owned and rent_paid_2 >= z2:
                    cost_buy2 = rent_paid_2 + self.b2 + max(0, self.d1 - t + 1)
                    options.append(('buy_item2', cost_buy2))

                if not item1_owned and not item2_owned and (rent_paid_1 + rent_paid_2) >= Z:
                    cost_bundle = (rent_paid_1 + rent_paid_2) + self.B
                    options.append(('buy_bundle', cost_bundle))
                
                if options:
                    action, min_cost = min(options, key=lambda x: x[1])
                    
                    # Pure rental guard mechanism
                    pure_rental_cost = self.d1 + self.d2
                    if min_cost > pure_rental_cost:
                        logger.debug(f"Guard activated: {min_cost} > {pure_rental_cost}")
                        return pure_rental_cost
                    
                    logger.debug(f"Decision at t={t}: {action} with cost {min_cost}")
                    return min_cost
            
            # No purchase decision made, return total rental cost
            total_cost = rent_paid_1 + rent_paid_2
            logger.debug(f"Pure rental: total cost {total_cost}")
            return total_cost
            
        except Exception as e:
            logger.error(f"Error in HybridRandomAlgorithm.run(): {e}")
            raise RuntimeError(f"Algorithm execution failed: {e}") from e

class AdaptiveHybridRandomAlgorithm(HybridRandomAlgorithm):
    """
    Implements the Hybrid Random Algorithm with an adaptive alpha value.
    The alpha value is calculated based on the ratio of individual purchase costs to bundle cost.
    """
    def __init__(self, b1: int, b2: int, B: int, d1: int, d2: int, u_value: float = None):
        """
        @param {float} u_value - Optional fixed random value for testing (0 to 1).
        @precondition u_value is None or 0 <= u_value <= 1
        @postcondition self.alpha > 0
        """
        # Calculate adaptive alpha
        adaptive_alpha = (b1 + b2) / B
        assert adaptive_alpha > 0, "Calculated adaptive_alpha must be positive"
        
        # Call parent constructor with the calculated alpha
        super().__init__(b1, b2, B, d1, d2, alpha=adaptive_alpha, u_value=u_value)