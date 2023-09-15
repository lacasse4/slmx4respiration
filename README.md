# slmx4respiration
This repo holds few Python3 programs to interacts with the SLMX4 radar sensor from SensorLogic. 
The main objective was to create a program that extracts respiration frequency in breath per minute (bpm) and transmits it to MaxMSP.

The program 'slmx4_to_max.py' interefaces with the SLMX4 sensor and transmits data to Max via OSC (i.e. updreceive).
The program 'start_slmx4.py' was written to integrate 'slmx4_to_max.py' nicely to Max. It's a upd server. Once started, it waits for incomming OSC messages with the form '/address <ip_address>' where <ip_address> is the ip address of the machine hosting Max. Once the ip address is received, the program 'slmx4_to_max.py is launched. 

## Installation:
Prior to running this program, some python module must be installed. Open a terminal and execute the following commands:
  
  - $ pip3 install pyserial
  - $ pip3 install protobuf
  - $ pip3 install python-osc

The Python programs have been tested on Linux raspberrypi 6.1.21 (32 bits) and macOS Monterey. Note that the python files povided by SensorLogic where modified (i.e. slmx4_health_wrapper.py, slmx4_health_debug.py).

## Setup:
The target system is comprised of a Mac running MaxMSP and a Raspeberry Pi 4B connected to the SLMX4 sensor via USB.  Note that the SLMX4 sensor must run the Health Firmware provided by SensorLogic. The two computers must be on the same local area network (LAN). Experience has shown that it is preferable to setup a separate network to host these machine (cabled or wifi). I have encountered unstable behaviors on a larger network where unrelated traffic was going on.

## Starting the system
### Approach 1
In Max, send the message '/address <ip_address>' to an 'updsend 224.0.0.1 7400' object. <ip_address> must be replace with the ip address of the Mac runnning Max. On a Mac, the ip address can be displayed with the command:

  - $ ipconfig getifaddr en0

The updsend object must be 'updsend 224.0.0.1 7400'. 224.0.0.1 is a special address to perform a multicast on a local LAN.
Also in Max, create a 'udpreceive 7401' object and link its output to an empty message (top right input). 
On the Raspberry Pi, open a terminal and start the SLMX4 sensor with the following commands:
  
  - $ cd slmx4respiration
  - $ python3 start_slmx4.py

The click on the '/address <ip_address>' message. The empty message will show data from the SLMX4 sensor.
The file 'Screen Shot 2023-09-13 ar 10.33.56.png' shows a basic Max patch performing Approach 1.

### Approach 2
Alternatively, you can hard code the ip address of the machine running Max in the command calling the python program on the Raspberry Pi. This simplifies the patch on Max as you can remove the updsend object. In order do so, on the Raspberry Pi, open a terminal and start the SLMX4 sensor with the following commands:

  - $ cd slmx4respiration
  - $ python3 slmx4_to_max.py <ip_address>

where <ip_address> is the ip address of the machine running Max. 

### Approach 3
It is also possible to connect the SLMX4 sensor via USB directly to the Mac running Max. The Python programs normaly running on the Raspberry Pi will run on a Mac and have been tested on macOS Montery with Python 3.10. This is a setup without a Raspberry Pi. In this case, use Approach #2 with ip address 127.0.0.1 or localhost.
