__author__ = 'Cyberstorm'
#parctice
#import tkinter
#import PIL
#from PIL import Image
#from PIL import ImageTk
import sys
import time as tms
import transformations as mat
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import pyassimp as assimp
# import pygame
# import pygame.docs
import sdl2
import sdl2.mouse
import sdl2.ext

import numpy as np

import idkname as q3bsp

class Face():
    def __init__(self, faces):
        self.raw = faces
        self.numFaces = len(faces)
        self.mv_xyz = list()
        self.vt_xyz = list()
        self.vn_xyz = list()
        self.parse()

    def parse(self):
        pass

TITLE = b'virus.exe'
mPos = np.array([0,0], dtype="int32")
class glObj():
    pass

glsl_v = \
"""
#version 430
//********************
in vec3 pos;
out vec3 dbg;

uniform mat4 matrix;
//********************
void main() {
    dbg = vec3(pos.x, pos.y, pos.z);
    gl_Position = matrix * vec4(pos.x, pos.y, pos.z, 1.0);
}
"""

glsl_f = \
"""
#version 430
//********************
out vec4 final;
in vec3 dbg;
uniform mat4 matrix;
//********************
void main() {
    if(matrix[3][0] < 0) {
        final = vec4(matrix[3][0]*-1*2, 0.6, 0.8, 1.0);
    } else {
        final = vec4(matrix[3][0]*2, 0.6, 0.8 , 1.0);
    }
}
"""


