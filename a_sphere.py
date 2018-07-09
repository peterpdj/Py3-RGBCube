#!/usr/bin/env python3

import cubeanim
from cubeanim import Color
from cubeanim import Position

import math


class MyFirstAnimation(cubeanim.Animation):
	colors = (
		Color( 0,  0,  0),
		Color(1.0,  0,  0),
		Color(1.0, 1.0,  0),
		Color( 0, 1.0,  0),
		Color( 0, 1.0, 1.0),
		Color( 0,  0, 1.0),
		Color(1.0,  0, 1.0),
		Color(1.0, 1.0, 1.0),
		Color( 0,  0,  0),
		Color( 0,  0,  0),
		Color(1.0,  0,  0),
		Color(1.0,  0,  0),
		Color(1.0,  0,  0),
		Color( 0,  0,  0),
		Color( 0,  0,  0),
		Color(1.0,  0,  0),
	)

	def draw(self, buf, t):
		pos = Position()
		center = Position(t%14, t%14, t%14)
		for x in range(8):
			pos.x = x
			for y in range(8):
				pos.y = y
				for z in range(8):
					pos.z = z
					#c = int(t) % len(self.colors)
					scale = 4
					rx = (x - center.x) / scale
					ry = (y - center.y) / scale
					rz = (z - center.z) / scale
					d = math.sqrt(rx * rx + ry * ry + rz * rz)
					c = int((1 + math.sin(t - d)) * 4)
					if c >= len(self.colors):
						c = len(self.colors) - 1
					color = self.colors[c]
					buf.set(pos, color)


if __name__ == '__main__':
	anim = MyFirstAnimation()
	cubeanim.runAnimation(anim)

