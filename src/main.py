import numpy as np 
import cv2
from matplotlib import pyplot as plt
import pygame
from frame import *
from constants import *
from Display2D import *
from Display3D import *
import sys

# initialising displays
f2d = dim2display()
f3d = dim3display()

# pygame.init()
# screen = pygame.display.set_mode([W,H])
# capture video	
cap = cv2.VideoCapture('../drive2.mp4')  
s = 1

allworldCoords = []
current_frames = []
while cap.isOpened():
	
	ret, frame = cap.read()
	if (ret == False):
		break

	frame = cv2.resize(frame, (W, H))	
	frame = Frame(frame)
	current_frames.append(frame)	#list of all frames

	getFeatures(frame)	# Extract features from image

	if len(current_frames) > 1:
		# match features from the previous frame
		features1, features2, pose, matches, numMatched = matchFeatures(current_frames[-1], current_frames[-2])
		
		# propogate pose from the initial frame
		current_frames[-1].pose = np.matmul(pose, current_frames[-2].pose)
		
		# get 3D world coordinates
		worldCoords = cv2.triangulatePoints(I44[:3], pose[:3], features1.T, features2.T)

		#Filter World coordinates 
		worldCoords = np.array(worldCoords[:,(np.abs(worldCoords[3,:]) > 0.0005) & (worldCoords[2,:] > 0)])

		if worldCoords.shape[1] > 0:
			worldCoords /= worldCoords[3,:]
			allworldCoords.append(worldCoords.T)

		# Display 2D points and 3D Map
		f3d.dispAdd(current_frames, allworldCoords)
		f2d.display2D(frame.image, matches)

		print(current_frames[-1].pose)

		if worldCoords.shape[1] > 0:
			print(worldCoords[:,0])