class Renderer():
    def __init__(self):
        #Drawing rectangle
        self.drawing_area = np.array([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0], dtype='float32')
        self.shaderProg = GLuint
        self.vbo = GLuint
        self.ebo = GLuint
        self.uniforms = dict()
        self.BSPloaded = 1
        self.m_button = [False, False, False, False]
        self.m_oldpos = [0,0]
        self.m_pan = [0,0]
        self.shiftval = 0.0
        self.aspect = 1
        self.adder = 0.01
        self.OBJmodel = assimp.load("tris.obj")
        self.triangle = np.array([0.0, 0.5, 0.0,
                                  0.5, -0.5,0.0,
                                  -0.5, -0.5, 0.0], dtype='float32')
        # row-major
        self.matrix = np.array([1.0, 0.0, 0.0, 0.0,
                                0.0, 1.0, 0.0, 0.0,
                                0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 0.0, 1.0], dtype='float32')
        #self.OBJmodel.meshes[0].vertices
            #np.array([0.0,0.5,0.5,-0.5,-0.5,-0.5], dtype='float32')

        # self.triangle = np.reshape(self.triangle, (len(self.triangle)*3))
        print (self.triangle)
        self.initialize()

    def initialize(self):
        glViewport(0,0,600,600)
        self.createBuffers()
        self.createShaders()
        self.initUniforms()
        # self.loadBSP("test_bigbox.bsp")
        # self.createKeyMaps()
        self.draw()

    def createBuffers(self):
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.triangle)*4, self.triangle, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

    def createShaders(self):
        status = 0
        log = ""

        VS = glCreateShader(GL_VERTEX_SHADER)
        FS = glCreateShader(GL_FRAGMENT_SHADER)
        #
        glShaderSource(VS, glsl_v)
        glShaderSource(FS, glsl_f)
        #
        #compile
        glCompileShader(VS)
        status = glGetShaderiv(VS, GL_COMPILE_STATUS)
        if(status != GL_TRUE):
            print ("Failed to compile Vertex Shader")
            log = glGetShaderInfoLog(VS)
            print ("LOG:\n%s" % log )
            return -1
        else: print ("Vertex Shader compiled successfully.")

        glCompileShader(FS)
        status = glGetShaderiv(FS, GL_COMPILE_STATUS)
        if(status != GL_TRUE):
            print ("Failed to compile Fragment Shader")
            log = glGetShaderInfoLog(FS)
            print ("LOG:\n%s" % log)
            return -1
        else: print ("Fragment Shader compiled successfully.")

        self.shaderProg = glCreateProgram()

        glAttachShader(self.shaderProg, VS)
        glAttachShader(self.shaderProg, FS)

        glLinkProgram(self.shaderProg)


        status = glGetProgramiv(self.shaderProg, GL_LINK_STATUS)
        if(status != GL_TRUE):
            print ("Failed to link shader program")
            log = glGetProgramInfoLog(self.shaderProg)
            print ("LOG:\n%s" % log)
            return -1
        else: print ("Program linked successfully.")

        #cleanup
        glDetachShader(self.shaderProg, VS)
        glDetachShader(self.shaderProg, FS)
        glDeleteShader(VS)
        glDeleteShader(FS)

        glUseProgram(0)
        return 0

    def initUniforms(self):
        glUseProgram(self.shaderProg)
        # self.uniforms["mPan"] = glGetUniformLocation(self.shaderProg, "mPan")
        # glUniform2f(self.uniforms["mPan"],0.0 , 0.0)
        # self.uniforms["aspect"] = glGetUniformLocation(self.shaderProg, "aspect")
        # glUniform1f(self.uniforms["aspect"], self.aspect)
        # self.uniforms["shift"] = glGetUniformLocation(self.shaderProg, "shift")
        # glUniform2f(self.uniforms["shift"], self.m_pan[0], self.m_pan[1])
        self.uniforms["matrix"] = glGetUniformLocation(self.shaderProg, "matrix")
        glUniformMatrix4fv(self.uniforms["matrix"],1, GL_FALSE, self.matrix)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        # glUniform2i(self.uniforms["mPan"], 1,1)
        glUseProgram(self.shaderProg)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glEnableVertexAttribArray(0)
        glUniformMatrix4fv(self.uniforms["matrix"],1, GL_FALSE, self.matrix)
        # glUniform2f(self.uniforms["shift"], self.m_pan[0], self.m_pan[1])
        # glDrawElements(GL_TRIANGLES, len(self.triangle), GL_FLOAT, None)
        # glDrawArrays(GL_TRIANGLES, 0, 24)
        glDrawArrays(GL_TRIANGLES, 0, len(self.triangle))

    def timer(self):
        pass

    def doShit(self):
        v = 13
        if(self.matrix[v] > 1):
            self.adder *= -1
        elif(self.matrix[v] < -1):
            self.adder *= -1
        #^2ifwatever
        self.matrix[v] += self.adder

    def mTest(self, a):
        self.matrix[12] = a[0]

    def loadBSP(self, filename=""):
        if len(filename) is 0:
            filename = "test_bigbox.bsp"
        self.ibsp = q3bsp.IBSP(filename)
        self.BSPloaded = 1
        self.uploadBSP()

    def uploadBSP(self):
        arrs = np.asarray(self.ibsp.vertex, dtype="float32")
        indx = np.asarray(self.ibsp.face)
        self.vindex = np.empty(len(indx))
        print(arrs)
        for i in range(len(indx)):
            self.vindex[i] = indx[i][3]

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.ibsp.vertex)*4, arrs, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 11, None)

    def mouse(self, button, state, x, y):
        if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
            print ("%i,%i" % (x,y))
            self.m_oldpos[0] = x
            self.m_oldpos[1] = y
            self.m_button[button] = True
            self.m_button[3] = 1
        elif(button == GLUT_LEFT_BUTTON and state == GLUT_UP):
            self.m_button[button] = False
            self.m_oldpos = [0,0]
            self.m_button[3] = 0

    def mouseMove(self, x, y):
        key1 = 0
        key2 = 0
        key1 =  (self.m_oldpos[0]-x)/240
        key2 =  (self.m_oldpos[1]-y)/240
        self.m_pan[0] -= key1
        self.m_pan[1] += key2
        self.m_pos = (x, y)
        self.m_oldpos = (x+key1,  y+key2)
        # print ("x: [%f] y: [%f]" % (key1, key2))

    def keyboard(self, key, x, y):
        pass

    def createKeyMaps(self):
        keys = list(b'qa')
        self.keymap = dict(zip(keys, self.uniforms.values()))

    def resize(self, x, y):
        glViewport(0, 0, x,y)
        self.aspect = float(x)/float(y)

    def unload(self):
        assimp.release(self.OBJmodel)



rend = 0
#TODO: Create a manipulator class for transforms and
#       pass a reference of renderer instance to it.
#       Have the IOProc class send data to the manipulator
#       via function in the manipulator instance. The
#       data will be a fixed list. Have to pass it by
#       reference from IOProc to manip to avoid copying.
#       The manip function will then process it with
#       if statements by checking if words have

