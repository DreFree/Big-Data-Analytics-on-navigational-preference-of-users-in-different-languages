from numpy import linalg as LA
import numpy as np
M=np.array([
    [0,0,0,0,0,0],
    [0,0,1,0,1,0],
    [0,1,0,0,3,1],
    [0,0,0,0,0,0],
    [0,1,3,0,0,1],
    [0,0,1,0,1,0]
])
W=[]



##MARKOV 1st model transform
M_P=[]
for i in range(len(M)):
    sum=np.sum(M[i])
    M_P.append([])
    for j in range(len(M[i])):
        if sum != 0:
            M_P[i].append(M[i][j]/sum)
        else:
            M_P[i].append(0)

for i in range(len(M)):
    W.append(np.sum(M[i]))

W=[1,1,1,1,1,1]

##HERE
print("M_P")
print(M_P)
A=np.append(np.transpose(M_P)-np.identity(6),[W],axis=0)
b=np.transpose(np.array([0,0,0,0,0,0,1]))
F=np.linalg.solve(np.transpose(A).dot(A), np.transpose(A).dot(b))
print("MARKOV stationary distribution")
print(F,np.sum(F))
print()
##MARKOV STATionary distribution states probability 
#HERE




"""
TRIED SOMETHING HERE
print()
w, v = LA.eig(M_P)
for i in range (len(M_P)):
    sum=0
    for j in range(len(M_P[i])):
        sum+=w[i]*v[i][j]
    print(i,":",sum)

print (w)
print()
print(v)
"""

""" LDA model transform
##NOPE DOENST WORK
M_L=[]
L_T=[]
for i in range(len(M)):
    L_T.append(0)

for i in range(len(M)):
    for j in range(len(M[i])):
        L_T[M[i][j]]+=1
for i in range(len(M)):
    sum=np.sum(M[i])
    M_L.append([])
    for j in range(len(M[i])):
        if sum!=0:
            M_L[i].append((M[i][j]/sum)*(L_T[i]/np.sum(L_T)))
        else:
            M_L[i].append(0)
###
"""