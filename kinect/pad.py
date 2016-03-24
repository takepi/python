eimport pygame                                     #pygameというモジュールをインポート
from pygame.locals import *                       #こっから
SCREEN_WIDTH = 640                                #640*480のウインドウ
SCREEN_HEIGHT = 480

pygame.joystick.init()                            #モジュールを初期化

try:                                              #エラー対策のやつ
	j = pygame.joystick.Joystick(0)               #jがコントローラー
	j.init()                                      #初期化
	print "Joystick name:" + j.get_name()         #ジョイステックの名
	print "button num:" + str(j.get_numbuttons()) #ジョイステックのボタンを取得
	
except pygame.error:                              #ジョイステックを取得できなかったら表示
	print "No joystick"

def main():
	pygame.init()                                 #pygameを初期化
#	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#	pygame.display.set_caption("joystick")        #スクリーンの関係
#	pygame.display.flip()
	
	while 1:
		for e in pygame.event.get():              #変数eにイベントキューにあるジョイスティクの情報を代入する
			if e.type == QUIT:                    #QUIT(?)ならおわり
				return
			if (e.type == KEYDOWN and e.key == K_ESCAPE):
				return                            #KEYDOWN(?),K_ESCAPE(?)ならおわり
			
			if e.type == pygame.locals.JOYAXISMOTION:
				x, y = j.get_axis(0), j.get_axis(1)
				print "x and y:" + str(x) + ", " + str(y)
				                                  #JOYAXISMOTION(ジョイスティック)のときx軸とy軸の値をプリント
			elif e.type == pygame.locals.JOYBALLMOTION:	
				print "ball motion"
				                                  #JOYBALLMOTION(ボールないけど...)のときボールの状況をプリント
			elif e.type == pygame.locals.JOYHATMOTION:
				print "hat motion"
				                                  #JOYHATMOTION(十字キー)の状況をプリント
			elif e.type == pygame.locals.JOYBUTTONDOWN:
				print "push button NO." + str(e.button)
				                                  #JOYBUTTONDOWN（ボタン)押されたボタンをプリント
			elif e.type == pygame.locals.JOYBUTTONUP:
				print "release button NO." + str(e.button)
				                                  #JOYBUTTONUP(ボタン)話されたボタンをプリント

if __name__ == "__main__":                        #ほかのプログラムでもこのプログラム内の関数、変数を使うためにある
	main()
