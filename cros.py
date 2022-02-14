from operator import itemgetter
from os.path import exists, isfile
from os import listdir
from LDA import traverse
from extra_func import getCATid,getURLrefFromTree,readFI
from _CAT import CAT as CAT
from url_tree import UTree as UT
from _APvalues import min_sup as min_sup
from _APvalues import min_conf as min_conf

#IDIR="un_res/"
ADIR="a_res/"
GDIR="gen/"
ODIR="comp/cros/"

_L=[]
_L2=[]
D=[{},{},{}]
_Ulist=[{},{}]
Count=[{},{},{}]
T=UT()

def getUrl(num):
    global _Ulist
    temp=_Ulist[1][int(num)]
    if temp[len(temp)-1]=="\n":
        temp=temp[:-1]
    return temp
            
def _fCheck(ID):
    global ADIR, _L, _L2
    L=listdir(ADIR)
    flag=[False,False,False]
    flag2=False
    for l in L:
        ls=l.split("_")
        if ls[0]==str(ID):
            if "fi" in ls[4]:
                flag[int(ls[1])]=True
                _L.append(l)
    L=listdir(GDIR)
    for l in L:
        ls=l.split("_")
        if ls[0]==str(ID):
            if ls[1]=="IN":
                flag2=True
                _L2.append(l)
                break
    if not flag2:
        return False

    for f in flag:
        if f==False:
            return False
    return True
def _initUl(ID):
    global _L2,ADIR, _Ulist,T
    T.readTree(GDIR+_L2[0])
    getURLrefFromTree(_Ulist[0],_Ulist[1],T.head)

def addItems(li,a):
    global Count
    n=len(li)
    it=Count[a].get(n)
    if not it:
        Count[a][n]=1
    else:
        Count[a][n]+=1

    for l in li:
        addItem(l,a,li)
    return
def addItem(item,a,li=[]):
    global D
    it=D[a].get(item)
    if not (it):
        D[a][item]=[1,[]]
        if li:
            D[a][item][1].append(li)
    else:
        it[0]+=1
        if len(li)!=0:
            it[1].append(li)
    return

def readFile(tag,a):
    global ADIR
    L=[]
    s=ADIR+tag
    readFI(s,L)
    for l in L:
        addItems(l,a)
 
    
    return
def writeFile(tag,a):
    global D, ODIR
    s=ODIR+tag.split("txt")[0][:-1]+"_g.txt"
    f=open(s,'w')
    if not f:
        print("Error creating file to write",s)
    for key, item in D[a].items():
        f.write(str(key))
        f.write(" ")
        url=getUrl(key)
        f.write(url)
        f.write("\n")
        f.write("----> ")
        f.write(str(item[0]))
        f.write(" : ")
        for i,it in enumerate(item[1]):
            if i!=0:
                f.write(" ")
            for j,e in enumerate(it):
                if j==0:
                    f.write("[")
                else:
                    f.write(",")
                f.write(str(e))
                if j==len(it)-1:
                    f.write("]")

        f.write("\n")

    f.close()
def writeLU(ID):
    global _Ulist, ODIR
    s=ODIR+str(ID)+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+"_LU.txt"
    f=open(s,'w')
    if not f:
        print("Error opening file:",s)
        return
    for key,val in _Ulist[0].items():
        f.write(str(val[0]))
        f.write(" : ")
        f.write(str(val[1]))
        f.write(" : ")
        f.write(str(key))
        f.write("\n")

    f.close()