def main():
    global rend
    
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return 0

    x, y = 0, 0
    running = True
    # window = sdl2.ext.Window("ekkek", 600,600, sdl2.SDL_WINDOW_OPENGL)
    window = sdl2.SDL_CreateWindow(TITLE, sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED, 600, 600, sdl2.SDL_WINDOW_OPENGL)
    context = sdl2.SDL_GL_CreateContext(window)
    manip = Transform()
    e = IOProc(sdl2.SDL_Event(), manip)
    # e = sdl2.SDL_Event()
    rend = Renderer()
    time = sdl2.SDL_GetTicks()
    prev_time = sdl2.SDL_GetTicks()
    frame_time = 0
    # sdl2.SDL_GL_SwapWindow(window)
    manip.GetRendHandle(rend)
    dt = 1000./60.

    # while sdl2.SDL_WaitEvent(ctypes.byref(event)):
    while e.checkEvents():
        # time = sdl2.SDL_GetTicks()
        # frame_time = time - prev_time
        # prev_time = time
        # while sdl2.SDL_PollEvent(ctypes.byref(e)) !=0:
        #     if(e.type == sdl2.SDL_QUIT):
        #         running = False

        time += dt
        frame_time = time - sdl2.SDL_GetTicks()
        if(frame_time <= 0):
            frame_time = 1
        tms.sleep(frame_time/1000.)

        #update shit here
        #...
        rend.doShit()
        rend.draw()
        sdl2.SDL_GL_SwapWindow(window)
    rend.unload()
    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_Quit()
#
class IOProc():
    """ Handles input and output to other classes """
    def __init__(self, e=0, t=0):
        """
        @param e: Takes SDL_Event() class
        @type e: sdl2.SDL_Event()
        @type t: Transform()
        :return: None
        """
        self.event = 0
        if self.initEvent(e) is 0:
            pass    #proceed with initialization
        self.manip = t
        self.mouseDown = False
        self.mousePos = np.array([0, 0], dtype="int32")
        self.running = True
    def initEvent(self, e):
        try:    #need to somehow check if correct class as well
            if(e != 0):
                self.event = e
                return 0
            else:
                raise Exception('e Needs to be SDL_Event() class')
        except Exception as exc:
            print(exc)
            a = exc.args
            print('e = ', a)
            return 1

    def checkEvents(self):
        """
        This just acts as a var switch and calls the process function
        @type self.event: sdl2.SDL_Event()
        @return: None
        """
        while sdl2.SDL_PollEvent(ctypes.byref(self.event)) !=0:
            if(self.event.type == sdl2.SDL_QUIT):
                self.running = False
            if(self.event.type == sdl2.SDL_MOUSEBUTTONDOWN):
                self.mouseDown = True
                break
            if(self.event.type == sdl2.SDL_MOUSEBUTTONUP):
                self.mouseDown = False
                break
            if(self.event.type == sdl2.SDL_MOUSEMOTION):
                    # print ("x: %i, y: %i" % (event.motion.x, event.motion.y))
                    self.mousePos[0] = self.event.motion.x
                    self.mousePos[1] = self.event.motion.y
                    # rend.mouseMove(self.event.motion.x, self.event.motion.y)
                    sdl2.SDL_FlushEvent(sdl2.SDL_MOUSEMOTION)
            self.process()
        return self.running

    def process(self):
        if(self.mouseDown == True):
            self.manip.update(self.mousePos)
            #doshit

class Transform():
    def __init__(self):
        self.oldpos = np.array([0,0], dtype='int32')
        self.newpos = np.array([0,0], dtype='int32')
        self.pos    = np.array([0,0], dtype='int32')
        self.upd = False
    def GetRendHandle(self, handle=0):
        """
        Need to call this after renderer is initialized
        @type handle: Renderer()
        """
        self.R_Handle = handle
    def update(self, xy, key=0):
        '''Takes xy as 2 elem. array and key as SDL key value'''
        self.oldpos = self.pos
        self.pos    = xy
        self.upd = True
        self.test()

    def test(self):
        #move mouse to increase/decrease triangle movement speed
        a = [1.0-self.pos[0]/300., 1.0 - self.pos[1]/600.]
        self.R_Handle.mTest(a)



