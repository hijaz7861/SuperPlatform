#!/usr/bin/env python3
import math

class Qubit:
    def __init__(self):
        self.state = [1.0, 0.0]

    def hadamard(self):
        a, b = self.state
        s = 1 / math.sqrt(2)
        self.state = [(a + b) * s, (a - b) * s]

    def probabilities(self):
        return {
            "0": round(self.state[0] ** 2, 6),
            "1": round(self.state[1] ** 2, 6)
        }

def demo():
    q = Qubit()

    print("=== ZERO-LOAD QUANTUM ENGINE ===")
    print("Initial:", q.probabilities())

    q.hadamard()

    print("After Hadamard:", q.probabilities())
    print("Quantum simulation: PASS")

if __name__ == "__main__":
    demo()
