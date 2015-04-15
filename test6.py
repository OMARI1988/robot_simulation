from visual import *
from shapefile import *
from Polygon import *
import numpy as np
import wx
from robot_functions import *
from scene_functions import *

c = (1,1,0)
c2 = color.rgb_to_hsv(c)	# convert RGB to HSV
print(c2)	# (0.16667, 1, 1)
c3 = color.hsv_to_rgb(c2)	# convert back to RGB
print(c3)	# (1, 1, 0)



len_arm1 = 8
len_arm2 = 6
len_gripper = 2
len_base = 2

S = Scene()
R = Robot()
print R.len_base

"""
for i in range(30):
	rate(10000)
	a0 = -i*np.pi/180.0
	a1 = -i*np.pi/180.0
	a2 = -i*np.pi/180.0
	R.rotate_robot(a0,a1,a2)

"""
