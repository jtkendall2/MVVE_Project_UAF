# servo.py
#
# Defines the servomotor control class for the MVVE project.
# Currently provides simulated functionality—will be expanded in future.
#
# Part of the MVVE Project - see README.md for project overview

class SimulatedServo:
    def __init__(self):
        self.position = 0.0

    def set_voltage(self, target_voltage):
        print(f"[Servo] Setting voltage to {target_voltage} V")
        self.position = target_voltage
