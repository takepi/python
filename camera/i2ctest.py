import smbus
import time

adr = 0x08
data = 0x01

bus = smbus.SMBus(1)

bus.write_byte(adr, data)
#	val = bus.read_byte(adr)

print "adr" +str(adr)
print "data" +str(data)
print "val", val
