# slmx4respiration

This repo holds few Python3 programs that interacts with the SLMX4 radar sensor from SensorLogic. 
The main objective was to create a program that extracts respiration frequency in breath per minute (bpm) and transmits it to MaxMSP.

The program 'slmx4_to_max.py' interefaces with the SLMX4 sensor and transmits data to Max via OSC (i.e. updreceive).
The program 'start_slmx4.py' was written to integrate 'slmx4_to_max.py' nicely to Max. It's a upd server. Once started, it waits for incomming OSC messages with the form '/address <ip_address>' where <ip_address> is the ip address of the machine hosting Max. Once the ip address is received, the program 'slmx4_to_max.py is launched. 

## Installation:
Prior to running this program, some python module must be installed. Open a terminal and execute the following commands:
  
  $ pip3 install pyserial
  $ pip3 install protobuf
  $ pip3 install python-osc

This has been tested on Linux (Raspberry Pi 32 bits) and macOS (Monterey). Note that the python files povided by SensorLogic where modified (i.e. slmx4_health_wrapper.py, slmx4_health_debug.py).

## Setup:
The target system is comprised of a Mac running MaxMSP and a Raspeberry Pi 4B connected to the SLMX4 sensor via USB. The two computers must be on the same local area network (LAN). 

In Max, send the message '/address <ip_address>' with a 'updsend 224.0.0.1 7400' object. <ip_address> must be replace with the ip address of the Mac runnning Max. The updsend object must be 'updsend 224.0.0.1 7400'.
Also in Max, create a 'udpreceive 7401' object and link its output to an empty message (top right input). 
On the Raspberry Pi, open a terminal and start the slmx4 sensor with the following command:
  
  $ cd slmx4respiration
  $ python3 start_slmx4.py

The click on the '/address <ip_address>' message. The empty message will show data from the SLMX4 sensor.
