eimport pygame                                     #pygame�Ƃ������W���[�����C���|�[�g
from pygame.locals import *                       #��������
SCREEN_WIDTH = 640                                #640*480�̃E�C���h�E
SCREEN_HEIGHT = 480

pygame.joystick.init()                            #���W���[����������

try:                                              #�G���[�΍�̂��
	j = pygame.joystick.Joystick(0)               #j���R���g���[���[
	j.init()                                      #������
	print "Joystick name:" + j.get_name()         #�W���C�X�e�b�N�̖�
	print "button num:" + str(j.get_numbuttons()) #�W���C�X�e�b�N�̃{�^�����擾
	
except pygame.error:                              #�W���C�X�e�b�N���擾�ł��Ȃ�������\��
	print "No joystick"

def main():
	pygame.init()                                 #pygame��������
#	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#	pygame.display.set_caption("joystick")        #�X�N���[���̊֌W
#	pygame.display.flip()
	
	while 1:
		for e in pygame.event.get():              #�ϐ�e�ɃC�x���g�L���[�ɂ���W���C�X�e�B�N�̏���������
			if e.type == QUIT:                    #QUIT(?)�Ȃ炨���
				return
			if (e.type == KEYDOWN and e.key == K_ESCAPE):
				return                            #KEYDOWN(?),K_ESCAPE(?)�Ȃ炨���
			
			if e.type == pygame.locals.JOYAXISMOTION:
				x, y = j.get_axis(0), j.get_axis(1)
				print "x and y:" + str(x) + ", " + str(y)
				                                  #JOYAXISMOTION(�W���C�X�e�B�b�N)�̂Ƃ�x����y���̒l���v�����g
			elif e.type == pygame.locals.JOYBALLMOTION:	
				print "ball motion"
				                                  #JOYBALLMOTION(�{�[���Ȃ�����...)�̂Ƃ��{�[���̏󋵂��v�����g
			elif e.type == pygame.locals.JOYHATMOTION:
				print "hat motion"
				                                  #JOYHATMOTION(�\���L�[)�̏󋵂��v�����g
			elif e.type == pygame.locals.JOYBUTTONDOWN:
				print "push button NO." + str(e.button)
				                                  #JOYBUTTONDOWN�i�{�^��)�����ꂽ�{�^�����v�����g
			elif e.type == pygame.locals.JOYBUTTONUP:
				print "release button NO." + str(e.button)
				                                  #JOYBUTTONUP(�{�^��)�b���ꂽ�{�^�����v�����g

if __name__ == "__main__":                        #�ق��̃v���O�����ł����̃v���O�������̊֐��A�ϐ����g�����߂ɂ���
	main()
