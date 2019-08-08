import numpy as np 
import cv2
from helpers import *
from matplotlib import pyplot as plt
from skimage.measure import ransac
from skimage.transform import EssentialMatrixTransform

class Frame(object):
	"""docstring for Frame"""
	def __init__(self, frame):
		super(Frame, self).__init__()
		self.image = frame
		(self.X, self.Y, self.Z) = frame.shape
		self.KeyPts = None
		self.des = None
		self.pose = np.eye(4)

def getFeatures(frame):
	# Extract good features to track
	orb = cv2.ORB_create()

	frame_gray = cv2.cvtColor(frame.image, cv2.COLOR_BGR2GRAY)
	corners = cv2.goodFeaturesToTrack(frame_gray,maxCorners=2000,qualityLevel=0.01,minDistance=10)

	KeyPts = []
	for i in corners:
		u,v = i.ravel()
		KeyPts.append(cv2.KeyPoint(u,v, _size=20))
	
	frame.KeyPts, frame.des = orb.compute(frame.image, KeyPts) # extract descriptor
	return

# D_glob = []

def matchFeatures(F1, F2):
	# Match features
	bf = cv2.BFMatcher(cv2.NORM_HAMMING)
	matches = bf.knnMatch(F1.des,F2.des, k=2)
	
	# filter matches by lowe's ratio test
	temp_matches = []
	for m,n in matches:
		if m.distance < 0.75*n.distance and m.distance < 32:
			temp_matches.append(m)

	pt1 = []
	pt2 = []
	good_matches = []
	for m in temp_matches:
		if m.queryIdx not in pt1 and m.trainIdx not in pt2:
			pt1.append(m.queryIdx)
			pt2.append(m.trainIdx)
			good_matches.append([F1.KeyPts[m.queryIdx].pt,F2.KeyPts[m.trainIdx].pt])

	#presence of atleast 8 points for 8 point algorithm
	assert(len(good_matches) >= 8)

	pt1 = np.array(pt1)
	pt2 = np.array(pt2)

	good_matches = np.array(good_matches)

	# Transform to camera coordinates for essential matrix calculation
	tx_matches = transform_coordinates(good_matches)

	# Calculate essential matrix and inliers
	model, inliers = ransac((tx_matches[:, 0], tx_matches[:, 1]),
                          	EssentialMatrixTransform,
                          	min_samples=8,
                          	residual_threshold=0.05,
							max_trials=100)

	pose = Pose(model.params) 	# calculate relative pose
	
	# # Code useful for computing Camera intrinsics
	# print pose
	# U,D,V = np.linalg.svd(model.params)

	# print 'U = ',np.linalg.norm(U)
	# print 'D = ',D
	# print 'V = ',np.linalg.norm(V), '\n'
	# D_glob.append(D)
	# D_med = np.median(D_glob,0)
	# print [D[0],D[1]], '\t', [D_med[0], D_med[1]]
	return np.array(tx_matches[inliers,0]), np.array(tx_matches[inliers,1]), pose, good_matches[inliers], len(good_matches)