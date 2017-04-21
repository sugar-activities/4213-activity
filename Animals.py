### By Gonzalo Odiard, 2006 godiard at gmail.com
### GPL License - http://www.gnu.org/copyleft/gpl.html

import gobject, gtk , cairo,os
import random
import World

print "Init aimals"

def getRandomDirection():
	return 1+int(random.random()*7)		

#	Deltas 
#	1 2 3
#	8 X 4
#	7 6 5

def getNextDirection(direction):
	if (direction == 8):
		return 1
	else:
		return direction + 1

def getDeltaX(direction):
	#print "getDeltaX",direction
	if (direction == 1) or (direction == 8) or (direction == 7):
		return -1
	if (direction == 2) or (direction == 6):
		return 0
	if (direction == 3) or (direction == 4) or (direction == 5):
		return 1
	return 0
def getDeltaY(direction):
	#print "getDeltaY",direction
	if (direction == 1) or (direction == 2) or (direction == 3):
		return -1
	if (direction == 8) or (direction == 4):
		return 0
	if (direction == 7) or (direction == 6) or (direction == 5):
		return 1
	return 0


def getState(world,x,y):
	# verify limits
	if (x >= World.CANT_TILES-1):
		x = 0
	if (y >= World.CANT_TILES-1):
		y = 0
	if (x < 0):
		x = World.CANT_TILES-2
	if (y < 0):
		y = World.CANT_TILES-2
	#print "getState",x,y,world.state[x][y].STATE
	return world.state[x][y].STATE

def internalMove(world,x,y,direction):
	tentativeX = x + int(getDeltaX(direction))   		
	tentativeY = y + int(getDeltaY(direction))
	if (tentativeX >= World.CANT_TILES-1):
		tentativeX = 0
	if (tentativeY >= World.CANT_TILES-1):
		tentativeY = 0
	if (tentativeX < 0):
		tentativeX = World.CANT_TILES-2
	if (tentativeY < 0):
		tentativeY = World.CANT_TILES-2
	return tentativeX,tentativeY



class AbstractAnimal:
	
	edadMaxima = 100
	madurezSexual = 50
	nivelCadenaAlimenticia = 1
	minFrecuenciaAlimentacion = 10
	maxFrecuenciaAlimentacion = 1
	especie = "Indefinida"
	maxNumeroCrias = 4
	frecuenciaSexual = 10

	def __init__(self,x,y):
		print "Iniciando AbstractAnimal"
		self.orden = 0
		self.edad = 30
		self.sexo = "F"
		self.ultimaActSexual = self.edad
		self.ultimaAlimentacion = self.edad
		self.posX = x
		self.posY = y
		self.ultimaDireccion = -1

	def draw(ctx):
		print "Draw"

	def move(self):
		print "Move"

	def checkLive(self):
		if (self.edad > self.edadMaxima):
			print "Muere por edad"
			return False	
		elif ((self.edad - self.ultimaAlimentacion)  > self.minFrecuenciaAlimentacion):
			print "Muere por falta de alimentacion"
			return False
		else:
			return True

# RABBIT		

