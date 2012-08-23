#!/usr/bin/python

from random import randrange, shuffle, random
import math
import sys

HEIGHT = 10000
WIDTH  = 10000
NUM_CITIES = 300

InitPopulation = 1000
MatePcnt       = 0.5
MutationRate   = 0.01
NumIterations  = 3000

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __repr__(self):
		return 'Point,'+str(self.x)+','+str(self.y)
	
	def distanceTo(self,other):
		dx = abs(self.x - other.x)
		dy = abs(self.y - other.y)
		
		return math.sqrt( dx*dx + dy*dy )

# Route for traveling to cities
# This is what gets "evolved" 
class Route:
	def __init__(self):
		self.path = []
		self.fitness_ = 0 
	
	def __repr__(self):
		return str(self.fitness_)

	# Generates a random route given a list of cities
	# Used to spawn the initial population
	def generateRoute(self,cities):
		 self.path = list(cities)
		 shuffle(self.path)

	# Fitness function
	# Inverse of distance
	def fitness(self):
		self.fitness_ = 1.0/self.distance()
		return self.fitness_
	
	# Computes the total distance of the path
	def distance(self):
		total = 0
		for i in xrange(0,len(self.path)):
			nx = i+1 if (i+1 != len(self.path)) else 0
			total += self.path[i].distanceTo(self.path[nx])
		return total
	
	# Mates the route with another
	# Grabs a random section from the first parent
    # then fills in the missing points in order from the second parent
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
	
	# Mutates the route by simple swap of points
	def mutate(self):
		idx1 = randrange(0, len(self.path))
		idx2 = idx1
		while idx1 == idx2:
			idx2 = randrange(0, len(self.path))
		
		self.path[idx1], self.path[idx2] = self.path[idx2], self.path[idx1]

	# Random Util
	def printPoints(self):
		for p in self.path:
			print p
	
	def fancyRepr(self):
		sx = 'X | '
		sy = 'Y | '
		for p in self.path:
			sx += str(p.x) + ' '
			sy += str(p.y) + ' '
		return sy + '\n' + sx + '\n'

	def addPoint(self,x,y): 
		self.path.append(Point(x,y))

# Randomly generates a grid of cities
class Grid:
	def __init__(self):
		self.height = HEIGHT
		self.width = WIDTH
		self.cities = []
	
	def Init(self, count):
		for i in xrange(count):
			x = randrange(0,self.width)
			y = randrange(0,self.height)
			self.cities.append(Point(x,y))




g = Grid()
g.Init(NUM_CITIES)
population = []

# Even Population
if InitPopulation%2 != 0:
	InitPopulation += 1


print 'Parameters ', HEIGHT, WIDTH, NUM_CITIES, InitPopulation, MatePcnt, MutationRate, NumIterations
print 'Generating Initial Population: Stand By'
for i in xrange(0,InitPopulation):
	r = Route()
	r.generateRoute(g.cities)
	population.append(r)

iteration = 0
print 'Starting life.'
for i in xrange(0,NumIterations):
	
	newPopulation = []
	
	# Compute fitness 
	for indv in population:
		indv.fitness()
	
	# Most Fit Individual 
	maxFit = max(population, key = lambda v: v.fitness_) 
	
	# Split population into two halves
	A = population[:int(len(population)/2)]
	B = population[int(len(population)/2):]
	
	# Sort them by fitness
	A = sorted(A, key= lambda v: v.fitness_, reverse=True)
	B = sorted(B, key= lambda v: v.fitness_, reverse=True)
	
	# Mate the top MatePcnt% 
	for idx in xrange(0,int(len(A)*MatePcnt)):
		newPopulation.append(A[idx].sexyTime(B[idx]))	
	
	# Mutate a few
	for indv in population:
		cpy = Route()
		cpy.path = list(indv.path)
		if(random() < MutationRate):
			cpy.mutate()
			newPopulation.append(cpy)
	
	# Randomly add rest of population to keep the size of the universe the same
	shuffle(population) 
	newPopulation += population[0:len(population)-len(newPopulation)]
	population = list(newPopulation)

	# Some logging
	print ('Iteration: ' + str(iteration ))
	print ('The most fit individual in this population is: ' + str(maxFit.fitness_))
	print ('Data,'+str(maxFit)+','+str((1.0/maxFit.fitness_)))
	print
	sys.stdout.flush() # Used to watch progress 
	iteration += 1


max(population, key = lambda v: v.fitness_).printPoints() 
print('Fitness: ' + str(max(population, key = lambda v: v.fitness_)))
  
