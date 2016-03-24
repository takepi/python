import RPi.GPIO as gpio

class AbsEncoder:
	def __init__(self):
		self.pins = (29,31,33,35,37,40,38,36)
		for pin in self.pins:
			gpio.setup(pin, gpio.IN, pull_up_down = gpio.PUD_UP)
		self.offset = 41
		
	def GetCount(self):
		grayData = 0
		data = 0
		for pin, i in zip(self.pins, [i for i in range(8)]):
			if not gpio.input(pin):
				grayData |= 2**i
		
		data |= grayData & 0x80
		for i in range(6,-1,-1):
			data |=((data >> i + 1) ^ (grayData >> i)) << i
		
		return data
		
	def GetAngle(self):
		count = self.GetCount()
		return int(360 * float(count - self.offset) / 255) * -1
		
	def GetDeg(self):
		count = self.GetCount()
		deg = int(360 * float(count - self.offset) / 255) * -1 + 7
		return deg

	def SetOffset(self):
		self.offset = self.GetCount()