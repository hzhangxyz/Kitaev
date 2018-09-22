import numpy as np
import sys

n1=int(sys.argv[1])
n2=int(sys.argv[2])
#sq=int(sys.argv[3])

data = np.load(f"data-{n1}-{n2}.npy")

data = np.reshape(np.abs(data),[-1])

def old_pro():
    index = [i for i,j in zip(range(2**(n1*n2)),map(lambda x:x>10e-5,data)) if j]

    gra = [bin(i)[2:].zfill(n1*n2) for i in index]

    def sprint(s,sq):
        res = ""
        for i in np.reshape(np.array(list(s)),[sq,sq]):
            res += "".join(i)
            res += "\n"
        return res

    def cut(gra, sq):
        ans = []
        for i in gra:
            tmp = np.reshape(np.array(list(i)),[n1,n2])
            for i in range(n1-sq+1):
                for j in range(n2-sq+1):
                    ans.append(sprint(tmp[i:i+sq,j:j+sq],sq))
        return ans

    ans = np.unique(cut(gra,sq),return_counts=True)
    res = list(zip(*ans))
    res.sort(key=lambda x:x[1])

    print(len(res),"/",2**(sq*sq))
    print()

    for i,j in res:
        print(j)
        print(i)

index = [i for i,j in zip(range(2**(n1*n2)),map(lambda x:x>1,data)) if j]
gra = [bin(i)[2:].zfill(n1*n2) for i in index]
cou = []

print(np.unique(list(map(lambda x:x.count("1"),gra)),return_counts=True))

"""
def check(arr):
    f = lambda x:"".join(np.reshape(x,[-1]))
    ft = lambda x:f(np.transpose(x))
    tmp = f(arr) > f(arr[::-1,::]) or f(arr) > f(arr[::-1,::-1]) or f(arr) > f(arr[::,::-1])
    if n1 != n2:
        return tmp
    return tmp or f(arr) > ft(arr) or f(arr) > ft(arr[::-1,::]) or f(arr) > ft(arr[::-1,::-1]) or f(arr) > ft(arr[::,::-1])

for i in gra:
    res = ""
    arr = np.reshape(np.array(list(i)),[n1,n2])
    if check(arr): continue
    for j in arr:
        res += "".join(j)
        res += "\n"
    cou.append(i.count("1"))
    print(res)

print(len(index))

from scipy.special import comb

for i,j in zip(*np.unique(cou,return_counts=True)):
    print(i,j,int(comb(n1*n2,i)))
"""
