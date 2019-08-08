import numpy as np 
import cv2
from matplotlib import pyplot as plt
from constants import *

def Pose(Essential_matrix):	
	# Rotation matrix
	W = np.array([[0,-1,0],[1,0,0],[0,0,1]])

	U, sigma, V = np.linalg.svd(Essential_matrix)

	# making det(U*V.T) positive
	if np.linalg.det(U) < 0:
		U *= -1.0
	if np.linalg.det(V) < 0:
		V *= -1.0

	# Final rotation matrix	
	R1 = np.matmul(U,np.matmul(W,V))

	if(np.trace(R1) < 0):
		R1 = np.matmul(U, np.matmul(W.T,V))

	# Translation matrix
	u_last_col = U[:,2]
	if(u_last_col[2] < 0):
		u_last_col = -1 * u_last_col

	pose = np.eye(4)
	pose[:3,:3] = R1
	pose[:3,3] = u_last_col

	return pose

def transform_coordinates(pt):	#Transform to camera coordinates
	ret = []
	for i in range(0, len(pt)):	
		x1 = np.array([pt[i,0,0], pt[i,0,1], 1])
		x2 = np.array([pt[i,1,0], pt[i,1,1], 1])
		x1 = np.matmul(Kinv, x1.T).T
		x2 = np.matmul(Kinv, x2.T).T
		point = [x1[:2], x2[:2]] 
		ret.append(point)

	ret = np.array(ret)
	return ret