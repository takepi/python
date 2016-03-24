import pygame, time, math, threading, ConfigParser
import traceback, sys, os, serial, datetime, RPi.GPIO as gpio
from pygame.locals import *
import mechatechpy.pic as pic
import mechatechpy.mechatech as me
import mecanumclass

pic.I2C.write_word_data(0,1,0x0000)
pic.I2C.write_word_data(0,0,12345)

inifile = ConfigParser.SafeConfigParser()
inifile.read("config.ini")
mecanumlist = pic.xmlConfig(inifile.get("MDcon","config"))
absencoder = mecanumclass.AbsEncoder()

MD = [
mecanumlist["mecanum1"]["MD"]["RF"],
mecanumlist["mecanum1"]["MD"]["LF"],
mecanumlist["mecanum2"]["MD"]["RB"],
mecanumlist["mecanum2"]["MD"]["LB"]]

Mecanum = mecanumclass.Mecanum(MD)

ser = serial.Serial('/dev/ttyUSB0',115200)


led3 = 13

gpio.setmode(gpio.BOARD)
gpio.setup(led3,gpio.OUT)
gpio.output(led3,True)

pygame.joystick.init()
try:
	j = pygame.joystick.Joystick(0)
	j.init()
	print "Joystick name:" + j.get_name()
	print "button num:" + str(j.get_numbuttons())
	print j.get_numaxes()

except pygame.error:
	print "No joystick"

class EventDelTh(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)
	
	def run(self):
		while True:
			pygame.event.clear
			time.sleep(0.01)
	
class SendDataThread(threading.Thread):
	def __init__(self,rcounter,ledpic):
		threading.Thread.__init__(self)
		self.rcounter = rcounter
		self.ledpic = ledpic
		self.setDaemon(True)
		
	def run(self):
		self.rcounter.Limit(2000,1500)
		while 1:
			rvalues = int(self.rcounter.GetCount())
			
			mecanumlist["mecanum2"]["SM"]["SM1"].Angle(rvalues)
			mecanumlist["mecanum2"]["SM"]["SM2"].Angle(rvalues)

			angle = str(hex(absencoder.GetDeg()))
			angle = angle.replace("0x","")
			rpm = 1554 * (rvalues - 1500) / 500
			rpmh = hex(rpm).replace("0x","")
			ser.write(angle + "," + rpmh + "\n")
			time.sleep(0.1)
			
			speed = Mecanum.GetRatio()
			
			i = 5
			j = 1
			while 1:
				try:
					if j and i:
						j = 0
					else:
						break
					pic.I2C.write_word_data(self.ledpic,8,int(rpm))
					pic.I2C.write_word_data(self.ledpic,9,int(speed))
				except:
					i -= 1
					j = 1
				


class FireThread(threading.Thread):
	def __init__(self,IN,OUT,switch,MD):
		threading.Thread.__init__(self)
		self.inPin = IN
		self.outPin = OUT
		self.switchPin = switch
		self.MD = MD
		self.setDaemon(True)
		gpio.setup(IN,gpio.OUT)
		gpio.setup(OUT,gpio.OUT)
		gpio.setup(switch,gpio.IN,pull_up_down = gpio.PUD_UP)

	def run(self):
		while 1:
			fireflg = firecounter.GetCount()
			if fireflg == 1:
				while gpio.input(self.switchPin):
					self.MD.NorRot(200)
				self.MD.Free()
				time.sleep(0.01)
				self.MD.Brake(1023)
				gpio.output(self.inPin, False)
				time.sleep(0.5)
				gpio.output(self.outPin, True)
				time.sleep(0.5)
				gpio.output(self.outPin, False)
				time.sleep(0.5)
				gpio.output(self.inPin, True)
				time.sleep(0.5)
				gpio.output(self.inPin, False)
				firecounter.SetCount(2)

			elif fireflg == 3:
				
				while gpio.input(self.switchPin) == 0:
					self.MD.NorRot(200)
				while gpio.input(self.switchPin) == 1:
					self.MD.NorRot(200)
				self.MD.Free()
				time.sleep(0.01)
				self.MD.Brake(1023)
				firecounter.SetCount(0)
				time.sleep(0.5)

