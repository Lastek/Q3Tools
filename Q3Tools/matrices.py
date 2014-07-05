'''
Created on Oct 25, 2013

@author: Cyberstorm
'''
from math import sin, cos, tan, radians, sqrt
import numpy as np

a1, a2 = 0, 0

    
def round3(vec3):
    for i in xrange(3):
        vec3[i] = round(vec3[i], 4)
        
def rotx3(deg, vec3):
    rad = radians(deg)
    a1 = cos(rad)
    a2 = sin(rad)
    r = np.zeros(3)
    r[0] = vec3[0]
    r[1] = (vec3[1] * a1) - (vec3[2] * a2)
    r[2] = (vec3[1] * a2) + (vec3[2] * a1)
     
    return r
    
def roty3(deg, vec3):
    rad = radians(deg)
    a1 = cos(rad)
    a2 = sin(rad)
    r = np.zeros(3)
    r[0] = (vec3[0] * a1) + (vec3[2] * a2)
    r[1] = vec3[1]
    r[2] = (-1 * (vec3[0] * a2)) + (vec3[2] * a1)
    
    return r
    
def rotz3(deg, vec3):
    rad = radians(deg)
    a1 = cos(rad)
    a2 = sin(rad)
    r = np.zeros(3)
    r[0] = (vec3[0] * a1) - (vec3[1] * a2)
    r[1] = (vec3[0] * a2) + (vec3[1] * a1)
    r[2] = vec3[2]
    
    return r

def mat4rotz(deg):
    r = np.zeros(16, dtype="float32")
    rad = radians(deg)
    a1 = round(cos(rad), 9)
    a2 = round(sin(rad), 9)
    
    r[0] = a1
    r[1] = -a2
    r[4] = a2
    r[5] = a1
    r[10] = 1.0
    r[15] = 1.0

    return r

def mat4rotx( deg ):
    r = np.zeros( 16, dtype="float32" )
    rad = radians( deg )
    a1 = round( cos( rad ), 9 )
    a2 = round( sin( rad ), 9 )

    r[0] = 1.0
    r[5] = a1
    r[6] = -a2
    r[9] = a2
    r[10] = a1
    r[15] = 1.0
    
    return r  
    
def proj(fov, aspect, near, far):
    R = np.zeros(16, dtype="float32")
    d = 1/tan(fov/2)
    zx = d/aspect
    
    a1 = (near+far)/(near-far)
    a2 = (2*near*far)/(near-far)
    
    R[0] = zx
    R[5] = d
    R[10] = a1
    R[11] = a2
    R[14] = -1
    
    return R

def camera(pos):
    R = np.zeros(16, dtype="float32")
    T = np.zeros(16, dtype="float32")
    V = np.zeros(16, dtype="float32")
    d = np.zeros(3, dtype="float32")
    f = np.zeros(3, dtype="float32")
    
    R[0] = 1
    R[6] = -1
    R[9] = 1
    R[15] = 1
    
    T[0] = 1
    T[5] = 1
    T[10] = 1
    T[15] = 1
    T[3] = -pos[0]
    T[7] = -pos[1]
    T[11] = -pos[2]
    #***************************************************************************
    # d = [target[0]-pos[0], target[1]-pos[1], target[2]-pos[2]]
    # 
    # m = sqrt(d[0]*d[0] + d[1]*d[1] + d[2]*d[2])
    # f = [d[0]/m[0], d[1]/m[1], d[2]/m[2]]
    #***************************************************************************
    
def mat4mul(mat1, mat2):
    r = np.zeros(16, dtype="float32")
    
    r[0] = mat1[0]*mat2[0]+mat1[1]*mat2[4]+mat1[2]*mat2[ 8]+mat1[3]*mat2[12]
    r[1] = mat1[0]*mat2[1]+mat1[1]*mat2[5]+mat1[2]*mat2[ 9]+mat1[3]*mat2[13]
    r[2] = mat1[0]*mat2[2]+mat1[1]*mat2[6]+mat1[2]*mat2[10]+mat1[3]*mat2[14]
    r[3] = mat1[0]*mat2[3]+mat1[1]*mat2[7]+mat1[2]*mat2[11]+mat1[3]*mat2[15]
    r[4] = mat1[4]*mat2[0]+mat1[5]*mat2[4]+mat1[6]*mat2[ 8]+mat1[7]*mat2[12]
    r[5] = mat1[4]*mat2[1]+mat1[5]*mat2[5]+mat1[6]*mat2[ 9]+mat1[7]*mat2[13]
    r[6] = mat1[4]*mat2[2]+mat1[5]*mat2[6]+mat1[6]*mat2[10]+mat1[7]*mat2[14]
    r[7] = mat1[4]*mat2[3]+mat1[5]*mat2[7]+mat1[6]*mat2[11]+mat1[7]*mat2[15]
    r[8] = mat1[8]*mat2[0]+mat1[9]*mat2[4]+mat1[10]*mat2[8]+mat1[11]*mat2[12]
    r[9] = mat1[8]*mat2[1]+mat1[9]*mat2[5]+mat1[10]*mat2[9]+mat1[11]*mat2[13]
    r[10]= mat1[8]*mat2[2]+mat1[9]*mat2[6]+mat1[10]*mat2[10]+mat1[11]*mat2[14]
    r[11]= mat1[8]*mat2[3]+mat1[9]*mat2[7]+mat1[10]*mat2[11]+mat1[11]*mat2[15]
    r[12]= mat1[12]*mat2[0]+mat1[13]*mat2[4]+mat1[14]*mat2[8]+mat1[15]*mat2[12]
    r[13]= mat1[12]*mat2[1]+mat1[13]*mat2[5]+mat1[14]*mat2[9]+mat1[15]*mat2[13]
    r[14]= mat1[12]*mat2[2]+mat1[13]*mat2[6]+mat1[14]*mat2[10]+mat1[15]*mat2[14]
    r[15]= mat1[12]*mat2[3]+mat1[13]*mat2[7]+mat1[14]*mat2[11]+mat1[15]*mat2[15]
    
    return r

#test
if __name__ == '__main__':
    print 'Vector rotation test:'
    vector = rotz3(180, (1.0, 1.0, 0.0))
    round3(vector)
    print vector
    print 'MatrixTest:'
    vector = mat4rotz(30)
    print vector
    
#identx3 = np.array([[1,0,0],
#                     [0,1,0],  
#                     [0,0,1]])
#[0, 0, 1]])                     
#xrotx3 = identx3
#yrotx3 = identx3
#zrotx3 = identx3
#
#xrot = np.array([[1,0,0],
#                 [0, m.cos(deg), -m.sin(deg)],
#                 [0, m.sin(deg),  m.cos(deg)]])
##y-axis
#yrot = np.array([[m.cos(deg), 0, m.sin(deg)],
#                 [0, 1, 0],
#                 [-m.sin(deg), 0, m.cos(deg)]])
##z-axis
#zrot = np.array([[m.cos(deg), -m.sin(deg), 0],
#                 [m.sin(deg),  m.cos(deg), 0],
#  
#    identity = np.array([[1,0,0,0]
#                         [0,1,0,0]
#                         [0,0,1,0]
#                         [0,0,0,1]])
    
