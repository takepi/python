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
			
class LimTurret(Process):
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
	def __init__(self, abe, pole, q_debug, q_turret, tcolor):
		swing = {1, 235, 2:0, 3:20}
		
	def fire(self, polenum):
		flg = 0
		nflg = 0
		swing = swing[polenum]
		
		if swing >= 128:
			turret = ["ccw", "cw"]
		else:
			turret = ["cw", "ccw"]
			
		while abe.GetData() != swing:
			q_debug.put([abe.GetData()])
			if abe.GetData() < swing:
				q_debug.put([turret[0])
				q_turret.put(turret[0])
			elif abe.GetData() > swing:
				q_debug.put([turret[1])
				q_turret.put(turret[1])
				
		q_turret.put("brake")
		
		while True:
			ret, frame = cap.read()
			img, point, color, area = pole.getPole("a", frame)

			if color != None:
				q_debug.put(["color good", flg, color])
				if bcolor == color:
					flg = flg + 1
					if flg > 20:
						if teamcolor == bcolor:
							zure = (point[0][0] - img.shape[1]/2 - 20)/16
							while abe.GetData() != swing + zure:
								if abe.GetData() - (swing + zure) < 0:
									q_debug.put(["cw", abe.GetData(), swing + zure])
									q_turret.put("cw")
								else:
									q_debug.put(["ccw", abe.GetData(), swing + zure])
									q_turret.put("ccw")
							q_turret.put("brake")
							q_debug.put(["turret ok"])
							q_turret.put("fire")
							break
						else:
							q_turret.put("brake")
							q_debug.put(["turret no"])
							break
				else:
					bcolor = color
			else:
				if nflg > 50:
					break
				q_debug.put(["None", nflg])
				nflg = nflg + 1
				
def main():
	inifile = ConfigParser.SafeConfigParser()
	inifile.read("polecolor.ini")
	teamcolor = str(inifile.get("team", "color"))

	abe = absclass.AbsEncoder()
	abe.SetOffset()

	pole = poleclass.Pole("polecolor.ini")
	q_turret = Queue(maxsize = 1)
	q_debug = Queue(maxsize = 5)
	
	p_send = SendData(q_turret)
	p_limturret = LimTurret(abe, q_turret, q_debug)
	p_debug = Debug(q_debug)
	auto = Auto(abe, pole, q_debug, q_turret, teamcolor)
	
	p_send.start()
	p_limturret.start()
	p_debug.start()
	
	while True:
		while gpio.input(19):
			pass
			
		q_turret.put("auto")
		for i in [3, 2, 1, 3, 2, 1]:
			auto.fire(i)
			time.sleep(5)
		
		q_turret.put("notauto")
		
		while not gpio.input(19):
			q_debug.put(["back please"])
			
if __name__ == "__main__":
	try:
		main()
	except:
		print "!-----------error------------!"
		print traceback.format_exc(sys.exc_info()[2])
		print "!----------------------------!"
	finally:
		cap.release()
		cv2.destroyAllWindows()
		gpio.cleanup()
