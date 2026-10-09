"""Bounded, offline implementation checks. This is not a competitive-ratio proof."""
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ski_rental_algorithms import (AdaptiveHybridRandomAlgorithm, CorrelatedRandomAlgorithm, OptimalOfflineAlgorithm)

subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)
checked = 0
for b1, b2, bundle in [(10, 100, 11), (10, 50, 100), (50, 100, 80), (20, 40, 55)]:
    for d1 in [0, 1, 5, 20, 60]:
        for d2 in [0, 1, 10, 30, 100]:
            optimum = min(d1+d2, b1+d2, d1+b2, b1+b2, bundle)
            assert OptimalOfflineAlgorithm(b1, b2, bundle, d1, d2).run() == optimum
            for u in [0.0, 0.1, 0.5, 0.9, 1.0]:
                for cls, kwargs in [(AdaptiveHybridRandomAlgorithm, {"u_value": u}), (CorrelatedRandomAlgorithm, {"x_value": u})]:
                    first = cls(b1, b2, bundle, d1, d2, **kwargs).run()
                    second = cls(b1, b2, bundle, d1, d2, **kwargs).run()
                    assert first == second, "Fixed random input must be repeatable"
                    assert math.isfinite(first) and first >= optimum, "Cost must be finite and no less than offline optimum"
                    checked += 1
print(json.dumps({"status": "passed", "bounded_cost_checks": checked, "formal_proof": "incomplete", "scope": "integer demand, four cost scenarios, fixed random grid"}, indent=2))
