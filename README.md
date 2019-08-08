# CV-Project

## Objective
### We present an algorithm to recover 3D trajectory of a camera using feature based sparse slam using a single camera (also called MonoSLAM).     

##  Method of Approach
**1.** Feature extraction
We used the feature trackers present in the opencv library (goodFeaturestotrack and ORB feature tracker). 

**2.** Feature Matching
We calculate the distance between all the two points using brute force approach. We estimate the 2 nearest neighbour of every point using knn clustering and eliminate the points/pairs using ratio test. In the next step, we estimate the essential matrix using 8 point algorithm. For that we convert the image coordinates to camera cordinates and check for a minimum of 8 feature points. We eliminate the outliers using thresholding and ransac.       

**3.** Pose estimation
We estimate the pose of the current frame using the Essential matrix. See references[2].

**4** World coordinates
Provides the world coordinate by using 2 projection matrices as input using triangulation.

**5.1** Display2D 
We used pygame and openGL to display the feature points and their mappings across frames.

**5.2** Display3D
We use pangolin to display a 3D map of the camera poses and world coordinates of the feature points.

## Dataset
Driving stock video

## list of code dependencies
- [opencv](https://docs.opencv.org/3.4/d2/de6/tutorial_py_setup_in_ubuntu.html)
- [openGL](https://www.wikihow.com/Install-Mesa-(OpenGL)-on-Linux-Mint)
- [pygame](https://askubuntu.com/questions/399824/how-to-install-pygame)
- [pangolin](https://github.com/uoip/pangolin)
- [another link for pangolin, this has fewer modules](https://github.com/stevenlovegrove/Pangolin)
- [multiprocessing](https://stackoverflow.com/questions/43752560/install-multiprocessing-python3)
- [matplotlib](https://matplotlib.org/faq/installing_faq.html)
- [numpy](https://askubuntu.com/questions/868599/how-to-install-scipy-and-numpy-on-ubuntu-16-04)
- [skimage](https://scikit-image.org/docs/dev/install.html)

The code is in Python3

## Detailed instructions

### Installations
See the respective links in code dependencies

### Run
```
python3 main.py
```

## Results
### Feature point tracking
![2D](https://github.com/youknowwho-07/CV-Project/blob/master/2D.png)

### 3D map construction
![3D](https://github.com/youknowwho-07/CV-Project/blob/master/3D.png)

### Pose tracking
![pose](https://github.com/youknowwho-07/CV-Project/blob/master/pose.png)

## References
- A nice [gitgub repository](https://github.com/geohot/twitchslam) that has the implementation of monocular slam and a [youtube video](https://www.youtube.com/watch?v=7Hlb8YX2-W8&t=3022s&fbclid=IwAR03PKJjRhdYJNToQuG85p_t-NEvMCS-KuJ0ScR6q0I49SmKS40wzb48RIc) explaining the code by the same guy. 

- A [paper](http://www.maths.lth.se/matematiklth/personal/calle/datorseende13/notes/forelas6.pdf) describing the computation of rotation matrix and translation vector from Essential matrix.

- Nice paper by David G. Lowe on [Lowe's ratio test](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf)
