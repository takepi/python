import serial
import threading
import time
from xbee import XBee,ieee

class Controller(threading.Thread):
	def __init__(self, dev, timeout = 3):
		super(Controller, self).__init__()
		self.setDaemon(True)
		ser = serial.Serial(dev, 57600)
		self.xbee = XBee(ser)
		self.lock = threading.Lock()
		self.timeout = timeout
		self.recv_time = 0
		self.recv_key = 0
	
	def run(self):
		while 1:
			recv_data = self.xbee.wait_read_frame()
			
			if not recv_data:
				print "Controller : Error = Not Receive"
				time.sleep()
				continue

			if recv_data["id"] == "rx_io_data":
				if (recv_data["samples"][0].has_key("dio-0") and
				    recv_data["samples"][0].has_key("dio-1") and
				    recv_data["samples"][0].has_key("dio-2") and
					recv_data["samples"][0].has_key("dio-3")):
					recv_key = 0x00
					if not recv_data["samples"][0]["dio-0"]:
						recv_key |= 0x01
					if not recv_data["samples"][0]["dio-1"]:
						recv_key |= 0x02
					if not recv_data["samples"][0]["dio-2"]:
						recv_key |= 0x04
					if not recv_data["samples"][0]["dio-3"]:
						recv_key |= 0x08
			
					with self.lock:
						self.recv_key = recv_key
						self.recv_time = time.time()
			
			else:
				print "Controller : Error = Wrong Packet"
				continue

	def get_key(self):
		with self.lock:
			recv_key = self.recv_key
			recv_time = self.recv_time

		if (time.time() - recv_time) > self.timeout:
			return 0x00

		return recv_key

ctrl = Controller("/dev/XBee",0.5)
ctrl.start()

def read():
	return ctrl.get_key()

