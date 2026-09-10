import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))

from quantum import Qubit

q = Qubit()

assert q.probabilities() == {"0": 1.0, "1": 0.0}

q.hadamard()

p = q.probabilities()

assert abs(p["0"] - 0.5) < 0.001
assert abs(p["1"] - 0.5) < 0.001

print("QUANTUM ENGINE TEST: PASS")
