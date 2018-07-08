#!/usr/bin/env python3

import time
import spidev

quit = False

anode = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]
class Buffer:
	def __init__(self):
		self.byte_red0 = bytearray(64)
		self.byte_blue0 = bytearray(64)
		self.byte_green0 = bytearray(64)

	def LED(self, pos, color):
		whichbyte = int(((pos.x*64)+(pos.y*8)+pos.z)/8)
		wholebyte = (pos.x*64)+(pos.y*8)+pos.z
		posInByte = wholebyte-(8*whichbyte)
		#print(posInByte)
		self.byte_red0[whichbyte] += bitRead(color.b,0)*posInByteHelp[posInByte]
		self.byte_green0[whichbyte] += bitRead(color.g,0)*posInByteHelp[posInByte]
		self.byte_blue0[whichbyte] += bitRead(color.r,0)*posInByteHelp[posInByte]
		#print(whichbyte, wholebyte, byte_red0[whichbyte],byte_green0[whichbyte],byte_blue0[whichbyte])

buf = Buffer()

posInByteHelp = [1,2,4,8,16,32,64,128]

def bitWrite(i, bitnr, value):
    return i | (1 << bitnr) if value else i & (1<<bitnr)

def bitRead(i, bitnr):
    return (i >> (bitnr))&1

def mainloop():
	t0 = time.time()
	fr = 0
	tf0 = 0
	spi = spidev.SpiDev()
	spi.open(0, 0)
	spi.max_speed_hz = 8000000
	while not quit:
		cbuf = buf
		for i in range(0, 64, 8):
			spi.xfer(list(cbuf.byte_red0[i:i+8]) + list(cbuf.byte_green0[i:i+8]) + list(cbuf.byte_blue0[i:i+8]) + list([1 << (i >> 3)]))
			#time.sleep(0.00001)
		fr += 1
		if fr == 400:
			t = time.time() - t0
			fps = fr / (t - tf0)
			print('Driver FPS', fps)
			fr = 0
			tf0 = t

	spi.xfer2([0] * 25)

