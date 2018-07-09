#!/usr/bin/env python3
import multiprocessing
from multiprocessing.sharedctypes import RawArray, RawValue
import array
import time
import spidev


class Buffer:
	"""
	This buffer is used to fill one frame of the animation on the cube.
	"""
	RED_OFFSET = 0
	GREEN_OFFSET = 64
	BLUE_OFFSET = 128

	MEM_SIZE = 3 * 64

	def __init__(self):
		self.mem = bytearray(self.MEM_SIZE)

	def LED(self, pos, color):
		whichbyte = int(((pos.x*64)+(pos.y*8)+pos.z)/8)
		wholebyte = (pos.x*64)+(pos.y*8)+pos.z
		posInByte = wholebyte-(8*whichbyte)
		self.mem[self.RED_OFFSET + whichbyte] += bitRead(color.b,0)*posInByteHelp[posInByte]
		self.mem[self.GREEN_OFFSET + whichbyte] += bitRead(color.g,0)*posInByteHelp[posInByte]
		self.mem[self.BLUE_OFFSET + whichbyte] += bitRead(color.r,0)*posInByteHelp[posInByte]

posInByteHelp = [1,2,4,8,16,32,64,128]

def bitWrite(i, bitnr, value):
	return i | (1 << bitnr) if value else i & (1<<bitnr)

def bitRead(i, bitnr):
	return (i >> (bitnr))&1

class Driver:
	def __init__(self):
		self.buf = RawArray('B', Buffer.MEM_SIZE)
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
		while not quit:
			for i in range(0, 64, 8):
				red_i = Buffer.RED_OFFSET + i
				green_i = Buffer.GREEN_OFFSET + i
				blue_i = Buffer.BLUE_OFFSET + i
				spi.xfer(list(buf[red_i:red_i+8]) + list(buf[green_i:green_i+8]) + list(buf[blue_i:blue_i+8]) + list([1 << (i >> 3)]))
				#time.sleep(0.00001)
			fr += 1
			if fr == 400:
				t = time.time() - t0
				fps = fr / (t - tf0)
				print('Driver FPS', fps)
				fr = 0
				tf0 = t
		spi.xfer2([0] * 25)

	@staticmethod
	def make_frame():
		return Buffer()

	def fill(self, frame):
		self.buf[:] = frame.mem

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

