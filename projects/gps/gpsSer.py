from ublox_gps import UbloxGps
import serial
# Can also use SPI here - import spidev
# I2C is not supported

port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
gps = UbloxGps(port)

def run():
  
  try: 
    print("Listenting for UBX Messages.")
    while True:
      try: 
        coords = gps.geo_coords()
        print(f"{coords.lat}, {coords.lon}")
      except (ValueError, IOError) as err:
        print(err)
  
  finally:
    port.close()

if __name__ == '__main__':
  run()
