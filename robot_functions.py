from visual import *
from shapefile import *
from Polygon import *
import numpy as np
import wx

# http://www.anninaruest.com/pie/2014/07/inverse-kinematics-and-the-m100rak/

class Robot():
	def __init__(self):
		self.chess_shift_x = 8
		self.chess_shift_y = 6

		self.len_arm1 = 8
		self.len_arm2 = 6
		self.len_gripper = 2
		self.len_base = 2

		self.l1 = 0
		self.l2 = self.len_arm1
		self.l3 = self.len_arm2 + self.len_gripper

		self.a0 = 0
		self.a1 = 0
		self.a2 = 0

		self.step = 30
		self.frame_number = 1

		self.draw_scene()
		self.draw_robot()
		self.rotate_robot_init(0,-3*np.pi/4,3*np.pi/4)

		self.chess_map = {}
		self.box_count = 1
		self.box = {}
		self.sphere_count = 1
		self.sphere = {}
		self.cylinder_count = 1
		self.cylinder = {}
		self.pyramid_count = 1
		self.pyramid = {}


	def draw_scene(self):
		self.display = display(title='Baby Robot',
			x=0, y=0, width=600, height=600,
			center=(self.chess_shift_x,self.chess_shift_y,0),
			forward=(self.chess_shift_x-10,self.chess_shift_y,-7),
			background=(1,1,1))

		checkerboard = ( (0,1,0,1,0,1,0,1), 
				 (1,0,1,0,1,0,1,0),
				 (0,1,0,1,0,1,0,1),
				 (1,0,1,0,1,0,1,0),
		 		 (0,1,0,1,0,1,0,1), 
				 (1,0,1,0,1,0,1,0),
				 (0,1,0,1,0,1,0,1),
				 (1,0,1,0,1,0,1,0) )
		tex = materials.texture(data=checkerboard,
				     mapping="sign",
				     interpolate=False)
		chess1 = box(pos=(self.chess_shift_x,self.chess_shift_y,-.3),axis=(0,0,1),size=(.4,9,9),color=color.orange,material=materials.wood)
		chess2 = box(pos=(self.chess_shift_x,self.chess_shift_y,-.25),axis=(0,0,1), size=(.5,8,8),color=color.orange, material=tex)


		x = arrow(pos=(0,0,0),axis=(1,0,0),length=2,shaftwidth=.2,color=color.red)
		y = arrow(pos=(0,0,0),axis=(0,1,0),length=2,shaftwidth=.2,color=color.green)
		z = arrow(pos=(0,0,0),axis=(0,0,1),length=2,shaftwidth=.2,color=color.blue)

	def _box(self,x,y,c):
		z = self.add_to_chess_map('box',x,y)
		self.box[self.box_count] = box(pos=(4.5+x,2.5+y,.4+z),axis=(0,0,1),size=(.8,.8,.8),color=c,material=materials.plastic)
		self.box_count+=1

	def _cylinder(self,x,y,c):
		z = self.add_to_chess_map('cylinder',x,y)
		self.cylinder[self.cylinder_count] = cylinder(pos=(4.5+x,2.5+y,z),axis=(0,0,.8),radius=.4,color=c,material=materials.plastic)
		self.cylinder_count+=1

	def _sphere(self,x,y,c):
		z = self.add_to_chess_map('sphere',x,y)
		self.sphere[self.sphere_count] = sphere(pos=(4.5+x,2.5+y,.4+z),radius=.4,color=c,material=materials.plastic)
		self.sphere_count+=1

	def _pyramid(self,x,y,c):
		z = self.add_to_chess_map('pyramid',x,y)
		self.pyramid[self.pyramid_count] = pyramid(pos=(4.5+x,2.5+y,z),axis=(0,0,1),size=(.8,.8,.8),color=c,material=materials.plastic)
		self.pyramid_count+=1

	def add_to_chess_map(self,n,x,y):
		if (x,y) not in self.chess_map:
			self.chess_map[(x,y)] = [n]
		else:
			self.chess_map[(x,y)].append([n])
		print self.chess_map
		return (len(self.chess_map[(x,y)])-1)*.8


	def rotate_robot(self,a0,a1,a2):
		p0 = np.linspace(self.a0,a0,self.step) # path 0
		p1 = np.linspace(self.a1,a1,self.step)
		p2 = np.linspace(self.a2,a2,self.step)
		for i in range(self.step):
			rate(10000)
			self.rotate_joint(self.base_faces,self.base_faces_origin,(0,self.chess_shift_y,0),p0[i],0,0)
			self.rotate_joint(self.arm1_faces,self.arm1_faces_origin,(0,self.chess_shift_y,self.len_base),p0[i],p1[i],0)
			self.rotate_joint(self.arm2_faces,self.arm2_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),p0[i],p1[i],p2[i])
			self.rotate_joint(self.gripper1_faces,self.gripper1_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),p0[i],p1[i],p2[i])
			self.rotate_joint(self.gripper2_faces,self.gripper2_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),p0[i],p1[i],p2[i])
			self.saveSnapshot()
		self.a0 = a0
		self.a1 = a1
		self.a2 = a2

	def rotate_robot_with_object(self,a0,a1,a2):
		p0 = np.linspace(self.a0,a0,self.step) # path 0
		p1 = np.linspace(self.a1,a1,self.step)
		p2 = np.linspace(self.a2,a2,self.step)
		for i in range(self.step):
			rate(10000)
			self.rotate_joint(self.base_faces,self.base_faces_origin,(0,self.chess_shift_y,0),p0[i],0,0)
			self.rotate_joint(self.arm1_faces,self.arm1_faces_origin,(0,self.chess_shift_y,self.len_base),p0[i],p1[i],0)
			self.rotate_joint(self.arm2_faces,self.arm2_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),p0[i],p1[i],p2[i])
			self.rotate_joint(self.gripper1_faces,self.gripper1_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),p0[i],p1[i],p2[i])
			self.rotate_joint(self.gripper2_faces,self.gripper2_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),p0[i],p1[i],p2[i])
			
			self.pyramid[1].pos = self.forward_arms(p0[i],p1[i],p2[i])
			self.saveSnapshot()
		self.a0 = a0
		self.a1 = a1
		self.a2 = a2

	def rotate_robot_init(self,a0,a1,a2):
		self.rotate_joint(self.base_faces,self.base_faces_origin,(0,self.chess_shift_y,0),a0,0,0)
		self.rotate_joint(self.arm1_faces,self.arm1_faces_origin,(0,self.chess_shift_y,self.len_base),a0,a1,0)
		self.rotate_joint(self.arm2_faces,self.arm2_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),a0,a1,a2)
		self.rotate_joint(self.gripper1_faces,self.gripper1_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),a0,a1,a2)
		self.rotate_joint(self.gripper2_faces,self.gripper2_faces_origin,(self.len_arm1,self.chess_shift_y,self.len_base),a0,a1,a2)

		self.a0 = a0
		self.a1 = a1
		self.a2 = a2

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
	def inverse_kinematics(self,x,y,z,action):
		if action == 'pick':
			if (x,y) not in self.chess_map:
				Z=-1
			else:
				Z = len(self.chess_map[(x,y)])-1
		if action == 'put':
			Z=0
		Z = Z*.8
		if Z >= 0:
			z -= 1.8
			z += Z
			x += 4.5
			y = 3.5 - y
			# used in case arm can't reach that location
			s  = "(%g,%g,%g) is out of range." % tuple(np.around([x,y,z],2))
			# compute the first angle
			a1 = np.arctan2(y,x)
			# compute the thirs angle
			r  = np.hypot(x,y)
			z -= self.l1
			u3 = ( r**2 + z**2 - self.l2**2 - self.l3**2 ) / ( 2*self.l2*self.l3 )
			if abs(u3)>1:    raise Exception(s)
			a3 = -np.arccos(u3)
			# compute the second angle
			v  = self.l2 + self.l3*u3
			w  = -self.l3 * np.sqrt(1-u3**2)  # this is sin(a3)>0 assuming 0<a3<pi
			a2 = np.arctan2(v*z-w*r,v*r+w*z)
			if a2<0 or a2>np.pi:    raise Exception(s)
			return a1,a2,a3
		else:
			print 'no object there !'
			return self.a1,self.a2,self.a3
			

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


	def saveSnapshot(self):
	    # based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08
	    dcSource = wx.ScreenDC()
	    size = dcSource.Size

	    # Create a Bitmap that will later on hold the screenshot image
	    # Note that the Bitmap must have a size big enough to hold the screenshot
	    # -1 means using the current default colour depth
	    bmp = wx.EmptyBitmap(self.display.width,self.display.height-20)

	    # Create a memory DC that will be used for actually taking the screenshot
	    memDC = wx.MemoryDC()

	    # Tell the memory DC to use our Bitmap
	    # all drawing action on the memory DC will go to the Bitmap now
	    memDC.SelectObject(bmp)

	    # Blit (in this case copy) the actual screen on the memory DC
	    # and thus the Bitmap
	    memDC.Blit( 0, # Copy to this X coordinate
		0, # Copy to this Y coordinate
		self.display.width, # Copy this width
		self.display.height-20, # Copy this height
		dcSource, # From where do we copy?
		self.display.x, # What's the X offset in the original DC?
		self.display.y+20  # What's the Y offset in the original DC?
		)

	    # Select the Bitmap out of the memory DC by selecting a new
	    # uninitialized Bitmap
	    memDC.SelectObject(wx.NullBitmap)

	    img = bmp.ConvertToImage()
	    if self.frame_number<10:
		j = '000'+str(self.frame_number)
	    elif self.frame_number<100:
		j = '00'+str(self.frame_number)
	    elif self.frame_number<1000:
		j = '0'+str(self.frame_number)
	    img.SaveFile('frame_'+j+'.png', wx.BITMAP_TYPE_PNG)
	    print self.frame_number,'image saved..'
	    self.frame_number+=1

	def forward_arms(self,a1,a2,a3):
		z = self.l2*np.sin(a2)+self.l3*np.sin(a3+a2)
		r = self.l2*np.cos(a2)+self.l3*np.cos(a3+a2)
		x = r*np.cos(a1)
		y = r*np.sin(a1)
		return (x,y+self.chess_shift_y,1.8-z)