main()

# class Input():
#     def __init__(self):
#         pass
#     def keyboard(self, key, x, y):
#         if(key == '['):
#             self.hud1_show ^= 1
#         elif(key == ']'):
#             self.hud2_show ^= 1
#         elif(key =='y'):
#             if(self.key_quantize > 1):
#                 self.key_quantize -= 1
#         elif(key == 'u'):
#             if(self.key_quantize < self.key_step+127):
#                 self.key_quantize += 1
#         elif(key == 'l'):
#             self.key_conways ^= 1
#         elif(key == '-'):
#             self.key_pan_precis *= 10
#         elif(key == '+'):
#             self.key_pan_precis /= 10
#         elif(key == 'e'):
#             self.key_zoom += 0.1
#             self.key_zoom *= 1.2
#         elif(key == 'q'):
#             self.key_zoom -= 0.1
#             self.key_zoom *= 0.83
#         elif(key == 'w'):
#             self.key_panx += self.key_pan_precis/self.key_zoom*1.5
#         elif(key == 's'):
#             self.key_panx -= self.key_pan_precis/self.key_zoom*1.5
#         elif(key == 'a'):
#             self.key_pany -= self.key_pan_precis/self.key_zoom*1.5
#         elif(key == 'd'):
#             self.key_pany += self.key_pan_precis/self.key_zoom*1.5
#         elif(key == 'z'):
#             self.key_step -= 1
#         elif(key == 'x'):
#             self.key_step += 1
#         elif(key == 'f'):
#             self.c_1 -= 0.001
#         elif(key == 'g'):
#             self.c_1 += 0.001
#         elif(key == 'v'):
#             self.c_2 -= 0.001
#         elif(key == 'b'):
#             self.c_2 += 0.001
#         elif(key == 'h'):
#             if(self.palette_bool == False):
#                 self.palette_bool = True
#             else:
#                 self.palette_bool = False


# def main():
#     global rend
#     glutInit(sys.argv)
#     glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
#     glutInitWindowSize(600,600)
#     glutCreateWindow(TITLE)
#     rend = Renderer()
#     glutDisplayFunc(rend.draw) #draw func here
#     # glutKeyboardFunc() #se
#     glutMouseFunc(rend.mouse)
#     glutMotionFunc(rend.mouseMove)
#     glutReshapeFunc(rend.resize) #resizing
#     glShadeModel(GL_SMOOTH)
#     glClearColor(0.0, 0.0, 0.0, 1)
#     glClearDepth(1.0)
#     # glEnable(GL_DEPTH_TEST)
#     # glDepthFunc(GL_LEQUAL)
#     glutMainLoop()  #se
#
# if __name__ == '__main__':
#
#     main()

# window = tkinter.Tk()
#
# def key(event):
#     print ("pressed", repr(event.char))
#
# def callback(event):
#     frame.focus_set()
#     print ("clicked at", event.x, event.y)
#
#
# border = 6
#
# x = 400
# y = 400
#
# frame = tkinter.Frame(window, width=600, height=600, bg="")
# frame.bind("<Key>", key)
# frame.bind( "<Button-1>", callback )
# frame.pack(expand="true", fill='both',ipadx="0", ipady="0")
# bt = tkinter.Button(frame, text="A button")
# bt.pack(side="bottom", pady="10")
# window.mainloop()

# From q3 bsp spec
# Face
# int   texture	        Texture index.
# int   effect	        Index into lump 12 (Effects), or -1.
# int   type	        Face type. 1=polygon, 2=patch, 3=mesh, 4=billboard
# int   vertex	        Index of first vertex.
# int   n_vertexes	    Number of vertices.
# int   meshvert	    Index of first meshvert.
# int   n_meshverts	    Number of meshverts.
# int   lm_index	    Lightmap index.
# int[2]        lm_start	    Corner of this face's lightmap image in lightmap.
# int[2]        lm_size	        Size of this face's lightmap image in lightmap.
# float[3]      lm_origin	    World space origin of lightmap.
# float[2][3]   lm_vecs	        World space lightmap s and t unit vectors.
# float[3]      normal	        Surface normal.
# int[2]        size	        Patch dimensions.
#

