#!/usr/bin/env python3

import cubeanim
from cubeanim import Color
from cubeanim import Position

import math


class RgbCubeAnimation(cubeanim.Animation):
	def draw(self, buf, t):
		pos = Position()
		for x in range(8):
			pos.x = x
			for y in range(8):
				pos.y = y
				for z in range(8):
					pos.z = z
					buf.set(pos, Color(x / 7, y / 7, z / 7))


if __name__ == '__main__':
	anim = RgbCubeAnimation()
	cubeanim.runAnimation(anim)

