import os
import time
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher

IP_MULTICAST = "224.0.0.1"
PORT = 7400

def handler(address, *args):
    print(f"{address}: {args}")
    print("Starting SLMX4 transmission to Max")
    time.sleep(1)
    os.execl("/usr/bin/python3", "python3", "slmx4_to_max.py", args[0])
    quit()

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
    
dispatcher = Dispatcher()
dispatcher.map("/address", handler)
dispatcher.set_default_handler(default_handler)

server = BlockingOSCUDPServer((IP_MULTICAST, PORT), dispatcher)
print("Please send the mac IP address from MaxMSP.")
print("Steps:")
print("    1- With Terminal, find the mac IP address using the command '$ ipconfig getifaddr en0'")
print("    2- In Max, create a messsage contaning '/address <IP address>'")
print("    3- In Max, create the following object: 'updsend 224.0.0.1 7400'")
print("    4- In Max, link the message's output to the objet's input")
print("    5- Trigger the message transmission by clicking on the message'")
print("The SLMX4 will start transmitting to Max. Receive OSC data with 'updreceive 7401'.")
server.serve_forever()

