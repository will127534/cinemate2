import threading
import keyboard

class Keyboard(threading.Thread):
    def __init__(self, cinepi_controller, monitor):
        threading.Thread.__init__(self)
        self.controller = cinepi_controller
        self.monitor = monitor

    def run(self):
        keyboard.on_press_key("r", self.handle_key_event)
        keyboard.wait("esc")  # Wait for the "esc" key to exit the event loop

    def handle_key_event(self, event):
        if event.name == "r":
            # Start/stop recording
            if self.controller.get_recording_status():
                self.controller.stop_recording()
                print("Recording stopped")
            else:
                self.controller.start_recording()
                print("Recording started")
        # Add more key handling code as needed
