#!/usr/bin/env python

import numpy as np

def get_matrix(n1,n2,Jx=4,Jy=1,Jz=1):
    matrix = np.zeros([n1*n2,n1*n2])

    for i in range(n1):
        for j in range(0,n2-1,4):
            matrix[i*n2+j,i*n2+j+1]=Jx
    for i in range(n1):
        for j in range(1,n2-1,2):
            matrix[i*n2+j,i*n2+j+1]=Jy
    for i in range(n1):
        for j in range(2,n2-1,4):
            matrix[i*n2+j,i*n2+j+1]=Jz
    for i in range(n1-1):
        for j in range(0,n2-1,4):
            matrix[i*n2+j,(i+1)*n2+j+1]=Jz
    for i in range(n1-1):
        for j in range(3,n2,4):
            matrix[i*n2+j,(i+1)*n2+j-1]=Jx

    matrix += np.transpose(matrix)

    print(np.mean(np.abs(np.linalg.eig(matrix)[0]))/8)

import sys
get_matrix(int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]))


