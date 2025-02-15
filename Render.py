import os
from functools import partial
from Backend import DataHandler
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui
from PyQt5 import QtOpenGL
from PyQt5 import QtWidgets as qtw
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import OpenGL.GL as gl
from OpenGL import GLU
from OpenGL.arrays import vbo
import numpy as np
import threading
import sys
import random
import webbrowser

class Render(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.x = 0
        self.y = 0
        self.z = 0

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(50, 50, 60)) # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST) # enable depth testing

        self.initGeometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        if height <= 0:
            height = 1

        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix() # push the current matrix to the current stack

        gl.glTranslate(0.0, 0.0, -50.0) # third, translate cube to specified depth
        gl.glScale(20.0, 20.0, 20.0) # second, scale cube
        gl.glRotate(float(self.x), 1.0, 0.0, 0.0)
        gl.glRotate(float(self.y), 0.0, 1.0, 0.0)
        gl.glRotate(float(self.z), 0.0, 0.0, 1.0)
        gl.glTranslate(-0.5, -0.5, -0.5) # first, translate cube center to origin

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE);

        gl.glPopMatrix() # restore the previous modelview matrix

    def initGeometry(self):
        self.cubeVtxArray = np.array(
        [[0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,
        (1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.cubeClrArray = np.array(
        [[0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0 ]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
        (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
        [0, 1, 2, 3,
        3, 2, 6, 7,
        1, 0, 4, 5,
        2, 1, 5, 6,
        0, 3, 7, 4,
        7, 6, 5, 4 ])

    def update(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z
