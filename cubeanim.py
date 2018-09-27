#!/usr/bin/env python3

import time
#import cubedriver
import virtualdriver
import numpy
import math


class Frame:
	def __init__(self):
		self.data = numpy.zeros((8,8,8,3))

	def set(self, pos, color):
		self.data[pos.x, pos.y, pos.z, 0] = color.b
		self.data[pos.x, pos.y, pos.z, 1] = color.g
		self.data[pos.x, pos.y, pos.z, 2] = color.r


class AnimationRunner:
	"""
	This class name says it all. This is running the animation file and uses
	cubedriver to shift the registers via SPI.
	A double buffer is used.
	"""
	def __init__(self, anim, driver):
		self.anim = anim
		self.driver = driver

	def run(self):
		t0 = time.time()
		f = 0
		tf0 = 0
		self.anim.start()
		while True:
			t = time.time() - t0
			frame = Frame()
			self.anim.draw(frame, t)
			self.driver.fill(frame)
			time.sleep(0.01)
			f += 1
			if f == 100:
				fps = f / (t - tf0)
				print('Animation FPS', fps)
				f = 0
				tf0 = t


class Animation:
	"""
	This class is not used at this moment.
	"""
	def __init__(self):
		pass

	def start(self):
		pass

	def draw(self, buf, t):
		pass


class Position:
	"""
	This class is used by the animation file.
	"""
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z

	def minus(self, pos):
		return Position(self.x - pos.x, self.y - pos.y, self.z - pos.z)

	def distance(self, pos):
		diff = self.minus(pos)
		return math.sqrt(diff.x * diff.x + diff.y * diff.y + diff.z * diff.z)

	def normalize(self):
		return Position((self.x - 3.5) / 3.5, ((self.y - 3.5) / 3.5), (self.z - 3.5) / 3.5)



class Color:
	"""
	This class is used by the animation file.
	"""
	def __init__(self, r = 0, g = 0, b = 0):
		self.r = r
		self.g = g
		self.b = b


def runAnimation(anim, bb):
	"""
	This class runs the function 'run' of class Animationrunner. Besides that
	is uses threading for running the cubedriver in a loop.
	"""
	#driver = cubedriver.Driver(bam_bits=bb)
	driver = virtualdriver.Driver(bam_bits=bb)
	driver.run()

	try:
		runner = AnimationRunner(anim, driver)
		runner.run()
	except KeyboardInterrupt:
		print('KeyboardInterrupt')
		driver.stop()
		print('Driver process stopped')

