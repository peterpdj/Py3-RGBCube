#!/usr/bin/env python3

import time
import cubedriver


class Frame:
	"""
	This buffer is used to fill one frame of the animation on the cube.
	"""
	BLUE_OFFSET = 0
	GREEN_OFFSET = 64
	RED_OFFSET = 128

	MEM_SIZE = 3 * 64

	def __init__(self):
		self.mem = bytearray(self.MEM_SIZE)

	def LED(self, pos, color):
		wholebyte = (pos.x*64)+(pos.y*8)+pos.z
		whichbyte = int((wholebyte) >> 3)
		posInByte = wholebyte-(8*whichbyte)
		self.mem[self.BLUE_OFFSET + whichbyte] |= self.bitRead(color.b,0) << posInByte
		self.mem[self.GREEN_OFFSET + whichbyte] |= self.bitRead(color.g,0) << posInByte
		self.mem[self.RED_OFFSET + whichbyte] |= self.bitRead(color.r,0) << posInByte

	@staticmethod
	def bitWrite(i, bitnr, value):
		return i | (1 << bitnr) if value else i & (1<<bitnr)

	@staticmethod
	def bitRead(i, bitnr):
		return (i >> (bitnr))&1


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
			self.driver.fill(frame.mem)
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

