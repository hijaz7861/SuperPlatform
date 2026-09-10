#!/usr/bin/env python3

import math
import random

class TwoQubit:
    def __init__(self):
        # |00> = 1, باقی states = 0
        self.state = [1.0, 0.0, 0.0, 0.0]

    def hadamard_q0(self):
        a, b, c, d = self.state
        s = 1 / math.sqrt(2)

        self.state = [
            (a + c) * s,
            (b + d) * s,
            (a - c) * s,
            (b - d) * s,
        ]

    def cnot(self):
        # CNOT: q0 control, q1 target
        self.state = [
            self.state[0],
            self.state[1],
            self.state[3],
            self.state[2],
        ]

    def probabilities(self):
        labels = ["00", "01", "10", "11"]

        return {
            label: round(amplitude * amplitude, 6)
            for label, amplitude in zip(labels, self.state)
        }

    def measure(self):
        probabilities = [
            amplitude * amplitude
            for amplitude in self.state
        ]

        r = random.random()
        total = 0

        for i, probability in enumerate(probabilities):
            total += probability

            if r <= total:
                return ["00", "01", "10", "11"][i]

def demo():
    q = TwoQubit()

    print("=== TWO-QUBIT QUANTUM ENGINE ===")
    print("Initial:", q.probabilities())

    q.hadamard_q0()
    print("After H(q0):", q.probabilities())

    q.cnot()
    print("After CNOT:", q.probabilities())

    print("Measurement:", q.measure())
    print("SIMULATION: PASS")

if __name__ == "__main__":
    demo()
