''' 
Program: slmx4_to_max.py
Author: Vincent Lacasse
Date: 2023-09-10

This program extract respiration frequency in breath per minute (bpm)
from a SensorLogic SLMX4 sensor and sends it to MaxMSP via OSC

Installation
  Prior to running this program, some python module must be installed.
  On maxOS, open a terminal and execute the following commands
  
  $ pip3 install pyserial
  $ pip3 install protobuf
  $ pip3 install python-osc
  
Additionnaly, the following modules (provided by SensorLogic)
must be present in the directory where the code is ran.

  1- slmx4_health_wrapper.py
  2- slmx4_usb_vcom_pb2.py
  3- slm4x_health_debug.py (if debugging output is required)
  
To run the program
  
  $ python3 slmx4_to_max.py

To receive data in MaxMSP

    - create a "udpreceive 7401" object
    - link its output to a message's input 
  
Note:
The radar data rate is fixed in hardware at 10 frames/second.

'''

import os
import time
import signal

from slmx4_health_wrapper import slmx4_health
from slmx4_health_debug import *

from pythonosc import udp_client

# Create a instance of the slmx4 health wrapper
# slmx4 = slmx4_health('/dev/ttyACM0') # Linux
# slmx4 = slmx4_health('COM3') # Windows
slmx4 = slmx4_health('/dev/tty.usbmodem141101') # macOS

# Open the USB VCOM connection

slmx4.open()

# Get the version info and display

ver = slmx4.get_version()
print('ver =', ver)
# The version info is a tuple which indicates:
# (firmware name, firmwave version, protocol version)

# The udp_client object allow communication with Max (using OSC)

ip = "127.0.0.1"    # loop back.  This script must be run on the same machine as MasMSP
port = 7400         # port to be used in the "updreceive" object in MaxMSP
client = udp_client.SimpleUDPClient(ip, port)

# Setup a clean-up function that will be called when CTRL_C is pressed. 

def cleanup(signum, frame):
    slmx4.stop()  # Stop data streaming
    slmx4.close() # Close the USB VCOM connection
    quit()

# Pressing CTRL_C will execute cleanup() and exit the program

signal.signal(signal.SIGINT, cleanup)
print('Press CTRL-C to terminate loop')
time.sleep(1)

# Start data streaming at fixed rate

slmx4.start()

# Main loop
while True:
    # When data streaming, the SLM-X4 will send two messages back-to-back:
    # the health message, followed by the respiration waveform
    health = slmx4.read_msg()
    resp_wave = slmx4.read_msg()

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    debug_health(health)
    # debug_resp_wave(resp_wave)
    client.send_message("/freq", health.health.respiration_rpm) 