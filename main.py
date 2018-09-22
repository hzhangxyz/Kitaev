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
    import os
    while True:
        lattice.update()
        ene = (1-lattice.energy)/(n1*n2)
        print(ene)
        np.save(f"data-{n1}-{n2}.temp.npy", lattice.state_vector)
        os.rename(f"./data-{n1}-{n2}.temp.npy",f"./data-{n1}-{n2}.npy")

square()

