__author__ = 'Cyberstorm'
# Bit of code to convert bytes to ascii chars
# lg = str(magic[0], encoding='ascii')
# print (type(lg))
# print (lg)
#mkay...
# http://www.mralligator.com/q3/
#
# Type	Description
# ubyte	unsigned byte
# int	4-byte integer, little-endian
# float	4-byte IEEE float, little-endian
# string[n]	string of n ASCII bytes, not necessarily null-terminated
#

#
# Index	    Lump Name	    Description
# 0	        Entities	    Game-related object descriptions.
# 1	        Textures	    Surface descriptions.
# 2	        Planes	        Planes used by map geometry.
# 3	        Nodes	        BSP tree nodes.
# 4	        Leafs	        BSP tree leaves.
# 5	        Leaffaces	    Lists of face indices, one list per leaf.
# 6	        Leafbrushes	    Lists of brush indices, one list per leaf.
# 7	        Models	        Descriptions of rigid world geometry in map.
# 8	        Brushes	        Convex polyhedra used to describe solid space.
# 9	        Brushsides  	Brush surfaces.
# 10	    Vertexes	    Vertices used to describe faces.
# 11	    Meshverts	    Lists of offsets, one list per mesh.
# 12	    Effects	        List of special map effects.
# 13	    Faces	        Surface geometry.
# 14	    Lightmaps   	Packed lightmap data.
# 15	    Lightvols   	Local illumination data.
# 16	    Visdata	        Cluster-cluster visibility data.

# Note: Q3 treats textures and shaders the same xept shaders
#       go thru some extra stages to be rendered.
# Note: Did some testing and (data[i*s : i*s+s]) is faster than (data[i*s : (i+1)*s])
#       Over 100000 iterations the first is about 2.7721 sec and second is 2.8583 sec
#       Ofcourse this, in reality, is totally irrelevant and does not matter one fucking bit.

# static formatdef lilendian_table[] = {
#     {'x',       1,              0,              NULL},
#     {'b',       1,              0,              nu_byte,        np_byte},
#     {'B',       1,              0,              nu_ubyte,       np_ubyte},
#     {'c',       1,              0,              nu_char,        np_char},
#     {'s',       1,              0,              NULL},
#     {'p',       1,              0,              NULL},
#     {'h',       2,              0,              lu_int,         lp_int},
#     {'H',       2,              0,              lu_uint,        lp_uint},
#     {'i',       4,              0,              lu_int,         lp_int},
#     {'I',       4,              0,              lu_uint,        lp_uint},
#     {'l',       4,              0,              lu_int,         lp_int},
#     {'L',       4,              0,              lu_uint,        lp_uint},
#     {'q',       8,              0,              lu_longlong,    lp_longlong},
#     {'Q',       8,              0,              lu_ulonglong,   lp_ulonglong},
#     {'?',       1,              0,              bu_bool,        bp_bool}, /* Std rep not endian dep,
#         but potentially different from native rep -- reuse bx_bool funcs. */
#     {'f',       4,              0,              lu_float,       lp_float},
#     {'d',       8,              0,              lu_double,      lp_double},
#     {0}
# };

    # def getdata(self, data, num_vars, c_type):
    #     if(len(c_type) != 1):
    #         print ("getdata() : c_type invalid or empty")
    #     c_types =  ['x',1,'b',1,'B',1,'c',1,'s',1,'p',1,'h',2,'H',2,'i',4,'I',4,'l',4,'L',4,'q',8,'Q',8,'?',1,'f',4,'d',8,]
    #     t = next(x for x in range(len(c_types)) if (c_types[x] == c_type)) + 1
    #     num_elem = int(len(data) / (c_types[t] * num_vars))
    #     for i in range(num_elem):

import struct



