#!/usr/bin/python

from random import randrange, shuffle, random
import math
import sys

HEIGHT = 10000
WIDTH  = 10000
NUM_CITIES = 100

InitPopulation = 1000
MatePcnt       = 0.5
MutationRate   = 0.1
NumIterations  = 1000

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __repr__(self):
		return '('+str(self.x)+','+str(self.y)+')';
	
	def distanceTo(self,other):
		dx = abs(self.x - other.x)
		dy = abs(self.y - other.y)
		
		return math.sqrt( dx*dx + dy*dy )

class Route:
	def __init__(self):
		self.path = []
		self.fitness_ = 0 
	
	def __repr__(self):
		return str(self.fitness_)

	def printPoints(self):
		for p in self.path:
			print 'Point,'+str(p.x)+','+str(p.y)
	
	def fancyRepr(self):
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
		self.fitness_ = 1.0/self.distance()
		return self.fitness_
	
	def distance(self):
		total = 0
		for i in xrange(0,len(self.path)):
			nx = i+1 if (i+1 != len(self.path)) else 0
			total += self.path[i].distanceTo(self.path[nx])
		return total
	
	def sexyTime(self,mate):
		child = Route()
		midme = int(len(self.path)/2)
		idx1 = randrange(0, midme)
		idx2 = randrange(idx1+1, len(self.path))
		child.path = self.path[idx1:idx2] 
		for p in mate.path:
			if p not in child.path:
				child.path.append(p)

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


if InitPopulation%2 != 0:
	InitPopulation += 1

print 'Generating Initial Population: Stand By'
for i in xrange(0,InitPopulation):
	r = Route()
	r.generateRoute(g.cities)
	population.append(r)

iteration = 0
print 'Starting life.'
for i in xrange(0,NumIterations):
	
	# Determine fitness
	for indv in population:
		indv.fitness()
	
	maxFit = max(population, key = lambda v: v.fitness_)
	
	print ('Iteration: ' + str(iteration ))
	iteration += 1
	print ('The most fit individual in this population is: ' + str(max(population, key = lambda v: v.fitness_)))
	print ('Datar,'+str(maxFit)+','+str((1.0/maxFit.fitness_)))
	print
	sys.stdout.flush()
	
	
	newPopulation = []
	#for idx in xrange(0,int(len(A)*MatePcnt)):
	

	# Split population into two halves
	A = population[:int(len(population)/2)]
	B = population[int(len(population)/2):]
	
	# Sort by fitness
	A = sorted(A, key= lambda v: v.fitness_, reverse=True)
	B = sorted(B, key= lambda v: v.fitness_, reverse=True)
	
	# Mate
	for idx in xrange(0,int(len(A)*MatePcnt)):
		newPopulation.append(A[idx].sexyTime(B[idx]))	
	
	# Mutate
	for indv in population:
		cpy = Route()
		cpy.path = list(indv.path)
		if(random() < MutationRate):
			cpy.mutate()
			newPopulation.append(cpy)
	
	# Add rest of population
	shuffle(population) 
	newPopulation += population[0:len(population)-len(newPopulation)]
	population = list(newPopulation)




max(population, key = lambda v: v.fitness_).printPoints() 
print('Fitness: ' + str(max(population, key = lambda v: v.fitness_)))
  
