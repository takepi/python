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

def sendData(q):
	import controller
	bus = smbus.SMBus(1)
	while True:
		cdata = controller.read() << 4

		if q.empty():
			data = cdata
		else:
			if q.get() == "cw":
				print "cw"
				data = cdata | 2
			elif q.get() == "ccw":
				print "ccw"
				data = cdata | 1
			elif q.get() == "fire":
				data = cdata | 3
			else:
				print "stop"
				data = cdata
		
		debug(data = bin(data))
		bus.write_byte(0x08, cdata)

def debug(q):
	while True:
		if q.qsize() != 0:
			for i in q.get():
				if type(i) == np.ndarray:
					cv2.imshow("img", i)
				else:
					pass
					print i

def autoFire(abe, pole, q_debug, teamcolor, polenum):
	swing = {1:235, 2:0, 3:20}
	bcolor = None
	flg = 0
	nflg = 0
	swing = swing[polenum]

	while abe.GetData() != swing:
		q_debug.put([abe.GetData()])
		#q_turret.put("cw")

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
								#q_turret.put("cw")
							else:
								q_debug.put(["ccw", abe.GetData(), swing + zure])
								#q_turret.put("ccw")
						q_debug.put(["turret ok"])
						#q_turret.put("fire")
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
	gpio.setmode(gpio.BOARD)
	gpio.setup(19, gpio.IN, pull_up_down = gpio.PUD_UP)

	inifile = ConfigParser.SafeConfigParser()
	inifile.read("polecolor.ini")
	teamcolor = str(inifile.get("team", "color"))

	abe = absclass.AbsEncoder()

	pole = poleclass.Pole("polecolor.ini")
	q_turret = Queue(maxsize = 1)
	q_debug = Queue(maxsize = 5)

	p_send = Process(target = sendData, args = (q_turret, ))
	p_debug = Process(target = debug, args = (q_debug, ))
	p_send.daemon = True
	p_debug.daemon = True
	p_debug.start()
	#p_send.start()

	while gpio.input(19):
		q_debug.put(["not auto"])

	abe.SetOffset()
	for i in range(3, 0, -1):
		autoFire(abe, pole, q_debug, teamcolor, i)
		time.sleep(5)

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
		print "End"