class AutoFocusThread(threading.Thread):
	def __init__(self,angleList, rollerList):
		threading.Thread.__init__(self)
		self.angleList = angleList
		self.rollerList = rollerList
		self.setDaemon(True)

	def auto(self,angle,roller):
		Deg = absencoder.GetDeg()
		rcounter.SetCount(roller)
		if Deg == angle:
			focusflg.SetCount(0)
		elif Deg < angle:
			mecanumlist["fire"]["MD"]["Angle"].NorRot(400)
		elif Deg > angle:
			mecanumlist["fire"]["MD"]["Angle"].RevRot(400)
			
	def run(self):
		while 1:
			Deg = absencoder.GetDeg()
			autofocusflg = focusflg.GetCount()
			if autofocusflg == 0:
				mecanumlist["fire"]["MD"]["Angle"].Free()
				
			elif autofocusflg == 1:
				mecanumlist["fire"]["MD"]["Angle"].RevRot(400)
				
			elif autofocusflg == 2:
				mecanumlist["fire"]["MD"]["Angle"].NorRot(400)
			
			elif autofocusflg == 3:
				self.auto(self.angleList[0],self.rollerList[0])

			elif autofocusflg == 4:
				self.auto(self.angleList[1],self.rollerList[1])
				
			elif autofocusflg == 5:
				self.auto(self.angleList[2],self.rollerList[2])
				
			elif autofocusflg == 6:
				self.auto(self.angleList[3],self.rollerList[3])

			elif autofocusflg == 7:
				self.auto(self.angleList[4],self.rollerList[4])

			elif autofocusflg == 8:
				if Deg > 10:
					mecanumlist["fire"]["MD"]["Angle"].RevRot(400)
					angle = absencoder.GetDeg()
				else:
					focusflg.SetCount(0)

def errwrite():
	f = open("HON50errfile.txt","w")
	f.write("err:%s\n"%(datetime.datetime.today()))
	f.write(traceback.format_exc(sys.exc_info()[2]))
	f.close()