# My old code in C
# for(int i = 0; i < numFaces; ++i) {
# 		if(data.faces[i].type != 1) continue;
#
# 		firstMV		= data.faces[i].meshvert;
# 		numMV		= data.faces[i].n_meshverts;
# 		firstV		= data.faces[i].vertex;
# 		numV		= data.faces[i].n_vertexes;
#
# 		for(int a = 0; a < numMV; a+=3) {
# 			glBindTexture(GL_TEXTURE_2D, texture[0]);
# 			glBegin(GL_TRIANGLES);
#
# 			v1	= data.m_verts[firstMV].offset;
# 			v2	= data.m_verts[firstMV+1].offset;
# 			v3	= data.m_verts[firstMV+2].offset;
#
# 			vt0	= data.verts[firstV + v1].pos;
# 			vt1	= data.verts[firstV + v2].pos;
# 			vt2	= data.verts[firstV + v3].pos;
#
# 			vn0	= data.verts[firstV + v1].normal;
# 			vn1	= data.verts[firstV + v2].normal;
# 			vn2	= data.verts[firstV + v3].normal;
#
# 			glColor3f(0.1f,0.1f,0.1f);
# 			glNormal3f(vn0[0], vn0[1], vn0[2]);
# 			glVertex3f(vt0[0], vt0[1], vt0[2]);
#
# 			glColor3f(0.05f,0.05f,0.05f);
# 			glNormal3f(vn1[0], vn1[1], vn1[2]);
# 			glVertex3f(vt1[0], vt1[1], vt1[2]);
#
# 			glColor3f(0.2f,0.2f,0.2f);
# 			glNormal3f(vn2[0], vn2[1], vn2[2]);
# 			glVertex3f(vt2[0], vt2[1], vt2[2]);
#
# 			glEnd();
# 			firstMV+=3;
# 		}
          #TEX||FX||TYPE||v|n_v|m_v|n_mv|lm_i|lm_s1|lm_s2|lm_sz1|lm_sz2|lm_o1||lm_o2|||lm_o3||lm_v11|lm_v12|lm_v13|lm_v21|lm_v22|lm_v23|nm1||||nm2|||nm3|sz1|sz2|
