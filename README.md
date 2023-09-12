# vernierrespiration

This repo holds few Python3 programs that interacts with the Vernier Respiration Belt sensor (GDX-RB). 
The main objective was to create a simple program that extract respiration frequency in breath per minute (bpm) from a Vernier GDX-RB sensor and transmit this information to MaxMSP. This program was written in Python3 and is named 'vernier_to_max.py'. The other programs contained in this repo were used as tests.

vernier_to_max.py uses 2 external modules:
  1- the GDX library which allows communication the GDX-RB sensor.  
     This library was provided by Vernier.
  2- the OSC library which allows communication with MaxMSP 

Installation
  Prior to running this program, some python module must be installed.
  On macOS, open a terminal and execute the following commands
  
  $ pip3 install godirect
  $ pip3 install python-osc
  
  Also, the running directory must contain the gdx/ directory 
  provided by Vernier.

To run the program
  
  $ python3 vernier_to_max.py

To receive data in MaxMSP

    - create a "udpreceive 7400" object
    - link its output to a message's input 

# slmx4respiration