class Rabbit(AbstractAnimal):
	#print "Inicio conejo"

	path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"images")

	imageSmallMale = cairo.ImageSurface.create_from_png (os.path.join(path,"rabbit_small_m.png"))
	imageSmallFem = cairo.ImageSurface.create_from_png (os.path.join(path,"rabbit_small_f.png"))
	imageMale = cairo.ImageSurface.create_from_png (os.path.join(path,"rabbit_m.png"))
	imageFem = cairo.ImageSurface.create_from_png (os.path.join(path,"rabbit_f.png"))

	edadMaxima = 100
	madurezSexual = 20
	frecuenciaSexual = 10
	nivelCadenaAlimenticia = 1
	minFrecuenciaAlimentacion = 10
	maxFrecuenciaAlimentacion = 1
	especie = "Rabbit"
	maxNumeroCrias = 5


	def __init__(self,x,y):
		#print "Iniciando Rabbit"
		self.orden = 0
		self.edad = 1
		self.sexo = "F"
		if (random.random() > 0.5):
			self.sexo = "M"
		self.ultimaActSexual = self.edad
		self.ultimaAlimentacion = self.edad
		self.posX = x
		self.posY = y
		self.ultimaDireccion = -1

	def draw(self,ctx):
		#print "Draw"
		x1 = World.MARGEN+(self.posX*World.SIZE_TILE)
		y1 = World.MARGEN +(self.posY*World.SIZE_TILE)
		ctx.move_to(x1,y1)
		ctx.translate(x1,y1)
		ctx.rectangle(0,0,World.SIZE_TILE,World.SIZE_TILE);
		ctx.set_source_rgb(146.0/256.0,98.0/256.0,46.0/256.0)	
		if (self.sexo == "M"):
			if (self.edad < Rabbit.madurezSexual):
				ctx.set_source_surface(Rabbit.imageSmallMale,1,1)
			else:
				ctx.set_source_surface(Rabbit.imageMale,1,1)
		if (self.sexo == "F"):
			if (self.edad < Rabbit.madurezSexual):
				ctx.set_source_surface(Rabbit.imageSmallFem,1,1)
			else:
				ctx.set_source_surface(Rabbit.imageFem,1,1)

		ctx.fill()


	def move(self,world):
		self.edad = self.edad + 1
		
		# eat
		if (world.state[self.posX][self.posY].STATE >=1):
			world.state[self.posX][self.posY].STATE = world.state[self.posX][self.posY].STATE - 3
			if (world.state[self.posX][self.posY].STATE <0):
				world.state[self.posX][self.posY].STATE = 0
			self.ultimaAlimentacion = self.edad

		# move
		if (self.ultimaDireccion == -1) :
			self.ultimaDireccion = getRandomDirection()
		# verify green in the next position
		self.tentativeX,self.tentativeY = internalMove(world,self.posX,self.posY,self.ultimaDireccion)
		self.tentativeDirection = getNextDirection(self.ultimaDireccion)
		 
		while ((getState(world,self.tentativeX,self.tentativeY) == 0) and 
			(self.tentativeDirection != self.ultimaDireccion)):
			#print self.tentativeX, self.tentativeY, self.tentativeDirection, self.ultimaDireccion			
			self.tentativeX,self.tentativeY = internalMove(world,self.posX,self.posY,self.tentativeDirection)
			self.tentativeDirection = getNextDirection(self.tentativeDirection)

		self.posX = self.tentativeX
		self.posY = self.tentativeY

		# if female verify for male rabbit
		if ((self.sexo == "F") and 
		    (self.edad > Rabbit.madurezSexual) and
		    ((self.edad - self.ultimaActSexual) > Rabbit.frecuenciaSexual)):
			
			animalsNearArray = world.animalsNear(self.posX,self.posY)	
			if (len(animalsNearArray) > 0):
				maleOk = False
				n = 0
				while (n < len(animalsNearArray) and not (maleOk)):
					nearAnimal = animalsNearArray[n]
					if ((nearAnimal.sexo == "M") and 
					    (nearAnimal.especie == self.especie) and
					    (nearAnimal.edad > Rabbit.madurezSexual) and
					    ((nearAnimal.edad - nearAnimal.ultimaActSexual) > Rabbit.frecuenciaSexual)):
						# born rabbits
						self.ultimaActSexual = self.edad
						cantCrias = int(random.random()*Rabbit.maxNumeroCrias)
						for n in range(cantCrias):
							child = Rabbit(self.posX,self.posY)
							world.animals.append(child)
							print "Nace conejo"
						# salgo del while
						maleOk = True

					n = n + 1


# FOX

