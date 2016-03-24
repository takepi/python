import smbus
import time

adr = 0x08
data = 0x02

bus = smbus.SMBus(1)

while True:
	bus.write_byte(adr, data)
#	val = bus.read_byte(adr)

	print "adr" +str(adr)
	print "data" +str(data)

	time.sleep(3)
