#!/usr/bin/env python3

import cubeanim
from cubeanim import Color
from cubeanim import Position

import math
import time

class SquareAnimation(cubeanim.Animation):
    def draw(self, buf, t):
        r = 1+math.sin(1*t)
        g = 1+math.sin(1.3*t+1.2)
        b = 1+math.sin(1.6*t+2.4)
        for x in range(8):
            for y in range(8):
                for z in range(8):
                    color = Color(r,g,b)
                    buf.set(Position(x,y,z), color)

if __name__ == '__main__':
	anim = SquareAnimation()
	cubeanim.runAnimation(anim, bb=8)

