import numpy as np
import visual as vp
# http://www.anninaruest.com/pie/2014/07/inverse-kinematics-and-the-m100rak/

#----------------------------------------------------------------------------------#
# input: coordinates x,y,z of the target point, lengths l1,l2,l3 of the arms, were
# l1 is the base height
# l2 is the length of the first arm
# l3 is the length of the second arm
#			
#	     /\
#	l2  /  \  l3
#	   /	\
#	  #
#      l1 #
#       #####
#
# output: angles a1,a2,a3 of the joints, in radians
def inverse_kinematics(x,y,z,l1,l2,l3):
	# used in case arm can't reach that location
	s  = "(%g,%g,%g) is out of range." % tuple(np.around([x,y,z],2))
	# compute the first angle
	a1 = np.arctan2(y,x)
	# compute the thirs angle
	r  = np.hypot(x,y)
	z -= l1
	u3 = ( r**2 + z**2 - l2**2 - l3**2 ) / ( 2*l2*l3 )
	if abs(u3)>1:    raise Exception(s)
	a3 = -np.arccos(u3)
	# compute the second angle
	v  = l2 + l3*u3
	w  = -l3 * np.sqrt(1-u3**2)  # this is sin(a3)>0 assuming 0<a3<pi
	a2 = np.arctan2(v*z-w*r,v*r+w*z)
	if a2<0 or a2>np.pi:    raise Exception(s)
	return a1,a2,a3

#----------------------------------------------------------------------------------#
def draw_robot(x,y,z,l1,l2,l3):
	# first draw x,y,z axes
	p0 = 10*array([-1,-1,0])
	#for e in ex,ey,ez:	vp.arrow(pos=p0,axis=5*e,shaftwidth=0.5,color=e)
	a1,a2,a3,a4 = invert(x,y,z,l2,l3,l4)                  # compute joint angles
	u2,u3,u4 = arms(a1,a2,a3,a4,l2,l3,l4)                    # compute arm vectors
	w = 0.2                                          # arm radius and base thickness
	u0 = w*ez 
	v0 = cos(a1)*ex + sin(a1)*ey                     # "front" direction
	r = 3                                            # radius of the base
	vp.cylinder(pos=-u0,axis=2*u0,radius=r)         # draw base
	vp.cylinder(pos=-u0+0.8*r*v0,axis=2*u0,radius=0.1*r,color=(0.5,0.5,0.5)) # draw grey circle that indicates base direction
	vp.cylinder(pos=(0,0,0),axis=u2,radius=w,color=(0.7,1,0.7)) # draw arm 2
	vp.sphere(pos=u2,radius=w)                                  # draw joint 2
	vp.cylinder(pos=u2,axis=u3,radius=w,color=(0.7,0.7,1))      # draw arm 3
	vp.sphere(pos=u2+u3,radius=w)                               # draw joint 3
	vp.cylinder(pos=u2+u3,axis=u4,radius=w,color=(0.7,0.7,1))   # draw arm 4
	vp.sphere(pos=u2+u3+u4,radius=2*w,color=(0,1,0))            # draw end of arm 4
	vp.sphere(pos=(x,y,z),radius=2*w,color=(1,0,0))             # draw target point
	#the last two lines are doing the same but are there for debugging 
