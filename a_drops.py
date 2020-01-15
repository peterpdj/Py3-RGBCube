#!/usr/bin/env python3

import cubeanim
from cubeanim import Color
from cubeanim import Position

import math
import random
import operator
import functools


def sumproduct(*lists):
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))


def generate_color():
    c1 = random.random()
    c2 = random.random()
    c3 = max(0, 1 - c1 - c2)
    cs = [c1 * 500, c2 * 500, c3 * 500]
    random.shuffle(cs)
    return tuple(cs)


def normalize_color(ct):
    total = max(ct)
    return tuple(map(lambda c: c / total, ct))


def weighted_avg(nrs):
    WEIGHTS = (1, 1.4, 1, 1.4, 2, 1.4, 1, 1.4, 1)
    return sumproduct(nrs, WEIGHTS) / sum(WEIGHTS)


def dissolve(lake, x, y, dt):
    DISSOLVE_TIME = 0.9
    dissolve_step = min(1, dt / DISSOLVE_TIME)
    return tuple(map(
        sum, 
        zip(*[
            map(lambda ce: ce * dissolve_step, map(weighted_avg, zip(*[c for cc in lake[x-1:x+2] for c in cc[y-1:y+2]]))),
            map(lambda ce: ce * (1 - dissolve_step), lake[x][y])
        ])
    ))


class DropsAnimation(cubeanim.Animation):
    def __init__(self):
        self.lake = [[(1, 1, 1) for x in range(10)] for y in range(10)]
        self.drops = []
        self.next_drop_t = 0
        self.prev_t = 0

    def draw(self, buf, t):
        dt = t - self.prev_t
        self.prev_t = t
        if t > self.next_drop_t:
            self.next_drop_t = t + 0.1 + random.random() * 3
            drop = {
                    "height": 8,
                    "x": math.floor(random.random() * 8),
                    "y": math.floor(random.random() * 8),
                    "speed": 2 + random.random() * 5,
                    "color": generate_color()
            }
            for r in range(math.floor(random.random() * 5)):
                new_drop = drop.copy()
                new_drop["height"] += r
                self.drops.append(new_drop)

        drops_to_remove = []
        for drop_index, drop in enumerate(self.drops):
            drop["height"] = drop["height"] - (dt * drop["speed"])
            if drop["height"] < 1:
                drop["height"] = 0
                drops_to_remove.append(drop_index)
                self.lake[drop["x"] + 1][drop["y"] + 1] = drop["color"]
            elif drop["height"] < 8:
                buf.set(Position(math.floor(drop["height"]), math.floor(drop["x"]), math.floor(drop["y"])), Color(*normalize_color(drop["color"])))

        for drop_index in reversed(drops_to_remove):
            del self.drops[drop_index]

        # Show lake:
        for lx in range(8):
            for ly in range(8):
                buf.set(Position(0, lx, ly), Color(*normalize_color(self.lake[lx + 1][ly + 1])))

        # Dissolve lake:
        for lx in range(1, 9):
            for ly in range(1, 9):
                self.lake[lx][ly] = dissolve(self.lake, lx, ly, dt)


if __name__ == '__main__':
    anim = DropsAnimation()
    cubeanim.runAnimation(anim, bb=4)

