from visual import *
from shapefile import *
from Polygon import *
import numpy as np

pattern = zeros((8,8,3)) # 4 by 8 by 3 numpy array of 0's
pattern[0][0] = (1,.5,.7) # assign first rgb triple



def rotate_robot(obj,faces,shift,a0,a1,a2):
	for j,v in enumerate(faces):
		v1 = v - shift
		v2 = rotate(v1, angle=a2, axis=(0,1,0)) + (shift[0],0,0)
		v2 = rotate(v2, angle=a1, axis=(0,1,0)) 
		v2 = rotate(v2, angle=a0, axis=(0,0,1)) + (0,shift[1],shift[2])
		obj.pos[j] = v2

#chess=box(pos=vector(0,0,0),size=(8,8,.5),color=color.orange,material=materials.wood)
#ball=sphere(pos=vector(4,7,3),radius=2,color=color.green)

c = (1,1,0)
c2 = color.rgb_to_hsv(c)	# convert RGB to HSV
print(c2)	# (0.16667, 1, 1)
c3 = color.hsv_to_rgb(c2)	# convert back to RGB
print(c3)	# (1, 1, 0)

chess_shift_x = 8
chess_shift_y = 6

len_arm1 = 8
len_arm2 = 6
len_gripper = 2
len_base = 2

scene2 = display(title='Examples of Tetrahedrons', x=0, y=0, width=600, height=600, center=(chess_shift_x,chess_shift_y,0), background=(1,1,1))

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
chess1 = box(pos=(chess_shift_x,chess_shift_y,-.3),axis=(0,0,1),size=(.4,9,9),color=color.orange,material=materials.wood)
chess2 = box(pos=(chess_shift_x,chess_shift_y,-.25),axis=(0,0,1), size=(.5,8,8),color=color.orange, material=tex)


x = arrow(pos=(0,0,0),axis=(1,0,0),length=10,shaftwidth=.2,color=color.red)
y = arrow(pos=(0,0,0),axis=(0,1,0),length=10,shaftwidth=.2,color=color.green)
z = arrow(pos=(0,0,0),axis=(0,0,1),length=10,shaftwidth=.2,color=color.blue)


base_1 = box(pos=(0,chess_shift_y,-.25),axis=(0,0,1), size=(.5,2,2),color=color.black, material=materials.plastic)

base_2 = Polygon( [(-1,0), (-.75,len_base), (.75,len_base), (1,0)] )
base_3 = shapes.circle(pos=(0,len_base), radius=.75)
base_4 = shapes.circle(pos=(0,len_base), radius=0.2)
base_s = [(0,chess_shift_y-.5,0),(0,chess_shift_y+.5,0)]
base = extrusion(pos=base_s, shape=base_2+base_3-base_4, color=color.red)

arm1_1 = Polygon( [(0,.75), (len_arm1,.5), (len_arm1,-.5), (0,-.75)] )
arm1_2 = shapes.circle(pos=(0,0), radius=.75)
arm1_3 = shapes.circle(pos=(0,0), radius=0.2)
arm1_4 = shapes.circle(pos=(len_arm1,0), radius=.5)
arm1_5 = shapes.circle(pos=(len_arm1,0), radius=0.2)
arm1_s = [(0,chess_shift_y+.5,len_base),(0,chess_shift_y+1.5,len_base)]
arm1 = extrusion(pos=arm1_s, shape=arm1_1+arm1_2-arm1_3+arm1_4-arm1_5, color=color.blue)

arm2_1 = Polygon( [(0,.5), (len_arm2,.4), (len_arm2,-.4), (0,-.5)] )
arm2_2 = shapes.circle(pos=(0,0), radius=.5)
arm2_3 = shapes.circle(pos=(0,0), radius=0.2)
arm2_4 = shapes.circle(pos=(len_arm2,0), radius=.4)
arm2_5 = shapes.circle(pos=(len_arm2,0), radius=0.2)
arm2_s = [(len_arm1,chess_shift_y-.5,len_base),(len_arm1,chess_shift_y+.5,len_base)]
arm2 = extrusion(pos=arm2_s, shape=arm2_1+arm2_2-arm2_3+arm2_4-arm2_5, color=color.red)

gripper_1 = Polygon( [(0,.4), (len_gripper,.3), (len_gripper,-.3), (0,-.4)] )
gripper_2 = shapes.circle(pos=(0,0), radius=.4)
gripper_4 = shapes.circle(pos=(len_gripper,0), radius=.3)
gripper1_s = [(len_arm1+len_arm2,chess_shift_y-.6,len_base),(len_arm1+len_arm2,chess_shift_y-.5,len_base)]
gripper2_s = [(len_arm1+len_arm2,chess_shift_y+.5,len_base),(len_arm1+len_arm2,chess_shift_y+.6,len_base)]

gripper1 = extrusion(pos=gripper1_s, shape=gripper_1+gripper_2+gripper_4, color=color.green)
gripper2 = extrusion(pos=gripper2_s, shape=gripper_1+gripper_2+gripper_4, color=color.green)

base_faces = base.create_faces()
arm1_faces = arm1.create_faces()
arm2_faces = arm2.create_faces()

base_faces_copy = base_faces.pos.copy()
arm1_faces_copy = arm1_faces.pos.copy()
arm2_faces_copy = arm2_faces.pos.copy()

for i in range(90):
	rate(10)
	a0 = i*np.pi/180.0
	a1 = i*np.pi/180.0
	a2 = i*np.pi/180.0
	rotate_robot(base_faces,base_faces_copy,(0,chess_shift_y,0),a0,0,0)
	rotate_robot(arm1_faces,arm1_faces_copy,(0,chess_shift_y,len_base),a0,a1,0)
	rotate_robot(arm2_faces,arm2_faces_copy,(len_arm1,chess_shift_y,len_base),a0,a1,a2)
	#print base_faces_copy[0]



