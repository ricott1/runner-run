import random
import brain


class Runner(object):
	def __init__(self, index, pool, generation, max_energy, structure):
		self.index = index
		self.pool = pool
		self.generation = generation
		self.id = str(self.pool)
		self.max_energy = max_energy
		self.energy = self.max_energy

		self.velocity = 0
		self.position = 0
		self.output = 0
		self.isArrived = 0

		self.brain = brain.Brain(structure)

	def update(self, inputs):
		self.output = self.brain.propagate(inputs, 0)[0]
		self.position += self.velocity
		if self.energy - self.output > 0:
			self.velocity = max(0, min(self.energy, self.velocity + self.output))
			self.energy = min(self.max_energy, self.energy - self.output)
		else:
			self.max_energy -= 0.01
			self.velocity = max(0, min(self.energy, self.velocity))
			self.energy = min(self.max_energy, max(0, self.energy + 0.01))

		
	def print_state(self):
		return "{:20s}: x = {:6.2f}; v = {:.2f}; e = {:4d}%".format(self.id, f(self.position), f(self.velocity), int(f(self.energy/self.max_energy)*100) )



def f(value):
	return round(value, 2)


