#!/usr/bin/env python3

import cubeanim
from cubeanim import Color
from cubeanim import Position

import math


class SquareAnimation(cubeanim.Animation):
    def draw(self, buf, t):
        speed = 2
        st = t * speed
        sinus = int(3.5*(1.05+math.sin(st)))
        a = Position(3.5,3.5,sinus)
        b = Position(3.5,sinus,3.5)
        c = Position(sinus,3.5,3.5)
        a_size = 4
        b_size = 4
        c_size = 4
        for x in range(8):
            for y in range(8):
                for z in range(8):
                    color = Color(0,0,0)
                    if x >= (a.x-a_size) and x <= (a.x+a_size):
                        if y >= (a.y-a_size) and y <= (a.y+a_size):
                            if z == a.z:
                                color.r = 1
                    if x >= (b.x-b_size) and x <= (b.x+b_size):
                        if y == b.y:
                            if z  >= (b.z-b_size) and z <= (b.z+b_size):
                                color.b = 1
                    if x == c.x:
                        if y >= (c.y-c_size) and y <= (c.y+c_size):
                            if z >= (c.z-c_size) and z <= (c.z+c_size):
                                color.g = 1
                    buf.set(Position(x,y,z), color)

if __name__ == '__main__':
	anim = SquareAnimation()
	cubeanim.runAnimation(anim)

