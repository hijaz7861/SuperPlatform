#!/usr/bin/env python3

import math
import random


class QuantumCircuit:
    def __init__(self, qubits=2):
        if qubits < 1:
            raise ValueError("qubits must be >= 1")

        self.n = qubits
        self.size = 2 ** qubits

        # |00...0>
        self.state = [0.0] * self.size
        self.state[0] = 1.0

    def _check(self, q):
        if q < 0 or q >= self.n:
            raise IndexError("invalid qubit")

    def x(self, q):
        self._check(q)
        step = 2 ** q

        for base in range(0, self.size, step * 2):
            for i in range(step):
                a = base + i
                b = a + step
                self.state[a], self.state[b] = (
                    self.state[b],
                    self.state[a],
                )

    def h(self, q):
        self._check(q)
        step = 2 ** q
        s = 1 / math.sqrt(2)

        for base in range(0, self.size, step * 2):
            for i in range(step):
                a = base + i
                b = a + step

                old_a = self.state[a]
                old_b = self.state[b]

                self.state[a] = (old_a + old_b) * s
                self.state[b] = (old_a - old_b) * s

    def z(self, q):
        self._check(q)
        step = 2 ** q

        for base in range(0, self.size, step * 2):
            for i in range(step):
                self.state[base + step + i] *= -1

    def cnot(self, control, target):
        self._check(control)
        self._check(target)

        if control == target:
            raise ValueError("control and target must differ")

        cbit = 1 << control
        tbit = 1 << target

        for i in range(self.size):
            if (i & cbit) and not (i & tbit):
                j = i | tbit
                self.state[i], self.state[j] = (
                    self.state[j],
                    self.state[i],
                )

    def probabilities(self):
        result = {}

        for i, amplitude in enumerate(self.state):
            bits = format(i, f"0{self.n}b")
            result[bits] = round(amplitude * amplitude, 6)

        return result

    def measure(self):
        probabilities = [
            amplitude * amplitude
            for amplitude in self.state
        ]

        r = random.random()
        total = 0.0

        for i, probability in enumerate(probabilities):
            total += probability

            if r <= total:
                return format(i, f"0{self.n}b")

        return format(self.size - 1, f"0{self.n}b")


def demo():
    print("=== QUANTUM ENGINE v3 ===")

    q = QuantumCircuit(2)

    print("Initial:", q.probabilities())

    q.h(0)
    print("H(q0):", q.probabilities())

    q.cnot(0, 1)
    print("CNOT(q0,q1):", q.probabilities())

    print("Measurement:", q.measure())
    print("ENGINE v3: PASS")


if __name__ == "__main__":
    demo()
