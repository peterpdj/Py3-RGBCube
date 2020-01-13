#!/usr/bin/env python3

import cubeanim
from cubeanim import Color
from cubeanim import Position

import math


class RgbCubeAnimation(cubeanim.Animation):
	def draw(self, buf, t):
		pos = Position()
		ROTATION_TIME = 8.0
		rot = 0 # t * (2 * 3.141592653 / ROTATION_TIME)
		center = Position(3.5, 3.5, 3.5)
		for x in range(8):
			pos.x = x
			for y in range(8):
				pos.y = y
				for z in range(8):
					pos.z = z
					dy = (y - center.y)
					dz = (z - center.z)
					vy = dy * math.cos(rot) - dz * math.sin(rot)
					vz = dy * math.sin(rot) + dz * math.cos(rot)
					vpos = Position(pos.x, vy + 3.5, vz + 3.5)
					buf.set(pos, Color(vpos.x / 7, vpos.y / 7, vpos.z / 7))


if __name__ == '__main__':
	anim = RgbCubeAnimation()
	cubeanim.runAnimation(anim,bb=4)

