#!/usr/bin/env python3

import time, sys, csv, os
import serial, struct, threading

ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=0.1)

os.system("sudo echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null 2>&1")



#nRST     = b"\xB5\x62\x06\x04\x04\x04\x04\x00\xFF\xFF\x02\x00\x0E\x61"
#baudrate = b"\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xD0\x08\x00\x00\x00\xC2\x01\x00\x07\x00\x03\x00\x00\x00\x00\x00\xC0\x7E"
#update   = b"\xB5\x62\x06\x08\x06\x00\x64\x00\x01\x00\x01\x00\x7A\x12" # 10Hz


fname = "/home/pi/projects/data/{}.csv".format(time.strftime('%Y%m%d-%H%M%S'))



#print(ser.is_open, ser.port, ser.baudrate, ser.writable(), end='\n')
#print(f"{nRST}\n{bytes(nRST)}")

def dataLED(loop,_time):
    sleeptime = 0.0001 if _time==None else _time
#    os.system("sudo echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null 2>&1")
    for i in range(0,loop):

        os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness > /dev/null 2>&1")
        time.sleep(sleeptime)
        os.system("echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null 2>&1")
        time.sleep(sleeptime)


def fletchCSum(mes):
    sum1 = 0
    sum2 = 0
    key = 'B' * len(mes[2:])
    unpacked = struct.unpack(key, mes[2:])
    for i in unpacked:
        sum1 = (sum1 + i) % 256
        sum2 = (sum2 + sum1) % 256
    csum = ((sum2 << 8) | sum1)
#    print(f"{sum1}, {sum2}, {(sum1 << 8) | sum2}")
#    print(f"{hex((sum2 << 8) | sum1)}") 
    zed = struct.pack("H", csum)

    return(mes + zed)
    

def X(filename):
	time.sleep(1)
	zed = time.time()
	ledBit = 1
	with open(filename, 'w') as csvfile:
		writer = csv.writer(csvfile)
		while 1:
			try:
				os.system(f"echo {ledBit} | sudo tee /sys/class/leds/led0/brightness > /dev/null 2>&1")
				ledBit = !ledBit
				
				x = ser.readline()
				if x[:6] == b'$GNRMC':
					print(f"{time.time() - zed}\n{x}")
					buf = x.decode("utf-8").split(',')
					writer.writerow(buf)
				else:
					print(x)
					
			except KeyboardInterrupt:
				
				os.system("sudo echo cpu0 | sudo tee /sys/class/leds/led0/trigger")

				print("\nexiting")
				sys.exit()

if __name__ == "__main__":
	print("Initializing...")
	z.start()
#	os.system("sudo echo gpio | sudo tee /sys/class/leds/led0/trigger")

#	time.sleep(1)
#	ser.write(nRST)
#	time.sleep(10)
#	print("reset complete!")
#	time.sleep(1)
#	print("reset complete!")
	
	dGA = fletchCSum(b"\xB5\x62\x06\x01\x03\x00\xF0\x00\x00")
	dLL = fletchCSum(b"\xB5\x62\x06\x01\x03\x00\xF0\x01\x00")
	dSA = fletchCSum(b"\xB5\x62\x06\x01\x03\x00\xF0\x02\x00")
	dSV = fletchCSum(b"\xB5\x62\x06\x01\x03\x00\xF0\x03\x00")
	dTG = fletchCSum(b"\xB5\x62\x06\x01\x03\x00\xF0\x05\x00")
	dST = fletchCSum(b"\xB5\x62\x06\x01\x03\x00\xF0\x07\x00")
	dDA = fletchCSum(b"\xB5\x62\x06\x01\x03\x00\xF0\x08\x00")
	dBS = fletchCSum(b"\xB5\x62\x06\x01\x03\x00\xF0\x09\x00")



	ser.write(dGA); ser.write(dLL); ser.write(dSA); ser.write(dSV)
	ser.write(dTG); ser.write(dST); ser.write(dDA); ser.write(dBS)

	ser.write(fletchCSum(b"\xB5\x62\x06\x08\x06\x00\x64\x00\x01\x00\x00\x00"))

	z.join()
	print("initialization complete!")
	time.sleep(1)

	X(fname)
