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

def sendData(q):
	import controller
	bus = smbus.SMBus(1)
	gpio.setup(21, gpio.OUT)
	gpio.setup(23, gpio.OUT)
	gpio.output(21, False)
	gpio.output(23, False)

	while True:
		data = controller.read() << 4

		if q.empty():
			try:
				bus.write_byte(0x08, data)
			except:
				print "uwaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
		else:
			if q.get() == "cw":
				#print "cw"
				data = 8
			elif q.get() == "ccw":
				#print "ccw"
				data = 4
			elif q.get() == "fire":
				gpio.output(21, True)
				time.sleep(0.5)
				gpio.output(21, False)
				time.sleep(0.5)
				gpio.output(23, True)
				time.sleep(0.5)
				gpio.output(23, False)
				time.sleep(0.5)
				data = 12
			else:
				#print "stop"
				pass
		
		#print bin(data)
			try:
				bus.write_byte(0x08, data)
			except:
				print "uwaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

def debug(q):
	while True:
		if q.qsize() != 0:
			for i in q.get():
				if type(i) == np.ndarray:
					cv2.imshow("img", i)
				else:
					pass
					print i

def autoFire(abe, pole, q_debug,q_turret, teamcolor, polenum):
	swing = {1:235, 2:0, 3:20}
	bcolor = None
	flg = 0
	nflg = 0
	swing = swing[polenum]

	while abe.GetData() != swing:
		q_debug.put([abe.GetData()])
		if abe.GetData() < swing:
			q_debug.put(["ccw"])
			q_turret.put("ccw")
		elif abe.GetData() > swing:
			q_debug.put(["ccw"])
			q_turret.put("ccw")

	while True:
		ret, frame = cap.read()
		img, point, color, area = pole.getPole("a", frame)

		if color != None:
			q_debug.put(["color good", flg, color])
			if bcolor == color:
				flg = flg + 1
				if flg > 20:
					if teamcolor == bcolor:
						zure = (point[0][0] - img.shape[1]/2)/16
						while abe.GetData() != swing + zure:
							if zure > 0:
								q_debug.put(["cw", abe.GetData(), swing + zure])
								q_turret.put("cw")
							else:
								q_debug.put(["ccw", abe.GetData(), swing + zure])
								q_turret.put("ccw")
						q_debug.put(["turret ok"])
						q_turret.put("fire")
						time.sleep(5)
						break
					else:
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
	gpio.setup(19, gpio.IN, pull_up_down = gpio.PUD_UP)

	inifile = ConfigParser.SafeConfigParser()
	inifile.read("polecolor.ini")
	teamcolor = str(inifile.get("team", "color"))

	abe = absclass.AbsEncoder()
	abe.SetOffset()

	pole = poleclass.Pole("polecolor.ini")
	q_turret = Queue(maxsize = 1)
	q_debug = Queue(maxsize = 5)

	p_send = Process(target = sendData, args = (q_turret, ))
	p_debug = Process(target = debug, args = (q_debug, ))
	p_send.daemon = True
	p_debug.daemon = True
	p_debug.start()
	p_send.start()

	while True:
		while gpio.input(19):
			pass
			#q_debug.put(["not auto"])

		for i in range(2):
			for i in range(3, 0, -1):
				autoFire(abe, pole, q_debug, q_turret, teamcolor, i)
				time.sleep(5)

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
