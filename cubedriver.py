#!/usr/bin/env python3
import multiprocessing
from multiprocessing.sharedctypes import RawArray, RawValue
import array
import time
import spidev


class Driver():
	MEM_SIZE = 3 * 64
	RED_OFFSET = 0
	GREEN_OFFSET = 64
	BLUE_OFFSET = 128

	def __init__(self, bam_bits):
		self.bam_bits = bam_bits
		self.bam_lookup = BAM_BITS[self.bam_bits]
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
				if fr == 2000:
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
					wholebyte = (x << 6) + (y << 3) + z
					whichbyte = wholebyte >> 3
					posInByte = wholebyte & 7
					idx = wholebyte * 3
					redValue = ((data[idx + 2] + 1) * self.bam_bits) >> 8
					greenValue = ((data[idx + 1] + 1) * self.bam_bits) >> 8
					blueValue = ((data[idx + 0] + 1) * self.bam_bits) >> 8
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
		for bb_timeslot in range(self.bam_bits):
			bam_offset = bb_timeslot * self.MEM_SIZE
			byte_offset = bam_offset + whichbyte
			buf[byte_offset + self.RED_OFFSET] |= self._get_bam_value(bb_timeslot, r) << posInByte
			buf[byte_offset + self.GREEN_OFFSET] |= self._get_bam_value(bb_timeslot, g) << posInByte
			buf[byte_offset + self.BLUE_OFFSET] |= self._get_bam_value(bb_timeslot, b) << posInByte

	def _get_bam_value(self, timeslot, val):
		return self.bam_lookup[val][timeslot]


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

