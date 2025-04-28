# feedback.py
#
# Defines the class for reading back voltage from variac
# Currently simulates feedback voltage for visual reference
#
# Part of the MVVE Project - see README.md for project overview

import random

class SimulatedFeedback:
    def __init__(self):
        self.simulated_voltage = 0.0
        self.target_voltage = 0.0
        self.response_rate = 0.1  # controls how fast it follows
        self.noise_amplitude = 0.5  # magnitude of random voltage noise

    def simulate_voltage(self, target_voltage):
        # Just set the new goal (no immediate move)
        self.target_voltage = target_voltage

    def read_voltage(self):
        # Gradually move toward target
        self.simulated_voltage += self.response_rate * (self.target_voltage - self.simulated_voltage)
        # Add some random noise
        self.simulated_voltage += random.uniform(-self.noise_amplitude, self.noise_amplitude)
        return self.simulated_voltage
