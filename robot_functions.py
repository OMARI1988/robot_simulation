from visual import *
from shapefile import *
from Polygon import *
import numpy as np
# http://www.anninaruest.com/pie/2014/07/inverse-kinematics-and-the-m100rak/

class Robot():
	def __init__(self):
		self.chess_shift_x = 8
		self.chess_shift_y = 6

		self.len_arm1 = 8
		self.len_arm2 = 6
		self.len_gripper = 2
		self.len_base = 2

		self.draw_robot()
		self.rotate_robot(0,-3*np.pi/4,3*np.pi/4)

	def rotate_robot(self,a0,a1,a2):

		self.rotate_joint(self.base_faces,self.base_faces_origin,(0,self.chess_shift_y,0),a0,0,0)
		self.rotate_joint(self.arm1_faces,self.arm1_faces_origin,(0,self.chess_shift_y,self.len_base),a0,a1,0)
		self.rotate_joint(self.arm2_faces,self.arm2_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),a0,a1,a2)
		self.rotate_joint(self.gripper1_faces,self.gripper1_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),a0,a1,a2)
		self.rotate_joint(self.gripper2_faces,self.gripper2_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),a0,a1,a2)

	def rotate_joint(self,obj,faces,shift,a0,a1,a2):
		for j,v in enumerate(faces):
			v1 = v - shift
			v2 = rotate(v1, angle=a2, axis=(0,1,0)) + (shift[0],0,0)
			v2 = rotate(v2, angle=a1, axis=(0,1,0)) 
			v2 = rotate(v2, angle=a0, axis=(0,0,1)) + (0,shift[1],shift[2])
			obj.pos[j] = v2
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
	def draw_robot(self):

		base_1 = box(pos=(0,self.chess_shift_y,-.25),axis=(0,0,1), size=(.5,2,2),color=color.black, material=materials.plastic)
		base_2 = Polygon( [(-1,0), (-.75,self.len_base), (.75,self.len_base), (1,0)] )
		base_3 = shapes.circle(pos=(0,self.len_base), radius=.75)
		base_4 = shapes.circle(pos=(0,self.len_base), radius=0.2)
		base_s = [(0,self.chess_shift_y-.5,0),(0,self.chess_shift_y+.5,0)]
		self.base = extrusion(pos=base_s, shape=base_2+base_3-base_4, color=color.red)

		arm1_1 = Polygon( [(0,.75), (self.len_arm1,.5), (self.len_arm1,-.5), (0,-.75)] )
		arm1_2 = shapes.circle(pos=(0,0), radius=.75)
		arm1_3 = shapes.circle(pos=(0,0), radius=0.2)
		arm1_4 = shapes.circle(pos=(self.len_arm1,0), radius=.5)
		arm1_5 = shapes.circle(pos=(self.len_arm1,0), radius=0.2)
		arm1_s = [(0,self.chess_shift_y+.5,self.len_base),(0,self.chess_shift_y+1.5,self.len_base)]
		self.arm1 = extrusion(pos=arm1_s, shape=arm1_1+arm1_2-arm1_3+arm1_4-arm1_5, color=color.blue)

		arm2_1 = Polygon( [(0,.5), (self.len_arm2,.4), (self.len_arm2,-.4), (0,-.5)] )
		arm2_2 = shapes.circle(pos=(0,0), radius=.5)
		arm2_3 = shapes.circle(pos=(0,0), radius=0.2)
		arm2_4 = shapes.circle(pos=(self.len_arm2,0), radius=.4)
		arm2_5 = shapes.circle(pos=(self.len_arm2,0), radius=0.2)
		arm2_s = [(self.len_arm1,self.chess_shift_y-.5,self.len_base),(self.len_arm1,self.chess_shift_y+.5,self.len_base)]
		self.arm2 = extrusion(pos=arm2_s, shape=arm2_1+arm2_2-arm2_3+arm2_4-arm2_5, color=color.red)

		gripper_1 = Polygon( [(0,.4), (self.len_gripper,.3), (self.len_gripper,-.3), (0,-.4)] )
		gripper_2 = shapes.circle(pos=(0,0), radius=.4)
		gripper_4 = shapes.circle(pos=(self.len_gripper,0), radius=.3)
		gripper1_s = [(self.len_arm1+self.len_arm2,self.chess_shift_y-.6,self.len_base),(self.len_arm1+self.len_arm2,self.chess_shift_y-.5,self.len_base)]
		gripper2_s = [(self.len_arm1+self.len_arm2,self.chess_shift_y+.5,self.len_base),(self.len_arm1+self.len_arm2,self.chess_shift_y+.6,self.len_base)]

		self.gripper1 = extrusion(pos=gripper1_s, shape=gripper_1+gripper_2+gripper_4, color=color.green)
		self.gripper2 = extrusion(pos=gripper2_s, shape=gripper_1+gripper_2+gripper_4, color=color.green)

		self.base_faces = self.base.create_faces()
		self.arm1_faces = self.arm1.create_faces()
		self.arm2_faces = self.arm2.create_faces()
		self.gripper1_faces = self.gripper1.create_faces()
		self.gripper2_faces = self.gripper2.create_faces()

		self.base_faces_origin = self.base_faces.pos.copy()
		self.arm1_faces_origin = self.arm1_faces.pos.copy()
		self.arm2_faces_origin = self.arm2_faces.pos.copy()
		self.gripper1_faces_origin = self.gripper1_faces.pos.copy()
		self.gripper2_faces_origin = self.gripper2_faces.pos.copy()