def main():
	
	iniangle = ["angle1m","angle2m","angle3m","angle1mf","angle1mc"]
	iniroller = ["roller1m","roller2m","roller3m",
					"roller1mf","roller1mc"]
	angleConf = [0,0,0,0,0]
	rollerConf = [0,0,0,0,0]

	Mmspeed = int(inifile.get("Motor","mmspeed"))
	rollerupdown = int(inifile.get("Roller","updown"))
	rollerupdown = int(rollerupdown * 500 /1554)
	
	ledpic = int(inifile.get("LED","adr"))
	
	for i in range(5):
		angleConf[i] = int(inifile.get("Angle","%s" %iniangle[i]))
		rollerConf[i] = int(inifile.get("Roller","%s" %iniroller[i]))
		rollerConf[i] = int(rollerConf[i] * 500 / 1554 + 1500)

	pygame.init()
	
	threads = {}
	rcounter = me.Counter(1500.0)
	firecounter = me.Counter()
	focusflg = me.Counter()
	threads["counterth"] = me.CountThread(0.1,rcounter.CountDown)
	threads["eventDel"] = EventDelTh()
	#eventDel.start()

	piclist = [
	           mecanumlist["mecanum1"]["pic"],
	           mecanumlist["mecanum2"]["pic"],
	           mecanumlist["fire"]["pic"]]
	threads["syncTh"] = pic.SyncThread(piclist)
	#syncTh.start()

	threads["fireth"] = FireThread(21,23,19,mecanumlist["fire"]["MD"]["magazine"])
	threads["senddatath"] = SendDataThread(rcounter,ledpic)
	threads["autofocusth"] = AutoFocusThread(angleConf,rollerConf)
	"""
	counterth.start()
	senddatath.start()
	fireth.start()
	autofocusth.start()
	"""
	for i in threads:
		threads[i].start()
	Mecanum.SetMmspeed(Mmspeed)

	flg = 0
	stick = {0:0, 1:0, 2:-1 ,5:-1}

	while 1:
		for e in pygame.event.get():
			if e.type == QUIT:
				return
			if (e.type == KEYDOWN and e.key == K_ESCAPE):
				return

			if e.type == JOYAXISMOTION:
			
				if e.axis in [0,1,2,5]:
					stick[e.axis] = e.value
					for i in [0,1,2,5]:
						stick[i] = round(stick[i],4)
					
				if e.axis == 4:
					rcounter.SetStep((round(j.get_axis(4),1))*10)
					
			elif e.type == JOYHATMOTION:
				
				if j.get_hat(0) == (0,0):
					if focusflg.GetCount() == 1:
						focusflg.SetCount(0)
					elif focusflg.GetCount() == 2:
						focusflg.SetCount(0)
				
				elif j.get_hat(0) == (0,1):
					if flg:
						focusflg.SetCount(5)
					else:
						focusflg.SetCount(1)

				elif j.get_hat(0) == (0,-1):
					if flg:
						focusflg.SetCount(6)
					else:
						focusflg.SetCount(2)

				elif j.get_hat(0) == (1,0):
					if flg:
						focusflg.SetCount(3)
					else:
						r = rcounter.GetCount()
						r += rollerupdown
						rcounter.SetCount(r)
						
				elif j.get_hat(0) == (-1,0):
					if flg:
						focusflg.SetCount(4)
					else:
						r = rcounter.GetCount()
						r -= rollerupdown
						rcounter.SetCount(r)

			elif e.type == JOYBUTTONDOWN:

				if e.button == 0:
					focusflg.SetCount(8)
					rcounter.SetCount(1500.0)
					rcounter.SetStep(0.0)
					
				elif e.button == 1:
					Mecanum.SetMmspeed(1023)
					
				elif e.button == 2:
					gpio.output(21, False)
					time.sleep(0.5)
					gpio.output(23, True)
					time.sleep(0.5)
					gpio.output(23, False)
					time.sleep(0.5)
					gpio.output(21, True)
					time.sleep(0.5)
					gpio.output(21, False)
					
				elif e.button == 3:
					mecanumlist["fire"]["MD"]["magazine"].NorRot(200)
					
				elif e.button == 4:
					if flg:
						magazineflg = firecounter.GetCount()
						if magazineflg == 0:
							firecounter.SetCount(1)
						elif magazineflg == 2:
							firecounter.SetCount(3)
			
				elif e.button == 5:
					flg = 1
					
				elif e.button == 6:
					absencoder.SetOffset()
					
				elif e.button == 7:
					return 0

				elif e.button == 9:
					focusflg.SetCount(7)

				elif e.button == 10:
					rcounter.SetCount(1500.0)
					rcounter.SetStep(0.0)
					mecanumlist["mecanum1"]["SM"]["SM1"].Sync()
					mecanumlist["mecanum1"]["SM"]["SM2"].Sync()
					
			elif e.type == JOYBUTTONUP:
			
				if e.button == 1:
					Mecanum.SetMmspeed(Mmspeed)
					
				elif e.button == 3:
					mecanumlist["fire"]["MD"]["magazine"].Free()
					time.sleep(0.01)
					mecanumlist["fire"]["MD"]["magazine"].Brake(1023)
					
				elif e.button == 5:
					flg = 0

			else:
				pass
				
		Mecanum.MotorDrive(stick[0],stick[1],stick[2],stick[5])

if __name__ == "__main__":
	try:
		main()
	except:
		print "err"
		for i in range(3):
			gpio.output(led3,True)
			time.sleep(0.3)
			gpio.output(led3,False)
			time.sleep(0.3)
		errwrite()
		print traceback.format_exc(sys.exc_info()[2])
	finally:
		pic.I2C.write_word_data(0,1,0x0000)
		pic.I2C.write_word_data(0,0,12345)
		gpio.output(led3,False)
		ser.close()
		gpio.cleanup()
