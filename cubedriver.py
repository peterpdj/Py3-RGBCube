#!/usr/bin/env python3
import multiprocessing
from multiprocessing.sharedctypes import RawArray, RawValue
import time
import spidev


class Frame:
	MEM_SIZE = 3 * 64
	RED_OFFSET = 0
	GREEN_OFFSET = 64
	BLUE_OFFSET = 128

	def __init__(self, bam_bits):
		self.bam_bits = bam_bits
		self.buf = bytearray(self.MEM_SIZE * self.bam_bits)

	def set(self, pos, color):
		wholebyte = (pos.x << 6) + (pos.y << 3) + pos.z
		whichbyte = wholebyte >> 3
		posInByte = wholebyte & 7
		self._setBits(color.r, color.g, color.b, whichbyte, posInByte)

	def _setBits(self, r, g, b, whichbyte, posInByte):
		r = int((r + 0.05) * self.bam_bits)
		r = min(self.bam_bits, max(0, r))
		g = int((g + 0.05) * self.bam_bits)
		g = min(self.bam_bits, max(0, g))
		b = int((b + 0.05) * self.bam_bits)
		b = min(self.bam_bits, max(0, b))
		for bb_timeslot in range(self.bam_bits):
			bam_offset = bb_timeslot * self.MEM_SIZE
			self.buf[bam_offset + self.RED_OFFSET + whichbyte] |= get_bam_value(self.bam_bits, bb_timeslot, r) << posInByte
			self.buf[bam_offset + self.GREEN_OFFSET + whichbyte] |= get_bam_value(self.bam_bits, bb_timeslot, g) << posInByte
			self.buf[bam_offset + self.BLUE_OFFSET + whichbyte] |= get_bam_value(self.bam_bits, bb_timeslot, b) << posInByte

class Driver():
	MEM_SIZE = 3 * 64
	RED_OFFSET = 0
	GREEN_OFFSET = 64
	BLUE_OFFSET = 128

	def __init__(self, bam_bits):
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
				bb_timeslot = (bb_timeslot + 1) % bam_bits
				fr += 1
				if fr == 2000:
					t = time.time() - t0
					fps = fr / (t - tf0)
					print('Driver FPS', fps / bam_bits)
					fr = 0
					tf0 = t
		except KeyboardInterrupt:
			quit = 1
		spi.xfer2([0] * 25)

	def newFrame(self):
		return Frame(self.bam_bits)

	def fill(self, frame):
		self.buf[:] = frame.buf

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


BAM_BITS = {
    2: (
        (0, 0),
        (1, 0),
        (1, 1),
    ),
    4: (
        (0, 0, 0, 0),
        (0, 0, 1, 0),
        (1, 0, 1, 0),
        (1, 1, 1, 0),
        (1, 1, 1, 1),
    ),
    8: (
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 1),
        (0, 0, 1, 0, 0, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 0),
        (1, 0, 1, 0, 0, 1, 0, 1),
        (1, 0, 1, 1, 0, 1, 0, 1),
        (1, 0, 1, 0, 1, 1, 1, 0),
        (1, 1, 0, 1, 1, 1, 1, 0),
        (1, 1, 1, 1, 1, 1, 1, 1),
    )
}

def get_bam_value(bam_bits, timeslot, val):
    return BAM_BITS[bam_bits][val][timeslot]

