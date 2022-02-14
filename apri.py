from threading import main_thread
from apriori_python import apriori
from mlxtend.frequent_patterns import apriori as apriori2
from mlxtend.frequent_patterns import association_rules
from extra_func import readSess, sesToarr
from multiprocessing import Process
from os import getpid
from os.path import exists, isfile, isdir
from os import listdir
import pandas as pd
import datetime
import psutil
import sys
from _APvalues import min_sup as min_sup
from _APvalues import min_conf as min_conf

IFILE="gen/"
OFILE="a_res/"
cIFILE="gen/cat/co/"
cOFILE="gen/cat/co/"
#min_sup=0.0015
#min_conf=0.85

def writeRules(ID,i,rules,co=None):
    global min_sup, min_conf,_mode,OFILE,cOFILE
    if _mode==0:
        s=OFILE+str(ID)+"_"+str(i)+"_SUP"+str(min_sup)+"_CON"+str(min_conf)+"_rules.txt"
    else:
        s=cOFILE+co+"/"+str(ID)+"_"+str(i)+"_SUP"+str(min_sup)+"_CON"+str(min_conf)+"_rules.txt"
    OUT=open(s,"w")
    if not (OUT):
        print("Error creating file for write",s)
        return
    
    for rule in rules:
        for i,item in enumerate(rule):
            if i!=0:
                OUT.write(",")
            OUT.write(str(item))
        OUT.write('\n')
    OUT.close()
def writefi(ID,i,FI,co=None):
    global min_sup,_mode,OFILE,cOFILE
    #print(type(FI))
    #print(len(FI))
    #print(FI[1])
    if _mode==0:
        s=OFILE+str(ID)+"_"+str(i)+"_SUP"+str(min_sup)+"_CON"+str(min_conf)+"_fi.txt"
    else:
        s=cOFILE+co+"/"+str(ID)+"_"+str(i)+"_SUP"+str(min_sup)+"_CON"+str(min_conf)+"_fi.txt"
    OUT=open(s,"w")
    if not (OUT):
        print("Error creating file for write",s)
        return

    for i in range(len(FI)):
        for s in FI[i+1]:
            OUT.write("[")
            for x,num in enumerate(s):
                if (x!=0):
                    OUT.write(",")
                OUT.write(str(num))
            OUT.write("] ")
        OUT.write('\n')
    OUT.close()

def apri(ID,mode,i=0,co=None):
    global min_sup, min_conf,_mode
    _mode=mode
    
    _start_time=datetime.datetime.now()
    data=[]
    if _mode==0:
        s1=IFILE+str(ID)+"_"+str(i)+".txt"
    else:
        s1=cIFILE+co+"/"+str(ID)+"_"+str(i)+".txt"
        if not exists(s1):
            print(s1,"Not exist")
            return
    readSess(s1,data,True)
    #data=[[1,2,3],[1,2,3,4],[5,6,7],[1,2,3],[1,2,3,6,7],[1,2,3,7]]              ##Testing purposes
    data=sesToarr(data)
    _end_time=datetime.datetime.now()
    print("Session#"+str(ID),"-",i,"read & array transformation Complete")
    print("Start:",_start_time)
    print("End:",_end_time)
    print("Delta:",str(_end_time-_start_time))
    print("Mem:",psutil.Process(getpid()).memory_info().rss / 1024 ** 2,"MB\n")
    print("Apriori#"+str(ID),"-",i,"- Frequent pattern discovery started...")
    _start_time=datetime.datetime.now()
    fi_set,rules=apriori(data, minSup=min_sup,minConf=min_conf)
    #fi_set2=apriori2(data,min_support=min_sup, use_colnames=True)
    #rules2=association_rule(fi_sets2,metric="confidence",main_threshold=0.85)
    _end_time=datetime.datetime.now()
    print("Apriori#"+str(ID),"-",i,"Complete")
    print("Start:",_start_time)
    print("End:",_end_time)
    print("Delta:",str(_end_time-_start_time))
    print("Mem:",psutil.Process(getpid()).memory_info().rss / 1024 ** 2,"MB\n")

    writeRules(ID,i,rules,co)
    writefi(ID,i,fi_set,co)
    
    ##print(fi_set)
    ##print(fi_set2)
if __name__=="__main__":
    mode=0
    if len(sys.argv)>1:
        if sys.argv[1].upper()=="-C":
            mode=1
    ID=2                             ##ID value for selecting specific data set
    ID=int(input("Enter ID: "))
    print("MODE:",mode)
    print("Apriori")
    print("Tagert: ",ID)
    print("Min Sup:",min_sup,"Min Conf:",min_conf)
    print()

    if mode==0:
        if (not exists(OFILE)):
            print(OFILE, "Doesnt exists.")
            quit()
        if (not exists(IFILE)):
            print(IFILE, "Doesnt exists")
            quit()

        _p=[None, None, None]
        ##_p=[None]                       ##Testing purposes
        for i in range(len(_p)):
            
            _p[i]=Process(target=apri,args=(ID,mode,i,))
            #_p[i]=Process(target=apri,args=(ID,i))
            _p[i].start()
        for i in range(len(_p)):
            _p[i].join()
    elif mode==1:   ## to do all Countries FI HERE
        l=[]
        for item in listdir(cIFILE):
            if isdir(cIFILE+item):
                l.append(item)
        for item in l:
            _p=[None, None, None]
            for i in range(len(_p)):
            
                _p[i]=Process(target=apri,args=(ID,mode,i,item))
                #_p[i]=Process(target=apri,args=(ID,i))
                _p[i].start()
            for i in range(len(_p)):
                _p[i].join()
