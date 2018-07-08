#!/usr/bin/env python3

import time
import threading
import cubedriver


class AnimationRunner:
	def __init__(self, anim):
		self.anim = anim

	def run(self):
		t0 = time.time()
		f = 0
		tf0 = 0
		self.anim.start()
		while True:
			t = time.time() - t0
			buf = cubedriver.Buffer()
			self.anim.draw(buf, t)
			cubedriver.buf = buf
			time.sleep(0.02)
			f += 1
			if f == 1000:
				fps = f / (t - tf0)
				print('Animation FPS', fps)
				f = 0
				tf0 = t


class Animation:
	def __init__(self):
		pass

	def start(self):
		pass

	def draw(self, buf, t):
		pass


class Position:
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z


class Color:
	def __init__(self, r = 0, g = 0, b = 0):
		self.r = r
		self.g = g
		self.b = b


def runAnimation(anim):
	driver_thread = threading.Thread(target=cubedriver.mainloop, args=())
	driver_thread.start()

	try:
		runner = AnimationRunner(anim)
		runner.run()
	except KeyboardInterrupt:
		print('KeyboardInterrupt')
		cubedriver.quit = True
		driver_thread.join()
		print('Driver thread stopped')

