from multiprocessing import Process
from threading import Thread, Semaphore
from os import getpid
from os.path import exists, isfile
from os import listdir
from url_tree import UTree
import psutil

IFILE="a_res/r/"
TFILE="gen/"
OFILE="un_res/"

L=[]
L_sem = []
TAR_FI=[]
T=[UTree(),UTree(),UTree()]

def readFI(ID,div):
    global IFILE, L , T, TAR_FI, L_sem
    L_sem[ID].acquire()
    tag=TAR_FI[ID]
    f=open(IFILE+str(tag),"r")
    if not f:
        raise ValueError("File not exist")
    print("ID:",ID,"UNDO: READ tree:",tag,"Started")
    line=f.readline()
    while line:
        items=line.split(' ')
        items=items[:-1]
        for it in items:
            temp=[]
            it=it[1:-1]
            it=it.split(',')
            for et in it:
                node, st =T[div].getNodebyId(int(et))
                temp.append(st)
            L[ID].append(temp)
        line=f.readline()
    f.close()
    print("ID:",ID,"UNDO: READ tree:",tag,"Complete")
    L_sem[ID].release()
    

def writeFI(ID):
    global L, TAR_FI, L_sem
    L_sem[ID].acquire()
    tag=TAR_FI[ID]
    if len(L[ID])==0:
        print("no items")
        L_sem[ID].release()
        return
    print("ID:",ID,"UNDO: WRITE:",tag,"Started")
    OUT=open(OFILE+tag[:-6]+"undofi.txt","w",encoding="utf-8")
    if not (OUT):
        print("Error creating file for write",OFILE+tag[:-6]+"undofi.txt")
        L_sem[ID].release()
        return
    for items in L[ID]:
        for j,item in enumerate (items):
            if j>0:
                OUT.write('\n')
            OUT.write(item)
        OUT.write('\n\n')
    
    OUT.close()
    print("ID:",ID,"UNDO: WRITE:",tag,"Complete")
    L_sem[ID].release()
    return

def loadTrees(ID):
    global T, TFILE
    
    ufiles=listdir(TFILE)
    files=[]
    for tmp in ufiles:
        tmp_2=tmp.split("_")
        if str(ID) == tmp_2[0]:
            if "Tree" in tmp:
                files.append(tmp)
            
    print("Loading tree(s):")
    print(files)
    if len(files)==0:
        raise ValueError("No files detected: ID:",ID)

    _p=[None,None,None]
    for i in range(len(_p)):
        _p[i]=Thread(target=T[i].readTree,args=(TFILE+files[i],))
        L.append([])
        _p[i].start()
    for i in range(len(_p)):
        _p[i].join()
    if not(T[0].head) or not(T[1].head) or not(T[2].head):
        raise ValueError("Error initializing tree(s)")

    print("Trees Load complete.")
    return

def getFITargets(ID,SUP):
    global TAR_FI, IFILE
    pot=listdir(IFILE)
    for p in pot:
        p1=p.split("_")
        if p1[0]==str(ID):
            if str(SUP) in p1[2]:
                if str("fi") in p1[4]:
                    TAR_FI.append(p)

    if len(T)==0:
        raise ValueError("no Targets set")
    return


if __name__=="__main__":
    if (not exists(OFILE)):
        print(OFILE, "Directory Doesnt exists.")
        quit()
    if (not exists(IFILE)):
        print(IFILE, "Directory Doesnt exists")
        quit()
    if (not exists(TFILE)):
        print(TFILE, "Directory Doesnt exists")
        quit()

    
    target=(5,0.0015)
    try:
        loadTrees(target[0])
        getFITargets(target[0],target[1])
    except ValueError as e:
        print(e)
        quit()

    _p2=[]
    _p=[]
    #print(TAR_FI)
    for i in range(len(TAR_FI)):
        L.append([])
        L_sem.append(Semaphore())
        _p.append(Thread(target=readFI,args=(i, int(TAR_FI[i].split("_")[1]),)))
        
        _p[i].start()
 
    for i in range(len(TAR_FI)):
        _p2.append(Thread(target=writeFI,args=(i,)))
        _p2[i].start()

    for i in range(len(TAR_FI)):
        _p[i].join()
        _p2[i].join()
    print()
    #print(L[0])