
__author__ = 'Cyberstorm'
# Bit of code to convert bytes to ascii chars
# dont need this if we write with mode='bw'
# lg = str(magic[0], encoding='ascii')
# print (type(lg))
# print (lg)
#mkay...
import struct
import array
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

        for i in range(16):
            self.direntry.append(struct.unpack("ii", self.file.read(8)))
            print ("lump : {} ofst {} | len {}".format(i, self.direntry[i][0], self.direntry[i][1]))

        #self.Textures(self.rdlump(1))
        self.Planes(self.rdlump(2))
    def rdlump(self, de):
        self.file.seek(self.direntry[de][0])    #offset
        return self.file.read(self.direntry[de][1])    #length

    def Entities(self, data):
        pass

    def Textures(self, data):   #Needs to detect shader number shaders = (len/72)
        textures = len(data)/72
        # get tex name, unpack surface and content flags
        self.texture = list()
        for i in range(textures):
            self.texture.append(data[i*64 : i*64 + 64])
            #2byte int
            self.texture.append(struct.unpack("i", data[64:68]))
            self.texture.append(struct.unpack("i", data[68:72]))
        print (self.texture)

    def Planes(self, data):
        planes = int(len(data) / 16)
        self.plane = list()
        # 16 = planesize = 4bFloat*3verts+4bfloat*1dist
        for i in range(planes):
            self.plane.append(struct.unpack("ffff", data[i * 16:i * 16 + 16]))
        print (self.plane)

    def Nodes(self, data):
        pass

    def Leafs(self, data):
        pass

    def Leaffaces(self, data):
        pass

    def Leafbrushes(self, data):
        pass

    def Models(self, data):
        pass

    def Brushes(self, data):
        pass

    def Brushsides(self, data):
        pass

    def Vertexes(self, data):
        pass

    def Meshverts(self, data):
        pass

    def Effects(self, data):
        pass

    def Faces(self, data):
        pass

    def Lightmaps(self, data):
        pass

    def Lightvols(self, data):
        pass

    def Visdata(self, data):
        pass

ibsp = BSP()
ibsp.start("test_bigbox.bsp")