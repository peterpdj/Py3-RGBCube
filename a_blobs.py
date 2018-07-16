#!/usr/bin/env python3

import cubeanim
from cubeanim import Color
from cubeanim import Position

import math


class BlobsAnimation(cubeanim.Animation):
	def draw(self, buf, t):
		speed = 0.5
		st = t * speed
		a = Position(math.sin(2 * (st - 0.7)), math.cos(3 * (st - 0.25)), math.sin(5 * (st - 0.4)))
		b = Position(math.sin(7 * (st - 1.7)), math.cos(4 * (st - 0.75)), math.sin(3 * (st - 2.1)))
		c = Position(math.sin(5 * (st - 2.7)), math.cos(2 * (st - 1.25)), math.sin(4 * (st - 1.4)))
		size_a = 1.0 + (0.6 * math.sin(st * 4))
		size_b = 1.0 + (0.6 * math.sin(st * 2.5))
		size_c = 1.0 + (0.6 * math.sin(st * 3.1))
		for x in range(8):
			for y in range(8):
				for z in range(8):
					vp = Position(x,y,z).normalize()
					da = vp.distance(a)
					db = vp.distance(b)
					dc = vp.distance(c)
					color = Color(1 - (da * size_a), 1 - (db * size_b), 1 - (dc * size_c))
					buf.set(Position(x,y,z), color)


if __name__ == '__main__':
	anim = BlobsAnimation()
	cubeanim.runAnimation(anim, bb=4)

