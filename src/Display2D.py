import pygame
from constants import *
import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *



class dim2display:

	def __init__(self):	# initialise window
		pygame.init()
		self.screen = pygame.display.set_mode([W,H])
		
	def display2D(self, image, matches):

		# create surface
		f = np.rot90(image)
		disp = pygame.surfarray.make_surface(f)
		disp = pygame.transform.flip(disp, True, False)
		
		# add points to the window
		for pt1, pt2 in matches:
			u1,v1 = map(lambda x: int(round(x)), pt1)
			u2,v2 = map(lambda x: int(round(x)), pt2)

			pygame.draw.circle(disp,(255,0,0),(u1,v1),2)
			pygame.draw.line(disp,(0,0,255),(u1,v1),(u2,v2),2)

		# display window
		self.screen.blit(disp, (0,0))
		pygame.display.update()
		pygame.display.flip()
	
		cv2.waitKey(10)

		return

	

		
	