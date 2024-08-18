import snap7
from snap7.util import *

plc = snap7.client.Client()
plc.connect('192.168.0.1',0,1)
# Check if connected
if plc.get_connected():
    print("Connected to PLC")
else:
    print("Failed to connect to PLC")