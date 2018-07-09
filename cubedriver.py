#!/usr/bin/env python3
import multiprocessing
from multiprocessing.sharedctypes import RawArray, RawValue
import array
import time
import spidev


class Driver:
	MEM_SIZE = 3 * 64
	BLUE_OFFSET = 0
	GREEN_OFFSET = 64
	RED_OFFSET = 128

	def __init__(self):
		self.buf = RawArray('B', Driver.MEM_SIZE)
		self.sp = None
		self.quit = RawValue('B', 0)

	@staticmethod
	def _mainloop(buf, quit):
		t0 = time.time()
		fr = 0
		tf0 = 0
		spi = spidev.SpiDev()
		spi.open(0, 0)
		spi.max_speed_hz = 8000000
		try:
			while not quit:
				for i in range(0, 64, 8):
					red_i = Driver.RED_OFFSET + i
					green_i = Driver.GREEN_OFFSET + i
					blue_i = Driver.BLUE_OFFSET + i
					spi.xfer(list(buf[red_i:red_i+8]) + list(buf[green_i:green_i+8]) + list(buf[blue_i:blue_i+8]) + list([1 << (i >> 3)]))
					#time.sleep(0.00001)
				fr += 1
				if fr == 400:
					t = time.time() - t0
					fps = fr / (t - tf0)
					print('Driver FPS', fps)
					fr = 0
					tf0 = t
		except KeyboardInterrupt:
			quit = 1
		spi.xfer2([0] * 25)

	def fill(self, mem):
		self.buf[:] = mem

	def run(self):
		if self.sp is None:
			self.quit = 0
			self.sp = multiprocessing.Process(target=self._mainloop, args=(self.buf, self.quit))
			self.sp.daemon = True
			self.sp.start()

	def stop(self):
		if self.sp is not None:
			self.quit = 1
			self.sp.join()
			self.sp = None

