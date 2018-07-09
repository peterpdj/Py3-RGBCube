#!/usr/bin/env python3

import time
import cubedriver


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
			frame = self.driver.make_frame()
			self.anim.draw(frame, t)
			self.driver.fill(frame)
			time.sleep(0.01)
			f += 1
			if f == 1000:
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


class Color:
	"""
	This class is used by the animation file.
	"""
	def __init__(self, r = 0, g = 0, b = 0):
		self.r = r
		self.g = g
		self.b = b


def runAnimation(anim):
	"""
	This class runs the function 'run' of class Animationrunner. Besides that
	is uses threading for running the cubedriver in a loop.
	"""
	driver = cubedriver.Driver()
	driver.run()

	try:
		runner = AnimationRunner(anim, driver)
		runner.run()
	except KeyboardInterrupt:
		print('KeyboardInterrupt')
		driver.stop()
		print('Driver process stopped')

