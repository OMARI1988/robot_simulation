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


	def saveSnapshot(self,i):
	    # based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08
	    dcSource = wx.ScreenDC()
	    size = dcSource.Size

	    # Create a Bitmap that will later on hold the screenshot image
	    # Note that the Bitmap must have a size big enough to hold the screenshot
	    # -1 means using the current default colour depth
	    bmp = wx.EmptyBitmap(scene2.width,scene2.height-20)

	    # Create a memory DC that will be used for actually taking the screenshot
	    memDC = wx.MemoryDC()

	    # Tell the memory DC to use our Bitmap
	    # all drawing action on the memory DC will go to the Bitmap now
	    memDC.SelectObject(bmp)

	    # Blit (in this case copy) the actual screen on the memory DC
	    # and thus the Bitmap
	    memDC.Blit( 0, # Copy to this X coordinate
		0, # Copy to this Y coordinate
		scene2.width, # Copy this width
		scene2.height-20, # Copy this height
		dcSource, # From where do we copy?
		scene2.x, # What's the X offset in the original DC?
		scene2.y+20  # What's the Y offset in the original DC?
		)

	    # Select the Bitmap out of the memory DC by selecting a new
	    # uninitialized Bitmap
	    memDC.SelectObject(wx.NullBitmap)

	    img = bmp.ConvertToImage()
	    img.SaveFile(str(i)+'.png', wx.BITMAP_TYPE_PNG)
	    print i,'image saved..'