class BSP():
    def __init__(self):
        self.error = ''
    def start(self, filename):
        self.magic = 0
        self.version = 0
        self.direntry = []
        IBSP_s = 'IBSP'
        self.file = open(filename, mode='rb')

        self.magic = struct.unpack("cccc", self.file.read(4))

        for i in range(4):
            if(str(self.magic[i], encoding='ascii') != IBSP_s[i]):
                print("NOT AN IBSP FILE! Magic number does not match.")
                return 1

        self.version = struct.unpack("i", self.file.read(4))
        print ("version: {}".format(self.version))

        for i in range(17):
            self.direntry.append(struct.unpack("ii", self.file.read(8)))
            print ("lump : {} ofst {} | len {}".format(i, self.direntry[i][0], self.direntry[i][1]))

        self.Entities   (self.rdlump(0))
        self.Textures   (self.rdlump(1))
        self.Planes     (self.rdlump(2))
        self.Nodes      (self.rdlump(3))
        self.Leafs      (self.rdlump(4))
        self.Leaffaces  (self.rdlump(5))
        self.Leafbrushes(self.rdlump(6))
        self.Models     (self.rdlump(7))
        self.Brushes    (self.rdlump(8))
        self.Brushsides (self.rdlump(9))
        self.Vertexes   (self.rdlump(10))
        self.Meshverts  (self.rdlump(11))
        self.Effects    (self.rdlump(12))
        self.Faces      (self.rdlump(13))
        self.Lightmaps  (self.rdlump(14))
        self.Lightvols  (self.rdlump(15))
        self.Visdata    (self.rdlump(16))
        # After I got all the data it would be good to prune the texture names

    def rdlump(self, de):
        self.file.seek(self.direntry[de][0])    #offset
        return self.file.read(self.direntry[de][1])    #length

    def Entities(self, data):
        self.entity = data
        #that was ez
        print ("ents : {}".format(self.entity))

    def Textures(self, data):   #Needs to detect shader number shaders = (len/72)
        self.texture = list()
        s = 72
        textures = int(len(data)/s)
        # get tex name, unpack surface and content flags
        for i in range(textures):   # ideally it should be 1 tuple for each tex but idk how so fuck it (lazy)
            self.texture.append(data[i*s : i*s + 64])
            self.texture.append(struct.unpack("ii", data[i*s+64 : i*s+s]))  #2byte int
        # print ("textures : {}".format(self.texture))

    def Planes(self, data):
        self.plane = list()
        s = 16
        num = int(len(data) / s)
        # 16 = planesize = 4bFloat*3verts+4bfloat*1dist
        for i in range(num):
            self.plane.append(struct.unpack("ffff", data[i*s : i*s+s]))
        # print ("planes : {}".format(self.plane))

    def Nodes(self, data):
        self.node = list()
        s = 36
        num = int(len(data) / s)
        for i in range(num):
            self.node.append(struct.unpack("iiiiiiiii", data[i*s : i*s+s]))
        # print ("nodes : {}".format(self.node))

    def Leafs(self, data):
        self.leaf = list()
        s = 48
        num = int(len(data) / s)
        for i in range(num):
            self.leaf.append(struct.unpack("iiiiiiiiiiii", data[i*s : i*s+s])) #omg
        # print ("leafs : {}".format(self.leaf))

    def Leaffaces(self, data):
        self.leafface = list()
        s = 4
        num = int(len(data) / s)
        for i in range(num):
            self.leafface.append(struct.unpack("i", data[i*s : i*s+s]))

    def Leafbrushes(self, data):
        self.leafbrush = list()
        s = 4
        num = int(len(data) / s)
        for i in range(num):
            self.leafbrush.append(struct.unpack("i", data[i*s : i*s+s]))

    def Models(self, data):
        self.model = list()
        s = 40
        num = int(len(data) / s)
        for i in range(num):
            self.model.append(struct.unpack("ffffffiiii", data[i*s : i*s+s]))

    def Brushes(self, data):
        self.brush = list()
        s = 12
        num = int(len(data) / s)
        for i in range(num):
            self.brush.append(struct.unpack("iii", data[i*s : i*s+s]))

    def Brushsides(self, data):
        self.brushside = list()
        s = 8
        num = int(len(data) / s)
        for i in range(num):
            self.brushside.append(struct.unpack("ii", data[i*s : i*s+s]))

    def Vertexes(self, data):
        self.vertex = list()
        s = 4*10 + 4
        num = int(len(data) / s)
        for i in range(num):
            self.vertex.append(struct.unpack("ffffffffffBBBB", data[i*s : i*s+s]))

    def Meshverts(self, data):
        self.meshvert = list()
        s = 4
        num = int(len(data) / s)
        for i in range(num):
            self.meshvert.append(struct.unpack("i", data[i*s : i*s+s]))

    def Effects(self, data):
        s = 72
        num = int(len(data)/s)
        self.effect = list()
        for i in range(num):   # ideally it should be 1 tuple for each tex but idk how so fuck it (lazy)
            self.effect.append(data[i*s : i*s + 64])
            self.effect.append(struct.unpack("ii", data[i*s+64 : i*s+s]))  #2byte int
        # print ("effects : {}".format(self.effect))

    def Faces(self, data):
        self.face = list()
        s = 4 * 26
        num = int(len(data) / s)
        for i in range(num):
            self.face.append(struct.unpack("iiiiiiiiiiiiffffffffffffii", data[i*s : i*s+s])) #lol
        print ("faces : {}".format(self.face))

    def Lightmaps(self, data):
        self.lightmap = list()
        s = 1*128*128*3
        num = int(len(data) / s)
        for i in range(num):
            self.lightmap.append(struct.unpack("%dp" % s, data[i*s : i*s+s]))

    def Lightvols(self, data):
        self.lightvol = list()
        s = 8
        num = int(len(data) / s)
        for i in range(num):
            self.lightvol.append(struct.unpack("BBBBBBBB", data[i*s : i*s+s]))

    def Visdata(self, data):
        #only single visdata record
        if (self.direntry[16][1] == 0):
            return print ("Skipping Visdata. Length 0")
        self.visdata = list()
        s = 8
        self.visdata.append(struct.unpack("ii", data[0 : s]))
        size = self.visdata[0][0] * self.visdata[0][1]
        s = 1
        self.visdata.append(struct.unpack("B"*size, data[8 : 8+size]))

if __name__ == '__main__':
    ibsp = BSP()
    ibsp.start("test_bigbox.bsp")
