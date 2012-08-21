#!/usr/bin/python

from random import randrange, shuffle
import math

HEIGHT = 10
WIDTH  = 10
NUM_CITIES = 4

InitPopulation = 10
MutationRate = 0.1
NumIterations = 10

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __repr__(self):
		return '('+x+','+y+')';
	
	def distanceTo(self,other):
		dx = abs(self.x - other.x)
		dy = abs(self.y - other.y)
		
		return math.sqrt( dx*dx + dy*dy )

class Route:
	def __init__(self):
		self.path = []
	
	def __repr__(self):
		sx = 'X | '
		sy = 'Y | '
		for p in self.path:
			sx += str(p.x) + ' '
			sy += str(p.y) + ' '
		return sy + '\n' + sx + '\n'


	def addPoint(self,x,y): 
		self.path.append(Point(x,y))

	def generateRoute(self,cities):
		 self.path = list(cities)
		 shuffle(self.path)
	
	def fitness(self):
		# Fitness is reciprocal of distance
		return 1.0/distance()
	
	def distance(self):
		total = 0
		for i in xrange(0,len(self.path)):
			nx = i+1 if (i+1 != len(self.path)) else 0
			total += self.path[i].distanceTo(self.path[nx])
		return total
	
	def sexyTime(self,mate):
		midme = int(len(self.path)/2)
		midlover = int(len(mate.path)/2)
		child = Route()
		child.path = self.path[:midme] + mate.path[midlover:]
		return child
	
	def mutate(self):
		idx1 = randrange(0, len(self.path))
		idx2 = idx1
		while idx1 == idx2:
			idx2 = randrange(0, len(self.path))
		
		self.path[idx1], self.path[idx2] = self.path[idx2], self.path[idx1]


class Grid:
	# Basic map structure
	def __init__(self):
		self.height = HEIGHT
		self.width = WIDTH
		self.g = []
		self.cities = []
	# Generates a random map
    # self.g is only really used for display 
	def Init(self, count):
		self.g = [[False for i in range(self.width)] for j in range(self.height)]
		for i in xrange(count):
			x = randrange(0,self.width)
			y = randrange(0,self.height)
			self.cities.append(Point(x,y))
			self.g[y][x] = True
	
	def buildFromCities(self):
		self.g = [[False for i in range(self.width)] for j in range(self.height)]
		for c in self.cities:
			self.g[c.y][c.x] = True
	

	def __repr__(self):
		s = ''
		for row in self.g:
			s += ' '
			for col in row:
				if(col):
					s += ' X '
				else:
					s += ' - '
			s += '\n'
		return s




g = Grid()
g.Init(NUM_CITIES)
population = []

#generate Initial Population
for i in xrange(0,InitPopulation):
	r = Route()
	r.generateRoute(g.cities)
	population.append(r)


for i in xrange(0,NumIterations):
	



