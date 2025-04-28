# variac_widgets.py
#
# Provides funcitons to build UI components (buttons, labels, layouts)
# for the variac control panel
#
# Part of the MVVE Project - see README.md for project overview

from PyQt5.QtWidgets import (QPushButton, QLabel, QVBoxLayout,
                             QFileDialog,QLineEdit, QCheckBox,
                             QHBoxLayout, QWidget, QSizePolicy)

def make_control_panel():
    layout = QVBoxLayout()

    start_pause_button = QPushButton("Start")
    stop_button = QPushButton("Stop")
    load_profile_button = QPushButton("Load Profile")
    file_name_lineedit = QLineEdit()
    file_name_lineedit.setPlaceholderText("No file loaded...")
    hold_voltage_checkbox = QCheckBox("Hold Voltage on Pause")

    voltage_label = QLabel("Voltage: 0V")
    voltage_label.setContentsMargins(0, 0, 0, 0)
    elapsed_time_label = QLabel("Elapsed Time: 0s")
    elapsed_time_label.setContentsMargins(0, 0, 0, 0)

    status_label = QLabel("Status: Waiting")
    file_dialog = QFileDialog()


    label_layout = QVBoxLayout()
    label_layout.setSpacing(0)
    label_layout.addWidget(voltage_label)
    label_layout.addWidget(elapsed_time_label)

    hbox = QHBoxLayout()
    hbox.addWidget(start_pause_button)
    hbox.addWidget(stop_button)
    
    control_layout = QVBoxLayout()
    control_layout.addLayout(label_layout)
    control_layout.addSpacing(50)

    control_layout.addLayout(hbox)
    control_layout.addWidget(hold_voltage_checkbox)

    control_layout.addSpacing(50)
    
    control_layout.addWidget(load_profile_button)
    control_layout.addWidget(file_name_lineedit)
    control_layout.addWidget(status_label)

    container = QWidget()
    container.setLayout(control_layout)
    container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
    container.setMaximumWidth(150)

    return (container, start_pause_button,
            stop_button, load_profile_button,
            file_name_lineedit, hold_voltage_checkbox,
            status_label, voltage_label,
            elapsed_time_label)

def setup_button_connections(window):
    window.start_pause_button.clicked.connect(window.handle_start_pause)
    window.stop_button.clicked.connect(window.handle_stop)
    window.load_profile_button.clicked.connect(window.handle_load_profile)

def reset_ui_labels(window):
    window.voltage_label.setText("Voltage: 0V")
    window.elapsed_time_label.setText("Elapsed Time: 0s")

