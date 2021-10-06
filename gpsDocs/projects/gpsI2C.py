import time
import smbus2 as smbus
import signal 
import sys

BUS = None
address = 0x42
gpsReadInterval = 0.03

def connectBus():
    global BUS
    BUS = smbus.SMBus(1)

def parseResponse(line):
    if line.count(36) == 1:
        if len(line) < 84:
            cError = 0
            for c in line:
                if (c < 32 or c > 122) and c != 13:
                    cError += 1
            if cError == 0:
                gpsChars = ''.join(chr(c) for c in line)
                if gpsChars.find('txbuf') == -1:
                    gpsStr, chkSum = gpsChars.split('*', 2)
                    gpsComponents = gpsStr.split(',')

                    chkVal = 0

                    for d in gpsStr[1:]:
                        chkVal ^= ord(d)
                    if chkVal == int(chkSum, 16):
                        print(gpsChars)






def handle_ctrl_c(signal, frame):
        sys.exit(130)
 
#This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)
 
def readGPS():
    c = None
    response = []
    try:
        while True: # Newline, or bad char.
            c = BUS.read_byte(address)
 
            if c == 255:
                return False
            elif c == 10:
                break
            else:
                response.append(c)
 
        parseResponse(response)
 
    except IOError:
        connectBus()
    except Exception as e:
        print(e)
 
connectBus()
 
while True:
    readGPS()
    time.sleep(gpsReadInterval)
