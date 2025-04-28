# main.py
#
# Entry point for MVVE application
# Initializes and launches main PyQt5 user interface
#
# Part of the MVVE Project - see README.md for project overview

from PyQt5.QtWidgets import QApplication
from mvve.ui.variac_ui import VariacUI
from mvve.control.servo import SimulatedServo
from mvve.control.feedback import SimulatedFeedback
from mvve.control.controller import Controller

if __name__ == '__main__':
    app = QApplication([])

    servo = SimulatedServo()
    feedback = SimulatedFeedback()
    controller = Controller(None, servo, feedback)

    window = VariacUI()
    window.show()
    app.exec_()
