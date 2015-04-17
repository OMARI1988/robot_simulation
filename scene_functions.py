from visual import *
from shapefile import *
from Polygon import *
import numpy as np
import wx
# http://www.anninaruest.com/pie/2014/07/inverse-kinematics-and-the-m100rak/

class Scene():
	def __init__(self):
		self.chess_shift_x = 8
		self.chess_shift_y = 6

		self.draw_scene()

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





