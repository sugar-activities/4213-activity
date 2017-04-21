### By Gonzalo Odiard, 2006 godiard at gmail.com
### GPL License - http://www.gnu.org/copyleft/gpl.html

# inicializacion
MARGEN = 10
SIZE_WORLD = 800			 # 700
CANT_TILES =  25 			 #  30
print "*** calculo SIZE "
SIZE_TILE = int((SIZE_WORLD - MARGEN * 2) / CANT_TILES)
print "Size tile:", SIZE_TILE


class World:
	initialGreen = 10
	initialRabbits = 10
	initialFoxs = 10
	playState = False
	state = []
	animals = []

	
	def animalsNear(self,x,y):
		animalsNear = []
		for n in range(len(self.animals)):
			animal = self.animals[n]
			if ((abs(animal.posX-x) == 1) and 
			    (abs(animal.posY-y) == 1)):
				animalsNear.append(animal) 
				#print "Encuentra",x,y,animal.posX,animal.posY
		return animalsNear
