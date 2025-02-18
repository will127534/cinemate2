from time import sleep
from signal import pause
import redis
import threading
import numpy as np
import RPi.GPIO as GPIO 
from module.cinepi import Config, CinePi, CinePiController
from module.monitor import DriveMonitor
from module.simple_gui import SimpleGUI
from module.manual_controls import ManualControls

# Define ISO array

iso_array = [100, 200, 400, 800, 1600, 3200]

# Define shutter angle array

shutter_array = list(range(1, 361))     # Create an array from 1 to 360
index = shutter_array.index(173)              # Find the index of 173
shutter_array[index] = 172.8            # Replace 173 with 172.8

# Define FPS array

fps_array = [1,2,4,8,16,18,24,25,33,48,50]


# Create the Redis connection
r = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)

if __name__ == "__main__":
    try:
        # Instantiate and start the Monitor instance, for monitoring of SSD
        monitor = DriveMonitor('/media/RAW/', rec_out_pins=[5], button_pins=[26])
        threading.Thread(target=monitor.start_space_monitoring, args=(0.1,)).start()

        # Instantiate the CinePi instance and CinePiController
        cinepi = CinePi(r, monitor, shutter_array)

        cinepi_controller = CinePiController(cinepi, r, monitor)
        
        # Initialize SimpleGUI with the controller and monitor instances
        simple_gui = SimpleGUI(cinepi, cinepi_controller, monitor)

        # Instantiate the ManualControls class with the necessary GPIO pins
        manual_controls = ManualControls(cinepi_controller, monitor, cinepi.USBMonitor, 
                                        iso_steps=iso_array,    # Array for selectable ISO values (100-3200)
                                        shutter_angle_steps=shutter_array,       # Array for selectable shutter angle values (0-360 degrees in increments of 2 degrees)
                                        fps_steps=fps_array,      # Array for selectable fps values (1-50). To create and array of all frame rates from 1 - 50, replace the array with "list(range(1, 50))""
                                        iso_pot=0,                                     # Analog channel for ISO control, if Grove Base HAT is attached (if defined, it overrides any iso_inc and iso_dec pins). If no Grove Base HAT is attached, set this to None
                                        shutter_angle_pot=2,                           # Analog channel for shutter angle control, if Grove Base HAT is attached. If no Grove Base HAT is attached, set this to None
                                        fps_pot=4,                                     # Analog channel for fps control, if Grove Base HAT is attached. If no Grove Base HAT is attached, set this to None
                                        iso_inc_pin=23,                                # GPIO pin for button for increasing ISO
                                        iso_dec_pin=25,                                # GPIO pin for button for decreasing ISO
                                        pot_lock_pin=16,                               # GPIO pin for attaching shutter angle and fps potentiometer lock switch
                                        res_button_pin=[13, 24],                       # GPIO resolution button - switches between 1080 (cropped) and 1520 (full frame)
                                        fps_mult_pin1=18,                              # Flip switch for 50% frame rate
                                        fps_mult_pin2=19,                              # Flip switch for 200% frame rate (up to 50 fps)
                                        rec_pin=[4, 6, 22])                            # GPIO recording pins
        # print("manual controls running")
        pause()
    finally:
        GPIO.cleanup()