def common_check(ID,num):
    global D,ODIR
    if num!=0 and num!=1:
        print("Error in param sent")
        return
    s=str(ID)+"_"
    s2=s
    if num==0:
        s+="E-B"+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+".txt"
        s1="E: "
        s2+= "E_ONLY"+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+".txt"
    elif num==1:
        s+="C-B"+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+".txt"
        s1="C: "
        s2+="C_ONLY"+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+".txt"
    f=open(ODIR+s,'w')
    f2=open(ODIR+s2,'w')
    for key,item in D[num].items():
        _f=None
        _f=D[2].get(key)
        if _f:
            f.write(str(key))
            f.write(" ")
            url=getUrl(key)
            f.write(str(getCATid(CAT,url)))
            f.write(" ")
            f.write(url)
            f.write("\n")
            f.write(s1)
            for i,it in enumerate(item[1]):
                if i!=0:
                    f.write(" ")
                for j,e in enumerate(it):
                    if j==0:
                        f.write("[")
                    else:
                        f.write(",")
                    f.write(str(e))
                    if j==len(it)-1:
                        f.write("]")
            f.write("\n")
            f.write("B: ")
            for i,it in enumerate(_f[1]):
                if i!=0:
                    f.write(" ")
                for j,e in enumerate(it):
                    if j==0:
                        f.write("[")
                    else:
                        f.write(",")
                    f.write(str(e))
                    if j==len(it)-1:
                        f.write("]")
            f.write("\n")
            f.write("\n")
        else:
            f2.write(str(key))
            f2.write(" ")
            url=getUrl(key)
            f2.write(str(getCATid(CAT,url)))
            f2.write(" ")
            f2.write(url)
            f2.write("\n")
            f2.write(s1)
            for i,it in enumerate(item[1]):
                if i!=0:
                    f2.write(" ")
                for j,e in enumerate(it):
                    if j==0:
                        f2.write("[")
                    else:
                        f2.write(",")
                    f2.write(str(e))
                    if j==len(it)-1:
                        f2.write("]")
            f2.write("\n")
            f2.write("\n")
    f.close()
    f2.close()
    return
def onscreen():
    global D
    _olr=["ENGLISH", "CHINESE","BOTH"]
    cflag=False
    lflag=False
    
    while True:
        ch=-1
        s=input("Enter Command: ")
        s=s.split(" ")
        try:
            ch=int(s[0])
        except:
            pass
        if len(s)>1:
            for i,op in enumerate(s):
                if i==0:
                    continue
                if op.upper()=="-S":
                    cflag=True
                if op.upper()=="-L":
                    lflag=True

        if ch==-1:
            break
        print()
        for i in range(3):
            it=D[i].get(str(ch))
            if it:
                cArr=[0 for i in range(len(CAT)+2)]
                url=getUrl(ch)
                ccount={}
                print(_olr[i],"("+str(len(it[1]))+") CAT:",str(getCATid(CAT,url))+":")
                for iit in it[1]:
                    n=len(iit)
                    ll=ccount.get(n)
                    if ll:
                        ccount[n]+=1
                    else:
                        ccount[n]=1

                    for iiit in iit:
                        url2=getUrl(iiit)
                        if iiit != str(ch):
                            cArr[getCATid(CAT,url2)]+=1
                        print(iiit,url2)
                    print()
                print(_olr[i],cArr,sum(cArr))
                print(ccount)
                input()    
                

if __name__ =="__main__":
    ID=int(input("Target:"))
    print("Target:",ID)
    if not _fCheck(ID):
        print("Error fCheck")
        quit()
    print("_L:",_L)    
    _initUl(ID)
    writeLU(ID)
    
    
    for i,item in enumerate(_L):
        readFile(item,i)
        writeFile(item,i)
    
    common_check(ID,0)
    common_check(ID,1)
    print("Num of frequent item of len:")
    _o=[list(Count[0].items()),list(Count[1].items()),list(Count[2].items())]
    for i in range(len(_o)):
        _o[i].sort(key=itemgetter(0),reverse=False)
    _ol=["ENGLISH","CHINESE","BOTH"]
    for i in range(len(_o)):
        print("FOR",_ol[i])
        for c, ii in _o[i]:
            print(c,":",ii)
        
    
    print("COMPLETE...")
    ch=0
    try:
        ch=int(input("Type 1 on screen checking:"))
    except:
        pass
    if ch ==1:
        onscreen()
    
