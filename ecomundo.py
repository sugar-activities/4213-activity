#!/usr/bin/env python

### Simulacion de un ecosistema, en el que existe pasto, conejos y zorros.
### By Gonzalo Odiard, 2006 godiard at gmail.com
### GPL License - http://www.gnu.org/copyleft/gpl.html

import gobject, gtk , cairo
import math, random
import gettext
import gtk.glade
import World,Animals,Green
import glade_util
import os
print os.path.abspath(__file__)


world = World.World()

class Tile:
	def __init__ (self,x,y):
		self.X = x
		self.Y = y
		self.STATE = 0;


def drawGrid(ctx):
	ctx.set_line_width(2)
	ctx.set_source_rgb(0,0,0)
	for n in range(0,World.CANT_TILES):
		ctx.move_to(World.MARGEN,World.MARGEN +(World.SIZE_TILE*n))
		ctx.line_to(World.SIZE_TILE * (World.CANT_TILES-1) + World.MARGEN,
			World.MARGEN +(World.SIZE_TILE*n))
		ctx.move_to(World.MARGEN +(World.SIZE_TILE*n),World.MARGEN)
		ctx.line_to(World.MARGEN +(World.SIZE_TILE*n),
			World.SIZE_TILE * (World.CANT_TILES-1)+ World.MARGEN)
		ctx.stroke()

def initWorld(): 
	world.state = []
	world.animals = []
	for n in range(0,World.CANT_TILES):
		world.state.append([])
		for p in range(0,World.CANT_TILES):
			tile = Tile(n,p)
			world.state[n].append(tile)
			

def drawStateWorld(ctx):
	#print "drawStateWorld"
	for n in range(0,World.CANT_TILES-1):
		for p in range(0,World.CANT_TILES-1):
			ctx.save()
			Green.getImagesGreen(world,ctx,n,p)
			#Green.getColorTile(world,ctx,n,p)
			ctx.restore()
	for n in range(len(world.animals)):
		#print "Animal",n
		animal = world.animals[n]
		ctx.save()
		animal.draw(ctx)
		ctx.restore()

def initGreen():
	for n in range(world.initialGreen):
		x = int(random.random()*World.CANT_TILES)
		y = int(random.random()*World.CANT_TILES)
		world.state[x][y].STATE = 2

def initAnimals():
	for n in range(world.initialRabbits):
		x = int(random.random()*(World.CANT_TILES-1))
		y = int(random.random()*(World.CANT_TILES-1))
		#print "Init Rabbit",x,y
		animal = Animals.Rabbit(x,y)
		world.animals.append(animal)
	for n in range(world.initialFoxs):
		x = int(random.random()*(World.CANT_TILES-1))
		y = int(random.random()*(World.CANT_TILES-1))
		#print "Init Fox",x,y
		animal = Animals.Fox(x,y)
		world.animals.append(animal)
                                		

def updateState(drawingarea):	
	#print "update State"
	if (world.playState):
		Green.grow(world)
		n = 0
		
		while (n < len(world.animals)):
			animal = world.animals[n]
			animal.move(world)
			if (not animal.checkLive()):
				cantAnimals = len(world.animals)
				world.animals[n] = cantAnimals
				world.animals.remove(cantAnimals)
			else :
				#Actualizo donde esta
				x1 = World.MARGEN+(World.SIZE_TILE*animal.posX)
				y1 = World.MARGEN +(World.SIZE_TILE*animal.posY)
				n = n+1
		drawingarea.queue_draw_area(0, 0,World.SIZE_WORLD, World.SIZE_WORLD)
		source_id = gobject.timeout_add(1000, updateState,drawingarea)	


class ecomundoGui(glade_util.GladeWrapper):

	def onDrawingAreaExposed(self,da, event):
		#print "drawingarea exposed"
		x, y, width, height = da.allocation
		ctx = da.window.cairo_create()
		drawStateWorld(ctx)		
		drawGrid(ctx)

	def onWindowDestroyed(self, widget):
		gtk.main_quit()

	def onBtPlayClicked(self,widget):
		self.widgets.get_widget("btStop").set_sensitive(True);
		self.widgets.get_widget("btPlay").set_sensitive(False);
		world.playState = True
		source_id = gobject.timeout_add(2000, updateState,self.widgets.get_widget("drawingarea1"))	
		# http://www.pygtk.org/pygtk2tutorial-es/ch-TimeoutsIOAndIdleFunctions.html#sec-Timeouts


	def onBtStopClicked(self,widget):
		self.widgets.get_widget("btStop").set_sensitive(False);
		self.widgets.get_widget("btPlay").set_sensitive(True);
		world.playState = False

	def onBtNewClicked(self,widget):
		initWorld()
		world.initialGreen = self.widgets.get_widget("spbGreen").get_value_as_int()
		world.initialRabbits = self.widgets.get_widget("spbRabbit").get_value_as_int()
		world.initialFoxs = self.widgets.get_widget("spbFox").get_value_as_int()
		initGreen()
		initAnimals()
		# Despues de esto hay que recargar la pantalla
		drawingarea1 = self.widgets.get_widget("drawingarea1")
		ctx = drawingarea1.window.cairo_create()
		drawStateWorld(ctx)		
		drawGrid(ctx)

def main():
	gui = ecomundoGui("./ecomundo.glade", "window1")
	gui.widgets.get_widget("drawingarea1").set_size_request(World.SIZE_WORLD+(2*World.MARGEN),World.SIZE_WORLD+(2*World.MARGEN))
	initWorld()
	initGreen()
	initAnimals()
	gtk.main()

if __name__ == '__main__':
	main()
