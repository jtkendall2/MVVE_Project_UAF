# variac_ui.py
#
# Builds main control window for MVVE project.
# Manages user interaction: loading profiles, starting, pausing,
# stopping controller, and updating plot and feedback 
#
# Part of the MVVE Project - see README.md for project overview

import time
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import QTimer

from .variac_widgets import make_control_panel, \
                            setup_button_connections, reset_ui_labels
from .variac_plot import VariacPlot

from ..control.controller import Controller
from ..control.servo import SimulatedServo as Servo
from ..control.feedback import SimulatedFeedback as Feedback
from ..voltage_profile.profileloader import load_profile


class VariacUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Variac Controller")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.servo = Servo()
        self.feedback = Feedback()
        self.controller = Controller(None, self.servo, self.feedback)
        
        self.profile_loaded = False
        self.feedback_interval_ms = 10
        self.plot_interval_ms = 10 
        self.is_running = False

        self.plot = VariacPlot()
        self.main_layout.addWidget(self.plot)

        (self.control_panel, self.start_pause_button,
         self.stop_button, self.load_profile_button,
         self.file_name_lineedit, self.hold_voltage_checkbox,
         self.status_label, self.voltage_label,
         self.elapsed_time_label) = make_control_panel()
        
        self.main_layout.addWidget(self.control_panel)

        self.feedback_timer = QTimer(self)
        self.feedback_timer.timeout.connect(self.update_feedback)
        self.plot_timer = QTimer(self)
        self.plot_timer.timeout.connect(self.update_plot)

        setup_button_connections(self)
        self.start_pause_button.setEnabled(False)

    def update_feedback(self):
        if self.profile_loaded:
            if self.is_running:
                self.controller.current_feedback_voltage = self.feedback.read_voltage()
            else:
                if not self.hold_voltage_checkbox.isChecked():
                    self.feedback.simulate_voltage(0)
                    self.controller.current_feedback_voltage = self.feedback.read_voltage()
                else:
                    self.controller.current_feedback_voltage = self.feedback.read_voltage()

    def update_plot(self):
        if self.profile_loaded and self.is_running:
            now = time.time()

            if self.plot.last_update_real_time is None:
                self.plot.last_update_real_time = now
                return

            dt = now - self.plot.last_update_real_time
            self.plot.last_update_real_time = now

            self.plot.elapsed_profile_time += dt

            feedback_voltage = self.feedback.read_voltage()
            target_voltage = self.controller.current_target_voltage

            self.plot.update_plot(target_voltage,
                                  feedback_voltage,
                                  self.plot.elapsed_profile_time)

            self.voltage_label.setText(f"Voltage: {feedback_voltage:.2f}V")
            self.elapsed_time_label.setText(f"Elapsed Time:{self.plot.elapsed_profile_time:.2f}s")

    def handle_start_pause(self):
        if not self.profile_loaded:
            return

        if not self.is_running:
            self.controller.start()
            self.feedback_timer.start(self.feedback_interval_ms)
            self.plot_timer.start(self.plot_interval_ms)
            self.start_pause_button.setText("Pause")
            self.status_label.setText("Status: Running")
            self.is_running = True
        else:
            self.controller.pause()
            self.plot_timer.stop()
            self.plot.last_update_real_time = None
            
            if not self.hold_voltage_checkbox.isChecked():
                self.servo.set_voltage(0)
                self.feedback.simulate_voltage(0)
                
            self.start_pause_button.setText("Start")
            self.status_label.setText("Status: Paused")
            self.is_running = False
        
    def handle_stop(self):
        self.controller.stop()
        self.feedback_timer.stop()
        self.plot_timer.stop()
        self.servo.set_voltage(0)
        self.feedback.simulate_voltage(0)
        self.plot.clear()
        reset_ui_labels(self)
        self.start_pause_button.setText("Start")
        self.status_label.setText("Status: Waiting")
        self.is_running = False
        
    def handle_load_profile(self):
        filepath, _ = QFileDialog.getOpenFileName(self,
                                                  "Open Profile",
                                                  "",
                                                  "CSV Files (*.csv)")
        if filepath:
            profile = load_profile(filepath)
            self.controller.set_profile(profile)
            self.profile_loaded = True
            self.plot.clear()
            reset_ui_labels(self)
            self.file_name_lineedit.setText(filepath.split("/")[-1])
            self.start_pause_button.setEnabled(True)
            self.plot.profile_loaded = True
            self.plot.vLine.show()
