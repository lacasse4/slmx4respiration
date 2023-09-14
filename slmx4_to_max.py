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
  
To run the program:
  
  $ python3 slmx4_to_max.py <ip_address>
  
  and use the machine's ip address where Max is running
  or 127.0.0.1 if this code is ran on the same machine.

To receive data in MaxMSP:

    - create a "udpreceive 7401" object
    - link its output to a message's right input 
  
Note:
The radar data rate is fixed in hardware at 10 frames/second.

'''

import os
import sys
import time
import signal
import platform
import socket
from pythonosc import udp_client

from slmx4_health_wrapper import slmx4_health
from slmx4_health_debug import *

PORT = 7401

# Validate command line and parameter

if len(sys.argv) != 2:
    print("usage:")
    print("    slmx4_to_max.py <ip_address>")
    quit()
    
ip_address = sys.argv[1];
try:
    socket.inet_aton(ip_address)
except socket.error:
    print("Invalid ip address")
    quit()


# Create a instance of the slmx4 health wrapper

slmx4 = None;
if platform.system() == "Linux":
    slmx4 = slmx4_health('/dev/ttyACM0') # Linux
if platform.system() == "Windows":
    slmx4 = slmx4_health('COM3') # Windows
if platform.system() == "Darwin":
    slmx4 = slmx4_health('/dev/tty.usbmodem141101') # macOS
if slmx4 == None:
    print("Unrecognized platform")
    quit()

# Open the USB VCOM connection

slmx4.open()

# Get the version info and display

ver = slmx4.get_version()
print('ver =', ver)
# The version info is a tuple which indicates:
# (firmware name, firmwave version, protocol version)

# The udp_client object allow communication with Max (using OSC)

client = udp_client.SimpleUDPClient(ip_address, PORT)

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
    if not slmx4.msg_thread_is_alive():
        print("Message thread terminated unexpectedly")
        quit()
    
    # When data streaming, the SLM-X4 will send two messages back-to-back:
    # the health message, followed by the respiration waveform
    health = slmx4.read_msg()
    if health == None:
        continue
    resp_wave = slmx4.read_msg()
    if health == None:
        continue    

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    debug_health(health)
    # debug_resp_wave(resp_wave)    
    client.send_message("/data",
            [health.health.presence_detected,
            health.health.respiration_detected,
            health.health.movement_detected,
            health.health.movement_type,
            health.health.distance,
            health.health.distance_conf,
            health.health.respiration_rpm,
            health.health.respiration_conf,
            int(health.health.debug[0]),          # frame count
            int(health.health.debug[1])])         # minutes
    