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

	def __init__(self, bam_bits = 4):
		self.bam_bits = bam_bits
		self.buf = RawArray('B', Driver.MEM_SIZE * bam_bits)
		self.sp = None
		self.quit = RawValue('B', 0)

	@classmethod
	def _mainloop(self, buf, quit, bam_bits):
		t0 = time.time()
		fr = 0
		tf0 = 0
		spi = spidev.SpiDev()
		spi.open(0, 0)
		spi.max_speed_hz = 8000000
		bb_timeslot = 0
		try:
			while not quit:
				bam_offset = bb_timeslot * self.MEM_SIZE
				for i in range(0, 64, 8):
					red_i = bam_offset + Driver.RED_OFFSET + i
					green_i = bam_offset + Driver.GREEN_OFFSET + i
					blue_i = bam_offset + Driver.BLUE_OFFSET + i
					spi.xfer(list(buf[red_i:red_i+8]) + list(buf[green_i:green_i+8]) + list(buf[blue_i:blue_i+8]) + list([1 << (i >> 3)]))
					#time.sleep(0.00001)
				bb_timeslot = (bb_timeslot + 1) % bam_bits
				fr += 1
				if fr == 400:
					t = time.time() - t0
					fps = fr / (t - tf0)
					print('Driver FPS', fps / bam_bits)
					fr = 0
					tf0 = t
		except KeyboardInterrupt:
			quit = 1
		spi.xfer2([0] * 25)

	def fill(self, frame):
		buf = bytearray(self.MEM_SIZE * self.bam_bits)
		data = frame.data
		for x in range(8):
			for y in range(8):
				for z in range(8):
					wholebyte = (x*64)+(y*8)+z
					whichbyte = int((wholebyte) >> 3)
					posInByte = wholebyte-(8*whichbyte)
					redValue = data[x,y,z,0]
					greenValue = data[x,y,z,1]
					blueValue = data[x,y,z,2]
					self._setBits(buf, redValue, greenValue, blueValue, whichbyte, posInByte)
		self.buf[:] = buf

	def run(self):
		if self.sp is None:
			self.quit = 0
			self.sp = multiprocessing.Process(target=self._mainloop, args=(self.buf, self.quit, self.bam_bits))
			self.sp.daemon = True
			self.sp.start()

	def stop(self):
		if self.sp is not None:
			self.quit = 1
			self.sp.join()
			self.sp = None

	def _setBits(self, buf, r, g, b, whichbyte, posInByte):
		r = int((r + 0.05) * self.bam_bits)
		g = int((g + 0.05) * self.bam_bits)
		b = int((b + 0.05) * self.bam_bits)
		for bb_timeslot in range(self.bam_bits):
			bam_offset = bb_timeslot * self.MEM_SIZE
			buf[bam_offset + self.RED_OFFSET + whichbyte] |= get_bam_value(self.bam_bits, bb_timeslot, r) << posInByte
			buf[bam_offset + self.GREEN_OFFSET + whichbyte] |= get_bam_value(self.bam_bits, bb_timeslot, g) << posInByte
			buf[bam_offset + self.BLUE_OFFSET + whichbyte] |= get_bam_value(self.bam_bits, bb_timeslot, b) << posInByte


BAM_BITS = {
	4: (
		(0, 0, 0, 0),
		(0, 0, 1, 0),
		(1, 0, 1, 0),
		(1, 0, 1, 1),
		(1, 1, 1, 1),
	)
}

def get_bam_value(bam_bits, timeslot, val):
	return BAM_BITS[bam_bits][val][timeslot]

class FrameOld:
	"""
	This buffer is used to fill one frame of the animation on the cube.
	"""
	BLUE_OFFSET = 0
	GREEN_OFFSET = 64
	RED_OFFSET = 128

	MEM_SIZE = 3 * 64

	def __init__(self):
		self.mem = bytearray(self.MEM_SIZE)

	def set(self, pos, color):
		wholebyte = (pos.x*64)+(pos.y*8)+pos.z
		whichbyte = int((wholebyte) >> 3)
		posInByte = wholebyte-(8*whichbyte)
		self.mem[self.BLUE_OFFSET + whichbyte] |= self.bitRead(color.b,0) << posInByte
		self.mem[self.GREEN_OFFSET + whichbyte] |= self.bitRead(color.g,0) << posInByte
		self.mem[self.RED_OFFSET + whichbyte] |= self.bitRead(color.r,0) << posInByte

	@staticmethod
	def bitWrite(i, bitnr, value):
		return i | (1 << bitnr) if value else i & (1<<bitnr)

def bitRead(i, bitnr):
	return (i >> (bitnr))&1

