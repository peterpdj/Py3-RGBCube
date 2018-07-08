#!/usr/bin/env python3

import cubeanim
from cubeanim import Color
from cubeanim import Position

import math


class MyFirstAnimation(cubeanim.Animation):
    """
    Class defining properties for the Sphere animation.
    Starting with the color pattern.
    """
	colors = (
		Color( 0,  0,  0),
		Color(15,  0,  0),
		Color(15, 15,  0),
		Color( 0, 15,  0),
		Color( 0, 15, 15),
		Color( 0,  0, 15),
		Color(15,  0, 15),
		Color(15, 15, 15),
		Color( 0,  0,  0),
		Color( 0,  0,  0),
		Color(15,  0,  0),
		Color(15,  0,  0),
		Color(15,  0,  0),
		Color( 0,  0,  0),
		Color( 0,  0,  0),
		Color(15,  0,  0),
	)

	def draw(self, buf, t):
        """
        This function combines the colors and position of the colors and puts
        them into buf.LED(pos, color)
        """
		pos = Position()
		for x in range(8):
			pos.x = x
			for y in range(8):
				pos.y = y
				for z in range(8):
					pos.z = z
					#c = int(t) % len(self.colors)
					scale = 4
					rx = (x - 3.5) / scale
					ry = (y - 3.5) / scale
					rz = (z - 3.5) / scale
					d = math.sqrt(rx * rx + ry * ry + rz * rz)
					c = int((1 + math.sin(t - d)) * 4)
					if c >= len(self.colors):
						c = len(self.colors) - 1
					color = self.colors[c]
					buf.LED(pos, color)


if __name__ == '__main__':
    """
    main function calling the Sphere animation class 'MyFirstAnimation'.
    """
	anim = MyFirstAnimation()
	cubeanim.runAnimation(anim)

