#!/usr/bin/env python3
import multiprocessing
from multiprocessing.sharedctypes import RawArray, RawValue
import time
import numpy


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
 
class Frame:
	def __init__(self):
		self.data = numpy.zeros((8,8,8,3))

	def set(self, pos, color):
		self.data[pos.x, pos.y, pos.z, 0] = color.b
		self.data[pos.x, pos.y, pos.z, 1] = color.g
		self.data[pos.x, pos.y, pos.z, 2] = color.r


class Cube():
	window = 0
	px = 0
	py = 0
	 
	X_AXIS = 0.0
	Y_AXIS = 0.0
	Z_AXIS = 0.0
	 

	def InitGL(self, Width, Height): 
		glClearColor(0.0, 0.0, 0.0, 0.0)
		glClearDepth(1.0) 
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_SMOOTH)   
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)

	 
	def keyPressed(self, *args):
		if args[0] in (b'q', b'Q'):
			glutLeaveMainLoop()
	 
	 
	def DrawGLScene(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	 
		glLoadIdentity()
		glTranslatef(0.0,0.0,-20.0)
	 
		glRotatef(self.X_AXIS,1.0,0.0,0.0)
		glRotatef(self.Y_AXIS,0.0,1.0,0.0)
		glRotatef(self.Z_AXIS,0.0,0.0,1.0)
	 
		for x in range (8):
			for y in range(8):
				for z in range(8):
					glPushMatrix()
					glTranslatef(x - 3.5, y - 3.5, z - 3.5)
					r = self.buf[Driver.RED_OFFSET + x*8*8 + y*8 + z]
					g = self.buf[Driver.GREEN_OFFSET + x*8*8 + y*8 + z]
					b = self.buf[Driver.BLUE_OFFSET + x*8*8 + y*8 + z]
					glColor3f(r / 255.0, g / 255.0, b / 255.0)
					glutSolidSphere(0.10, 8, 8)
					glPopMatrix()
	 
		glutSwapBuffers()


	def mouseAction(self, b, a, x, y):
		if b == 0 and a == 0:
			self.px = x
			self.py = y


	def mouseMoved(self, x, y):
		self.X_AXIS += (y - self.py) * 0.2
		self.Y_AXIS += (x - self.px) * 0.2
		self.px = x
		self.py = y
	 
	 
	def __init__(self, buf):
		self.buf = buf

		SIZE = (1600, 1600)
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		glutInitWindowSize(*SIZE)
		glutInitWindowPosition(200,200)

		self.window = glutCreateWindow('OpenGL Python Cube')
	 
		glutDisplayFunc(self.DrawGLScene)
		glutIdleFunc(self.DrawGLScene)
		glutKeyboardFunc(self.keyPressed)
		glutMouseFunc(self.mouseAction)
		glutMotionFunc(self.mouseMoved)
		self.InitGL(*SIZE)
		glutMainLoop()
	 

class Driver():
	MEM_SIZE = 8 * 8 * 8
	RED_OFFSET = 0
	GREEN_OFFSET = MEM_SIZE
	BLUE_OFFSET = 2 * MEM_SIZE

	def __init__(self, bam_bits):
		self.bam_bits = bam_bits
		self.buf = RawArray('B', Driver.MEM_SIZE * 3)
		self.sp = None
		self.quit = RawValue('B', 0)

	@classmethod
	def _mainloop(self, buf, quit):
		t0 = time.time()
		try:
			cube = Cube(buf)
		except KeyboardInterrupt:
			pass
		quit = 1

	def newFrame(self):
		return Frame()

	def fill(self, frame):
		buf = bytearray(self.MEM_SIZE * 3)
		data = frame.data
		for x in range(8):
			for y in range(8):
				for z in range(8):
					r = int(data[x,y,z,0] * 255)
					g = int(data[x,y,z,1] * 255)
					b = int(data[x,y,z,2] * 255)
					r = max(0, min(255, r))
					g = max(0, min(255, g))
					b = max(0, min(255, b))
					buf[self.RED_OFFSET + x*8*8 + y*8 + z] = r
					buf[self.GREEN_OFFSET + x*8*8 + y*8 + z] = g
					buf[self.BLUE_OFFSET + x*8*8 + y*8 + z] = b
		self.buf[:] = buf

	def run(self):
		if self.sp is None:
			self.quit = 0
			self.sp = multiprocessing.Process(target=self._mainloop, args=(self.buf, self.quit))
			self.sp.daemon = True
			self.sp.start()

	def stop(self):
		if self.sp is not None:
			self.quit = 1
			self.sp.join()
			self.sp = None

