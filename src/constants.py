import numpy as np
F= 135 # focal length
W = 500 # image width
H = 500 # image height

I44 = np.eye(4) # initial camera orientation. overall ambiguity
K = np.array([[F, 0, W//2], [0, F, H//2], [0, 0, 1]], dtype=float) # camera intrinsic matrix
Kinv = np.linalg.inv(K)