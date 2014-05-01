__author__ = 'Cyberstorm'
#parctice
import tkinter
import PIL
from PIL import Image
from PIL import ImageTk
import OpenGL.GLUT
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

faces = [(0, -1, 1, 0, 4, 0, 6, 0, 66, 9, 33, 33, 0.0, 0.0, 0.0, 16.0, 0.0, 0.0, 0.0, 16.0, 0.0, 0.0, 0.0, 1.0, 0, 0), (0, -1, 1, 4, 4, 6, 6, 0, 33, 9, 33, 33, 0.0, 0.0, 128.0, 16.0, 0.0, 0.0, 0.0, 16.0, 0.0, 0.0, 0.0, -1.0, 0, 0), (0, -1, 1, 8, 4, 12, 6, 0, 0, 9, 33, 9, 0.0, 8.0, 0.0, 16.0, 0.0, 0.0, 0.0, 0.0, 16.0, 0.0, 1.0, 0.0, 0, 0), (0, -1, 1, 12, 4, 18, 6, 0, 66, 0, 33, 9, 504.0, 0.0, 0.0, 0.0, 16.0, 0.0, 0.0, 0.0, 16.0, -1.0, 0.0, 0.0, 0, 0), (0, -1, 1, 16, 4, 24, 6, 0, 33, 0, 33, 9, 0.0, 504.0, 0.0, 16.0, 0.0, 0.0, 0.0, 0.0, 16.0, 0.0, -1.0, 0.0, 0, 0), (0, -1, 1, 20, 4, 30, 6, 0, 0, 0, 33, 9, 8.0, 0.0, 0.0, 0.0, 16.0, 0.0, 0.0, 0.0, 16.0, 1.0, 0.0, 0.0, 0, 0)]

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


window = tkinter.Tk()

def key(event):
    print ("pressed", repr(event.char))

def callback(event):
    frame.focus_set()
    print ("clicked at", event.x, event.y)


border = 6

x = 400
y = 400

frame = tkinter.Frame(window, width=600, height=600, bg="")
frame.bind("<Key>", key)
frame.bind( "<Button-1>", callback )
frame.pack(expand="true", fill='both',ipadx="0", ipady="0")
bt = tkinter.Button(frame, text="A button")
bt.pack(side="bottom", pady="10")
window.mainloop()