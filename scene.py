from visual import *

pattern = zeros((8,8,3)) # 4 by 8 by 3 numpy array of 0's
pattern[0][0] = (1,.5,.7) # assign first rgb triple

#chess=box(pos=vector(0,0,0),size=(8,8,.5),color=color.orange,material=materials.wood)
#ball=sphere(pos=vector(4,7,3),radius=2,color=color.green)

c = (1,1,0)
c2 = color.rgb_to_hsv(c)	# convert RGB to HSV
print(c2)	# (0.16667, 1, 1)
c3 = color.hsv_to_rgb(c2)	# convert back to RGB
print(c3)	# (1, 1, 0)

chess_shift_x = 8
chess_shift_y = 6

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
chess1 = box(pos=(chess_shift_x,chess_shift_y,.2),axis=(0,0,1),size=(.4,9,9),color=color.orange,material=materials.wood)
chess2 = box(pos=(chess_shift_x,chess_shift_y,.25),axis=(0,0,1), size=(.5,8,8),color=color.orange, material=tex)


x = arrow(pos=(0,0,0),axis=(1,0,0),length=10,shaftwidth=.2,color=color.red)
y = arrow(pos=(0,0,0),axis=(0,1,0),length=10,shaftwidth=.2,color=color.green)
z = arrow(pos=(0,0,0),axis=(0,0,1),length=10,shaftwidth=.2,color=color.blue)
