from os.path import isfile,exists
from os import listdir, mkdir, remove
from delim import SPLIT_PARAM as SPLIT_PARAM
from delim import SPLIT_PARAM2 as SPLIT_PARAM2
from multiprocessing import Process

IDIR="gen/o/"
OCDIR="gen/cat/co/"
OEDIR="gen/cat/env/"
ICCFILE="cc.txt"

L=[]        ## List of items to work on
CC=[]       ## Country to IP range

_eIP={}     ## existing IP......hash map to eliminate research for previously seen IPs

def _getCC():
    global ICCFILE, CC
    try:
        f=open(ICCFILE,"r")
    except:
        return False
    lines=f.readlines()
    for line in lines:
        if line[len(line)-1]=="\n":
            line=line[:-1]
        line=line.split(",")
        line[0]=line[0].split(".")
        line[1]=line[1].split(".")
        

        CC.append(line)
    f.close()

    return True

def _init(ID):
    global IDIR, ODIR, L
    if not exists(IDIR):
        print("In directory doesnt exist",IDIR)
        return False
    if not exists(OCDIR):
        print("Out dir doesnt exists",OCDIR)
        return False
    if not exists(OEDIR):
        print("Out dir doesnt exists",OEDIR)
        return False
    if not _getCC():
        print("Error setting up CC file")
        return False
    l=listdir(IDIR)
    for item in l:
        if "_Tree"in item:
            continue
        if "_ENV"in item:
            continue
        if str(ID) == item.split("_")[0]:
            L.append(item)
    if len(L)==0:
        print("No target found ID:",ID)
        return False
    return True

def sep_by_ip():
    return
def sep_by_env():
    return
def findC(ip,CC):
    ip_v=None
    temp=ip.split('.')
    if len(temp)==4:
        ip=temp
        ip_v=4
    else:
        temp=ip.split(":")
        if len(temp)==8:
            ip=temp
            ip_v=6
            
    if ip_v==4:
        for item in CC:
            if int(ip[0])>=int(item[0][0]) and int(ip[0])<=int(item[1][0]):
                if int(ip[1])>=int(item[0][1]) and int(ip[1])<=int(item[1][1]):
                    if int(ip[2])>=int(item[0][2]) and int(ip[2])<=int(item[1][2]):
                        if int(ip[3])>=int(item[0][3]) and int(ip[3])<=int(item[1][3]):
                            return item[2]
    elif ip_v==6:
        return "v6Other"      ## Testing purpose until we have Ipv6 search capabilities
    else:
       
        return "NA"
    return "Other"
def mk_dirs(ID):
    global OCDIR
    _s=set(val[2] for val in CC)
    print("Different countries in list:",len(_s))
    for item in _s:
        if not exists(OCDIR+item):
            try:
                mkdir(OCDIR+item)
            except:
                return False
        else:
            l=listdir(OCDIR+item)
            for it in l:
                if isfile(OCDIR+item+'/'+it):
                    if str(ID) ==it.split("_")[0]:
                        try:
                            remove(OCDIR+item+'/'+it)
                        except:
                            return False

    return True

def job(ID,tag,CC):
    global IDIR,OCDIR
    _eIP={}
    print("Job ID:",tag,"working...")
    f=open(IDIR+tag,"r")
    if not f:
        print("ID",tag,"Error opening file",IDIR+tag)
        return
    line=f.readline()
    FID=0
    while line:
        line=line.split(SPLIT_PARAM)
        ip=line[0]
        flag=False
        country=_eIP.get(ip)
       
        if not country:
            flag=True
            country=findC(ip,CC)
        if flag:
            _eIP[ip]=country
            FID+=1
        line=f.readline()
    f.close()
   

    f=open(IDIR+tag,"r")
    f2=open(IDIR+tag.split(".")[0]+"_ENV.txt","r")
    if not f:
        print("ID",tag,"Error opening file",IDIR+tag)
        return
    line=f.readline()
    line2=f2.readline()
    while line:
        line_sep=line.split(SPLIT_PARAM)
        ip=line_sep[0]
        country=_eIP.get(ip)
        w=open(OCDIR+country+'/'+tag,'a')
        w.write(line)
        w.close()
        w2=open(OCDIR+country+'/'+tag.split(".")[0]+"_ENV.txt",'a')
        w2.write(line2)
        w2.close()
        line=f.readline()
        line2=f2.readline()
    f.close()
    f2.close()
    
    f3=open(IDIR+tag.split(".")[0]+"_Tree.txt","r")
    w3=open(OCDIR+tag.split(".")[0]+"_Tree.txt",'w')
    line=f3.readline()
    while line:
        w3.write(line)
        line=f3.readline()
    f3.close()
    w3.close()
    print("ID",ID,":",tag,"Finish...")
    return

if __name__ =="__main__":
    ID=int(input("Enter ID: "))
    if not _init(ID):
        quit()
    if not mk_dirs(ID):
        print("Failed to make necesary directories")
        quit()
    print(L)
    _p=[None for i in range(len(L))]
    for i in range(len(_p)):
        _p[i]=Process(target=job, args=(ID,L[i],CC,))
        _p[i].start()
    
    for i in range(len(_p)):
        _p[i].join()

    #job(ID,L[0])