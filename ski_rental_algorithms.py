import math
import random
from abc import ABC, abstractmethod

class SkiRentalAlgorithm(ABC):
    """
    Abstract base class for ski rental algorithms.
    """
    def __init__(self, b1: int, b2: int, B: int, d1: int, d2: int):
        """
        @param {int} b1 - The cost of buying item 1.
        @param {int} b2 - The cost of buying item 2.
        @param {int} B - The cost of buying the bundle.
        @param {int} d1 - The total demand duration for item 1.
        @param {int} d2 - The total demand duration for item 2.
        @precondition b1 > 0, b2 > 0, B > 0, d1 >= 0, d2 >= 0
        """
        assert b1 > 0, "b1 must be positive"
        assert b2 > 0, "b2 must be positive"
        assert B > 0, "B must be positive"
        assert d1 >= 0, "d1 must be non-negative"
        assert d2 >= 0, "d2 must be non-negative"

        self.b1 = b1
        self.b2 = b2
        self.B = B
        self.d1 = d1
        self.d2 = d2

    @abstractmethod
    def run(self) -> float:
        """
        Runs the algorithm and returns the calculated cost.
        @returns {float} The total cost incurred by the algorithm.
        @postcondition retval >= 0
        """
        pass

class OptimalOfflineAlgorithm(SkiRentalAlgorithm):
    """
    Calculates the optimal offline cost for the two-item ski rental problem.
    """
    def run(self) -> float:
        """
        @see SkiRentalAlgorithm.run
        """
        cost_rent_all = self.d1 + self.d2
        cost_buy1_rent2 = self.b1 + self.d2
        cost_rent1_buy2 = self.d1 + self.b2
        cost_buy_both_separately = self.b1 + self.b2
        cost_buy_bundle = self.B
        
        cost = min(cost_rent_all, cost_buy1_rent2, cost_rent1_buy2, cost_buy_both_separately, cost_buy_bundle)
        assert cost >= 0, "Postcondition failed: cost must be non-negative"
        return float(cost)

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
    """
    def __init__(self, b1: int, b2: int, B: int, d1: int, d2: int, alpha: float, u_value: float = None):
        """
        @param {float} alpha - Adjustment factor for bundle purchase tendency.
        @param {float} u_value - Optional fixed random value for testing (0 to 1).
        @precondition alpha > 0
        @precondition u_value is None or 0 <= u_value <= 1
        """
        super().__init__(b1, b2, B, d1, d2)
        assert alpha > 0, "alpha must be positive"
        if u_value is not None:
            assert 0 <= u_value <= 1, "u_value must be between 0 and 1"
        self.alpha = alpha
        self.u_value = u_value

    def run(self) -> float:
        """
        @see SkiRentalAlgorithm.run
        """
        rent_paid_1 = 0
        rent_paid_2 = 0
        item1_owned = False
        item2_owned = False
        total_rent_accumulated_if_no_purchase = 0

        max_duration = max(self.d1, self.d2)

        for t in range(1, max_duration + 1):
            current_day_rent_incurred = 0

            if t <= self.d1 and not item1_owned:
                rent_paid_1 += 1
                current_day_rent_incurred += 1
            
            if t <= self.d2 and not item2_owned:
                rent_paid_2 += 1
                current_day_rent_incurred += 1
            
            total_rent_accumulated_if_no_purchase += current_day_rent_incurred

            if (t > self.d1 and t > self.d2) or (item1_owned and item2_owned):
                continue

            u = self.u_value if self.u_value is not None else random.random()
            x_S = math.log(u * (math.e - 1) + 1)
            x_B = x_S ** self.alpha

            z1 = x_S * self.b1
            z2 = x_S * self.b2
            Z = x_B * self.B

            cost_option_buy1 = float('inf')
            cost_option_buy2 = float('inf')
            cost_option_buy_bundle = float('inf')

            if not item1_owned and rent_paid_1 >= z1:
                cost_option_buy1 = rent_paid_1 + self.b1 + self.d2

            if not item2_owned and rent_paid_2 >= z2:
                cost_option_buy2 = rent_paid_2 + self.b2 + self.d1

            if not item1_owned and not item2_owned and (rent_paid_1 + rent_paid_2) >= Z:
                cost_option_buy_bundle = (rent_paid_1 + rent_paid_2) + self.B
            
            min_purchase_cost = min(cost_option_buy1, cost_option_buy2, cost_option_buy_bundle)

            if min_purchase_cost != float('inf'):
                assert min_purchase_cost >= 0, "Postcondition failed: cost must be non-negative"
                
                # Pure rental guard mechanism
                pure_rental_cost = float(self.d1 + self.d2)
                if min_purchase_cost > pure_rental_cost:
                    return pure_rental_cost

                return float(min_purchase_cost)
                
        assert total_rent_accumulated_if_no_purchase >= 0, "Postcondition failed: cost must be non-negative"
        return float(total_rent_accumulated_if_no_purchase)

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