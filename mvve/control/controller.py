# controller.py
#
# Manages execution of loaded voltage profile.
# Controls servomotor and updates feedback, and
# handles start, pause, and stop operations.
#
# Part of the MVVE Project - see README.md for project overview

import threading
import time

class Controller:
    def __init__(self, profile, servo, feedback, ui_callback=None):
        self.profile = profile
        self.servo = servo
        self.feedback = feedback
        self.ui_callback = ui_callback

        self.running = False
        self.paused = False
        self.profile_index = 0
        self.current_target_voltage = 0.0
        self.thread = None

    def start(self):
        if not self.profile:
            print("[Controller] No profile loaded.")
            return
        if self.thread is None or not self.thread.is_alive():
            self.running = True
            self.paused = False
            if self.profile_index == 0:
                self.thread = threading.Thread(target=self.run_profile)
                self.thread.start()
            else:
                self.thread = threading.Thread(target=self.run_profile)
                self.thread.start()
            
    def run_profile(self):
        while self.profile_index < len(self.profile):
            if not self.running:
                self.paused = True
                return

            t_target, v_target = self.profile[self.profile_index]
            self.current_target_voltage = v_target

            self.servo.set_voltage(v_target)
            self.feedback.simulate_voltage(v_target)

            if self.ui_callback:
                self.ui_callback(v_target, self.feedback.read_voltage())

            if not hasattr(self,'remaining_time') or self.remaining_time is None:
                self.remaining_time = t_target / 1000.0  
            start_time = time.time()

            while self.remaining_time > 0:
                if not self.running:
                    self.remaining_time -= (time.time() - start_time)
                    if self.remaining_time < 0:
                        self.remaining_time = 0
                    self.paused = True
                    return

                time.sleep(0.01)
                self.remaining_time -= 0.01

            self.remaining_time = None
            self.profile_index += 1

        self.running = False
        self.paused = False
        self.profile_index = 0
        self.current_target_voltage = 0.0
        self.thread = None

    def pause(self):
        self.running = False
        self.paused = True

    def stop(self):
        self.running = False
        self.paused = True
        self.profile_index = 0
        self.current_target_voltage = 0.0
        if self.servo:
            self.servo.set_voltage(0)
        self.thread = None

    def set_profile(self, profile):
        self.profile = profile
        self.profile_index = 0