class Fox(AbstractAnimal):
	#print "Inicio zorro"

	path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"images")

	imageSmallMale = cairo.ImageSurface.create_from_png (os.path.join(path,"fox_small_m.png"))
	imageSmallFem = cairo.ImageSurface.create_from_png (os.path.join(path,"fox_small_f.png"))
	imageMale = cairo.ImageSurface.create_from_png (os.path.join(path,"fox_m.png"))
	imageFem = cairo.ImageSurface.create_from_png (os.path.join(path,"fox_f.png"))

	edadMaxima = 150
	madurezSexual = 20
	frecuenciaSexual = 5
	nivelCadenaAlimenticia = 2
	minFrecuenciaAlimentacion = 20
	maxFrecuenciaAlimentacion = 3
	especie = "Fox"
	maxNumeroCrias = 3

	def __init__(self,x,y):
		#print "Iniciando Rabbit"
		self.orden = 0
		self.edad = 1
		self.sexo = "F"
		if (random.random() > 0.5):
			self.sexo = "M"
		self.ultimaActSexual = self.edad
		self.minFrecuenciaAlimentacion = 30
		self.ultimaAlimentacion = self.edad
		self.posX = x
		self.posY = y
		self.ultimaDireccion = -1
		self.maxNumeroCrias = 2

	def draw(self,ctx):
		#print "Draw"
		x1 = World.MARGEN+(self.posX*World.SIZE_TILE)
		y1 = World.MARGEN +(self.posY*World.SIZE_TILE)
		ctx.move_to(x1,y1)
		ctx.translate(x1,y1)
		ctx.rectangle(0,0,World.SIZE_TILE,World.SIZE_TILE);
		ctx.set_source_rgb(146.0/256.0,98.0/256.0,46.0/256.0)	
		if (self.sexo == "M"):
			if (self.edad < Fox.madurezSexual):
				ctx.set_source_surface(Fox.imageSmallMale,1,1)
			else:
				ctx.set_source_surface(Fox.imageMale,1,1)
		if (self.sexo == "F"):
			if (self.edad < Fox.madurezSexual):
				ctx.set_source_surface(Fox.imageSmallFem,1,1)
			else:
				ctx.set_source_surface(Fox.imageFem,1,1)

		ctx.fill()


	def move(self,world):
		self.edad = self.edad + 1
		
		# move
		if (self.ultimaDireccion == -1) :
			self.ultimaDireccion = getRandomDirection()
		# verify green in the next position
		self.tentativeX,self.tentativeY = internalMove(world,self.posX,self.posY,self.ultimaDireccion)
		self.tentativeDirection = getNextDirection(self.ultimaDireccion)
		 
		while ((getState(world,self.tentativeX,self.tentativeY) == 0) and 
			(self.tentativeDirection != self.ultimaDireccion)):
			#print self.tentativeX, self.tentativeY, self.tentativeDirection, self.ultimaDireccion			
			self.tentativeX,self.tentativeY = internalMove(world,self.posX,self.posY,self.tentativeDirection)
			self.tentativeDirection = getNextDirection(self.tentativeDirection)

		self.posX = self.tentativeX
		self.posY = self.tentativeY

		# eat
		animalsNearArray = world.animalsNear(self.posX,self.posY)	
		if ((self.edad - self.ultimaAlimentacion) > self.maxFrecuenciaAlimentacion ):
			if (len(animalsNearArray) > 0):
				n = 0
				eat = False
				while ((n < len(animalsNearArray)) and not eat):
					nearAnimal = animalsNearArray[n]
					if (nearAnimal.nivelCadenaAlimenticia < self.nivelCadenaAlimenticia):
						print "Comer conejo!!"				
						n = n+1
						world.animals.remove(nearAnimal)
						eat = True
						self.ultimaAlimentacion = self.edad
					n = n+1

		# if female verify for male fox
		if ((self.sexo == "F") and 
		    (self.edad > Fox.madurezSexual) and
		    ((self.edad - self.ultimaActSexual) > Fox.frecuenciaSexual)):
			
			if (len(animalsNearArray) > 0):
				maleOk = False
				n = 0
				while (n < len(animalsNearArray) and not (maleOk)):
					nearAnimal = animalsNearArray[n]
					if ((nearAnimal.sexo == "M") and 
					    (nearAnimal.especie == self.especie) and
					    (nearAnimal.edad > Fox.madurezSexual) and
					    ((nearAnimal.edad - nearAnimal.ultimaActSexual) > Fox.frecuenciaSexual) ):
						#print "IUPI!!!!"
						# born foxs
						self.ultimaActSexual = self.edad
						cantCrias = int(random.random()*Fox.maxNumeroCrias)
						for n in range(cantCrias):
							child = Fox(self.posX,self.posY)
							world.animals.append(child)
							print "Nace zorro"
						# salgo del while
						maleOk = True

					n = n + 1