# faces = [(0, -1,    1,  0, 4,  0,  6,    0,   66,   9,   33,    33,      0.0,   0.0,   0.0,  16.0,  0.0,   0.0,   0.0,   16.0,   0.0,  0.0,  0.0,  1.0, 0, 0),
#          (0, -1,    1,  4, 4,  6,  6,    0,   33,   9,   33,    33,      0.0,   0.0, 128.0,  16.0,  0.0,   0.0,   0.0,   16.0,   0.0,  0.0,  0.0, -1.0, 0, 0),
#          (0, -1,    1,  8, 4, 12,  6,    0,    0,   9,   33,     9,      0.0,   8.0,   0.0,  16.0,  0.0,   0.0,   0.0,    0.0,  16.0,  0.0,  1.0,  0.0, 0, 0),
#          (0, -1,    1, 12, 4, 18,  6,    0,   66,   0,   33,     9,    504.0,   0.0,   0.0,   0.0, 16.0,   0.0,   0.0,    0.0,  16.0, -1.0,  0.0,  0.0, 0, 0),
#          (0, -1,    1, 16, 4, 24,  6,    0,   33,   0,   33,     9,      0.0, 504.0,   0.0,  16.0,  0.0,   0.0,   0.0,    0.0,  16.0,  0.0, -1.0,  0.0, 0, 0),
#          (0, -1,    1, 20, 4, 30,  6,    0,    0,   0,   33,     9,      8.0,   0.0,   0.0,   0.0, 16.0,   0.0,   0.0,    0.0,  16.0,  1.0,  0.0,  0.0, 0, 0)]
# meshverts = [(3), (0), (2), (2), (0), (1), (3), (0), (2,), (2,), (0,), (1,), (3,), (0,), (2,), (2,), (0,), (1,), (3,), (0,), (2,), (2,), (0,), (1,), (3,), (0,), (2,), (2,), (0,), (1,), (3,), (0,), (2,), (2,), (0,), (1,)]
#
# #23vertices
# vertices = [(8.0, 8.0, 0.0, 0.0625, 3.9375, 0.5234375, 0.078125, 0.0, 0.0, 1.0, 183, 183, 183, 255),
#             (8.0, 504.0, 0.0, 0.0625, 0.0625, 0.5234375, 0.3203125, 0.0, 0.0, 1.0, 11, 11, 11, 255),
#             (504.0, 504.0, 0.0, 3.9375, 0.0625, 0.765625, 0.3203125, 0.0, 0.0, 1.0, 3, 3, 3, 255),
#             (504.0, 8.0, 0.0, 3.9375, 3.9375, 0.765625, 0.078125, 0.0, 0.0, 1.0, 10, 10, 10, 255),
#             (8.0, 504.0, 128.0, 0.0625, 0.0625, 0.265625, 0.3203125, 0.0, 0.0, -1.0, 2, 2, 2, 255),
#             (8.0, 8.0, 128.0, 0.0625, 3.9375, 0.265625, 0.078125, 0.0, 0.0, -1.0, 255, 255, 255, 255),
#             (504.0, 8.0, 128.0, 3.9375, 3.9375, 0.5078125, 0.078125, 0.0, 0.0, -1.0, 2, 2, 2, 255),
#             (504.0, 504.0, 128.0, 3.9375, 0.0625, 0.5078125, 0.3203125, 0.0, 0.0, -1.0, 0, 0, 0, 255),
#             (504.0, 8.0, 128.0, 3.9375, 0.0, 0.25, 0.13671875, 0.0, 1.0, 0.0, 13, 13, 13, 255),
#             (8.0, 8.0, 128.0, 0.0625, 0.0, 0.0078125, 0.13671875, 0.0, 1.0, 0.0, 255, 255, 255, 255),
#             (8.0, 8.0, 0.0, 0.0625, 1.0, 0.0078125, 0.07421875, 0.0, 1.0, 0.0, 104, 104, 104, 255),
#             (504.0, 8.0, 0.0, 3.9375, 1.0, 0.25, 0.07421875, 0.0, 1.0, 0.0, 12, 12, 12, 255),
#             (504.0, 8.0, 0.0, 0.0625, 1.0, 0.5234375, 0.00390625, -1.0, 0.0, 0.0, 37, 37, 37, 255),
#             (504.0, 504.0, 0.0, 3.9375, 1.0, 0.765625, 0.00390625, -1.0, 0.0, 0.0, 15, 15, 15, 255),
#             (504.0, 504.0, 128.0, 3.9375, 0.0, 0.765625, 0.06640625, -1.0, 0.0, 0.0, 16, 16, 16, 255),
#             (504.0, 8.0, 128.0, 0.0625, 0.0, 0.5234375, 0.06640625, -1.0, 0.0, 0.0, 40, 40, 40, 255),
#             (504.0, 504.0, 0.0, 3.9375, 1.0, 0.5078125, 0.00390625, 0.0, -1.0, 0.0, 15, 15, 15, 255),
#             (8.0, 504.0, 0.0, 0.0625, 1.0, 0.265625, 0.00390625, 0.0, -1.0, 0.0, 40, 40, 40, 255),
#             (8.0, 504.0, 128.0, 0.0625, 0.0, 0.265625, 0.06640625, 0.0, -1.0, 0.0, 45, 45, 45, 255),
#             (504.0, 504.0, 128.0, 3.9375, 0.0, 0.5078125, 0.06640625, 0.0, -1.0, 0.0, 16, 16, 16, 255),
#             (8.0, 504.0, 0.0, 3.9375, 1.0, 0.25, 0.00390625, 1.0, 0.0, 0.0, 9, 9, 9, 255),
#             (8.0, 8.0, 0.0, 0.0625, 1.0, 0.0078125, 0.00390625, 1.0, 0.0, 0.0, 111, 111, 111, 255),
#             (8.0, 8.0, 128.0, 0.0625, 0.0, 0.0078125, 0.06640625, 1.0, 0.0, 0.0, 255, 255, 255, 255),
#             (8.0, 504.0, 128.0, 3.9375, 0.0, 0.25, 0.06640625, 1.0, 0.0, 0.0, 11, 11, 11, 255)]

