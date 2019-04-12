#!/usr/bin/env python

import numpy as np

class bond():
    def __init__(self, n1, n2, matrix):
        self.n1 = n1
        self.n2 = n2
        self.matrix = np.reshape(matrix,[2,2,2,2])
    def __repr__(self):
        return f"bond {self.n1}-{self.n2}"

class Lattice():
    def __init__(self, node_num):
        self.node_num = node_num
        self.state_vector = np.random.rand(*[2 for i in range(self.node_num)])-0.5
        self.bonds = []
        self.energy = 0
    def set_bond(self, n1, n2, matrix):
        self.bonds.append(bond(n1,n2,matrix))
    def update(self):
        self.energy = np.max(np.abs(self.state_vector))
        self.state_vector /= self.energy
        state_vector_tmp = np.zeros([2 for i in range(self.node_num)])
        for i in self.bonds:
            order = list(range(self.node_num-2))
            order.insert(i.n1, self.node_num-2)
            order.insert(i.n2, self.node_num-1)
            before_transpose = np.tensordot(self.state_vector, i.matrix, [[i.n1,i.n2],[0,1]])
            state_vector_tmp += np.transpose(before_transpose,order)
        self.state_vector -= state_vector_tmp
    def correlation(self, i, j, im, jm):
        #print(self.state_vector.reshape([-1]))
        order1 = list(range(self.node_num-1))
        order1.insert(i, self.node_num-1)
        tmp1 = np.tensordot(self.state_vector, im, [[i], [0]])
        tmp1t = np.transpose(tmp1, order1)
        #print(tmp1t.reshape([-1]))
        order2 = list(range(self.node_num-1))
        order2.insert(j, self.node_num-1)
        tmp2 = np.tensordot(tmp1t, jm, [[j], [0]])
        tmp2t = np.transpose(tmp2, order2)
        #print(tmp2t.reshape([-1]))
        res = np.dot(tmp2t.reshape([-1]), self.state_vector.reshape([-1]))
        over = np.dot(self.state_vector.reshape([-1]), self.state_vector.reshape([-1]))
        return res/over

S_x = np.reshape([
        0,1,
        1,0], [2,2])/2.

S_z = np.reshape([
        1,0,
        0,-1], [2,2])/2.

pauli_z = np.reshape([
        1,0,0,0,
        0,-1,0,0,
        0,0,-1,0,
        0,0,0,1
        ], [4,4])/4.

pauli_x = np.reshape([
        0,0,0,1,
        0,0,1,0,
        0,1,0,0,
        1,0,0,0
        ], [4,4])/4.

pauli_y = np.reshape([
        0,0,0,-1,
        0,0,1,0,
        0,1,0,0,
        -1,0,0,0
        ], [4,4])/4.

pauli = pauli_x+pauli_y+pauli_z

def square():
    import sys
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    np.set_printoptions(precision=2)
    np.set_printoptions(suppress=True)

    lattice = Lattice(n1*n2)
    for i in range(n1-1):
        for j in range(n2):
            lattice.set_bond(i*n2+j,(i+1)*n2+j,pauli)
    for i in range(n1):
        for j in range(n2-1):
            lattice.set_bond(i*n2+j,i*n2+j+1,pauli)
    for i in range(n1-1):
        for j in range(n2-1):
            lattice.set_bond(i*n2+j,(i+1)*n2+j+1,pauli)
    while True:
        lattice.update()
        ene = (1-lattice.energy)/(n1*n2)
        print(ene, lattice.correlation(int(sys.argv[3]),int(sys.argv[4]),S_x,S_x))

def kitaev(Jx=1, Jy=1, Jz=1, H=0):
    import sys
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    np.set_printoptions(precision=2)
    np.set_printoptions(suppress=True)

    lattice = Lattice(n1*n2)
    graph = [[' ' for i in range(n2*2)] for j in range(n1*2)]
    for i in range(n1):
        for j in range(n2):
            graph[i*2][j*2]="O"
    for i in range(n1):
        for j in range(0,n2-1,4):
            lattice.set_bond(i*n2+j,i*n2+j+1,pauli_x*Jx+pauli*H)
            graph[2*i][2*j+1] = "X"
    for i in range(n1):
        for j in range(1,n2-1,2):
            lattice.set_bond(i*n2+j,i*n2+j+1,pauli_y*Jy+pauli*H)
            graph[2*i][2*j+1] = "Y"
    for i in range(n1):
        for j in range(2,n2-1,4):
            lattice.set_bond(i*n2+j,i*n2+j+1,pauli_z*Jz+pauli*H)
            graph[2*i][2*j+1] = "Z"
    for i in range(n1-1):
        for j in range(0,n2-1,4):
            lattice.set_bond(i*n2+j,(i+1)*n2+j+1,pauli_z*Jz+pauli*H)
            graph[2*i+1][2*j+1] = "Z"
    for i in range(n1-1):
        for j in range(3,n2,4):
            lattice.set_bond(i*n2+j,(i+1)*n2+j-1,pauli_x*Jx+pauli*H)
            graph[2*i+1][2*j-1] = "X"
    for i in range(n1*2):
        print("".join(graph[i]))
    import os
    while True:
        lattice.update()
        ene = (1-lattice.energy)/(n1*n2)
        print(ene)
        np.save(f"data-{n1}-{n2}.temp.npy",lattice.state_vector)
        os.rename(f"./data-{n1}-{n2}.temp.npy",f"./data-{n1}-{n2}.npy")

square()

