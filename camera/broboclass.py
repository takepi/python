import absclass
import ConfigParser
import cv2
import numpy as np
from multiprocessing import Process, Queue
import poleclass
import RPi.GPIO as gpio
import smbus
import sys
import traceback
import time

cap = cv2.VideoCapture(0)
gpio.setmode(gpio.BOARD)
gpio.setup(21, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(19, gpio.IN, pull_up_down = gpio.PUD_UP)

class SendData(Process):
	def __init__(self, q):
		Process.__init__(self)
		self.daemon = True
		import controller
		bus = smbus.SMBus(1)
		flg = "notauto"
		bdata = 0
		gpio.output(21, False)
		gpio.output(23, False)
		
	def aircon(self):
		wait = 0.5
		for i in [21, 23]:
			for j in [True, False]:
				gpio.output(i, j)
				time.sleep(wait)
	
	def run(self):
		while True:
			if q.qsize() != 0:
				val = q.get()
				if val == "auto":
					flg = "auto"
				elif val == "notauto":
					flg = "notauto"
						
			if flg == "notauto":
				data = controller.read() << 4
				if data = 0xf0:
					self.aircon()
					data = 12
					
			elif flg == "auto":
				if q.qsize() == 0:
					data = bdata
				else:
					val = q.get()
					if val == "brake":
						data = 0
					elif val == "cw":
						data = 8
					elif val == "ccw":
						data = 4
					elif val == "fire":
						self.aircon()
						data = 12
					else:
						data = bdata
						
			try:
				bus.write_byte(0x08, data)
			except:
				pass
				
			bdata = data
			
class Limturret(Process):
	def __init__(self, abe, q_turret, q_debug):
		Process.__init__(self)
		self.daemon = True
		
	def run:
		while True:
			if 50 < abe.GetData() < 205:
				q_turret.put("brake")
				time.sleep(0.1)
				sys.exit("turret error")
			
class Debug(Process):
	def __init__(self, q):
		Process.__init__(self)
		self.daemon = True
		
	def run:
		while True:
			if q.qsize() != 0:
				for i in q.get():
					if type(i) == np.ndarray:
						cv2.imshow("img", i)
					else:
						print i
						
class Auto:
	def __init__(self, abe, pole, q_debug, q_turret, tcolor, polenum):
		swing = {1, 235, 2:0, 3:20}
		swing = swing[polenum]
		flg = 0
		nflg = 0
		q_turret.put("auto")
		
	def 