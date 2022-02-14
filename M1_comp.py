from threading import Thread
from os import listdir
from extra_func import getCATid
import numpy as np
from _CAT import CAT as CAT

IFILE="un_res/"
OFILE="comp/m1/"

target=(21,0.01)

T=[]
def _initM(M):
    M, CAT
    l=len(CAT)+2
    for i in range(l):
        M.append([])
        for j in range(l):
            M[i].append(0)

    if len(M)!=l and len(M[0])!=l:
        raise ValueError("M no properly initialized")


def M1_SS(M_P):
    W=[]
    _B=[]
    l=len(M_P)
    for i in range(l):
        W.append(1)
        _B.append(0)
    _B.append(1)
    A=np.append(np.transpose(M_P)-np.identity(l),[W],axis=0)
    b=np.transpose(np.array(_B))
    F=np.linalg.solve(np.transpose(A).dot(A), np.transpose(A).dot(b))
    return F
def M1_prob_trans(M):
    M_P=[]
    M=np.array(M)
    for i in range(len(M)):
        sum=np.sum(M[i])
        M_P.append([])
        for j in range(len(M[i])):
            if sum != 0:
                M_P[i].append(M[i][j]/sum)
            else:
                M_P[i].append(0)
    return M_P
def write(M,ID,S):
    global OFILE, T
    tag=T[ID]
    f=open(OFILE+tag,"w")
    if not f:
        print("error opening file for writing")
        return
    for i,item in enumerate(M):
        if i>0:
            f.write(',')
        f.write("{:.2%}".format(abs(item)))
    f.write(' : ')
    f.write(str(S))
    f.close()
    return

def job(ID):
    global T
    tag=T[ID]
    M=[]
    print("MC ID:",ID,"Started")
    try:
        _initM(M)
    except ValueError as e:
        print(e)
        return

    f=open(IFILE+str(tag),"r")
    line=f.readline()
    li=[]
    while(line):
        li.append(getCATid(CAT,line[:-1]))
        if line=='\n':
            for it in li:
                for et in li:
                    if it <len(CAT)+2 and et<len(CAT)+2:
                        if it != et:
                            M[it][et]+=1
                            
            li=[]
        line=f.readline()
    f.close()
    #print(M)
    M=M1_prob_trans(M)
    #print(M)
    M_S=M1_SS(M)
    #print(M_S,np.sum(M_S))
    write(M_S,ID,np.sum(M_S))
    print("MC ID:",ID,"Complete")

def _initT(ID,SUP):
    global T, IFILE
    files=listdir(IFILE)
    for item in files:
        if item[:3]==str(ID)+"_":
            if str(SUP) in item[8:15]:
                T.append(item)
    if len(T)==0:
        raise ValueError("T list empty")




if __name__ == "__main__":
    ID=target[0]
    SUP=target[1]
    try:
        _initT(ID,SUP)
    except ValueError as e:
        print (e)
    
    _p=[]
    v=len(T)
    #v=1    ##TEST__PURPOSE ONLY

    for i in range(v):
        _p.append(Thread(target=job,args=(i,)))
        _p[i].start()
    for i in range(v):
        _p[i].join()
