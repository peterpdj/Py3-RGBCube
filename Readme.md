Cube Animations
===============

First setup for a home made 8x8x8 RGB Led Cube to drive the LEDS with Python3.

Still working on the project to improve and add the following:
-> Better threading performance. The LED's blink a little due to threading problems.
-> Adding BAM, Bit Angle Modulation to increase color range and intensity.

cubedriver.py contains the functions (via SPI) to drive the LEDS on the cube.
cubeanim.py is the animation generator.
test1.py is the first animation which is using the animation generator.
