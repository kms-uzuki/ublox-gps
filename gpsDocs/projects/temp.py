import smbus2 as smbus
import time, signal, sys

BUS = smbus.SMBus(1)

def readGPS():
    c = None
    response = []
    try:
        while True: # Newline, or bad char.
            c = BUS.read_byte(0x42)
 
            if c == 255:
                return False
            elif c == 10:
                break
            else:
                response.append(c)
 
        print(response)
 
    except IOError:
        connectBus()
    except Exception as e:
        print(e)

while 1:
    readGPS()
    time.sleep(0.01)

