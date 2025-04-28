# variac_plot.py
#
# Manages real-time plotting of voltage data and
# mouse cursor tracking.
#
# Part of the MVVE Project - see README.md for project overview

import pyqtgraph as pg
from pyqtgraph import InfiniteLine
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
import time

class VariacPlot(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.elapsed_profile_time = 0.0
        self.last_update_real_time = None

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('black')
        self.plot_widget.showGrid(x=True, y=True)

        self.legend = self.plot_widget.addLegend()

        self.plot_widget.setLabel('bottom', 'Time', units='s')
        self.plot_widget.setLabel('left', 'Voltage', units='V')
        self.plot_widget.getAxis('bottom').setTextPen('w')
        self.plot_widget.getAxis('left').setTextPen('w')

        self.plot_widget.setYRange(0, 150)
        self.plot_widget.enableAutoRange(axis='y', enable=False)

        self.target_curve = self.plot_widget.plot(pen='r', name="Target Voltage")
        self.feedback_curve = self.plot_widget.plot(pen='g', name="Feedback Voltage")

        self.vLine = InfiniteLine(angle=90, movable=False, pen={'style': Qt.DashLine})
        self.vLine.hide()
        self.plot_widget.getViewBox().addItem(self.vLine)
        self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)

        self.data_label = pg.TextItem(color='w', anchor=(0,1))
        self.data_label.hide()
        self.plot_widget.getViewBox().addItem(self.data_label)
        
        self.layout.addWidget(self.plot_widget)

        self.target_curve = self.plot_widget.plot(pen='r')
        self.feedback_curve = self.plot_widget.plot(pen='g')

        self.time_data = []
        self.target_data = []
        self.feedback_data = []
        self.start_time = None
        self.paused_time = None
        self.profile_loaded = False

    def start_timing(self):
        if self.paused_time is None:
            self.start_time = time.time()
        else:
            pause_duration = time.time() - self.paused_time
            self.start_time += pause_duration
            self.paused_time = None

    def pause_timing(self):
        if self.start_time is not None:
            self.paused_time = time.time()

    def update_plot(self, target_voltage, feedback_voltage, elapsed_time):
        self.time_data.append(elapsed_time)
        self.target_data.append(target_voltage)
        self.feedback_data.append(feedback_voltage)

        self.target_curve.setData(self.time_data, self.target_data)
        self.feedback_curve.setData(self.time_data, self.feedback_data)

        window_size = 10
        if elapsed_time > window_size:
            self.plot_widget.setXRange(elapsed_time - window_size, elapsed_time)
        else:
            self.plot_widget.setXRange(0, window_size)

    def mouse_moved(self, pos):
        if not self.profile_loaded:
            return
        vb = self.plot_widget.getViewBox()
        if not vb.sceneBoundingRect().contains(pos):
            return
        
        mouse_point = vb.mapSceneToView(pos)
        x = mouse_point.x()
        y = mouse_point.y()

        x_data_target, y_data_target = self.target_curve.getData()
        x_data_feedback, y_data_feedback = self.feedback_curve.getData()

        if (x_data_target is not None and len(x_data_target) > 0 and
            x_data_feedback is not None and len(x_data_feedback) > 0):

            self.vLine.setPos(x)
            idx_target = min(range(len(x_data_target)), key=lambda i: abs(x_data_target[i] - x))
            target_voltage = y_data_target[idx_target]
            idx_feedback = min(range(len(x_data_feedback)), key=lambda i: abs(x_data_feedback[i] - x))
            feedback_voltage = y_data_feedback[idx_feedback]
            label_text = f"Time: {x:.2f} s\nTarget: {target_voltage:.2f} V\nFeedback: {feedback_voltage:.2f} V"
            self.data_label.setText(label_text)
            self.data_label.setPos(x, y)
            self.data_label.show()
            
    def clear(self):
        self.time_data.clear()
        self.target_data.clear()
        self.feedback_data.clear()
        self.start_time = None
        self.paused_time = None
        self.elapsed_profile_time = 0.0
        self.last_update_real_time = None
        self.target_curve.setData([], [])
        self.feedback_curve.setData([], [])
        self.plot_widget.setXRange(0,10)
