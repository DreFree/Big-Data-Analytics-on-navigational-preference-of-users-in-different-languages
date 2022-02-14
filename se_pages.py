from extra_func import getCATid, readSess, getURLrefFromLU
from _CAT import CAT as CAT
from os.path import exists
from operator import itemgetter
from _APvalues import min_conf as min_conf
from _APvalues import min_sup as min_sup
from copy import deepcopy

IPATH="gen/"
SPATH="comp/cros/"

M=[[],[],[]]
_U2N={}
_N2U={}

CAT2=deepcopy(CAT)

def _init_CAT(C_T):
    global CAT2
    for i in range(len(CAT2)):      ##Total hits for Categories
         C_T.append(0)
def print_CT(C_T):
    tot=sum(C_T)
    if tot==0:
        return
    C_T2=[]
    for i,each in enumerate(C_T):
        C_T2.append([CAT2[i][0],int(each)])
    #C_T2.sort(key=itemgetter(1),reverse=True)
    
    print("Total:",tot)
    print("%3s %20s %10s %10s"%("ID","Category","No","Prob"))
    for i,each in enumerate(C_T2):
        print("%3d %20s %10d %10f"%(i, each[0],each[1],each[1]/tot))

def _init_S(ID):
    global M,IPATH
    s=IPATH+str(ID)+"_"
    for i in range(3):
        if not exists(s+str(i)+".txt"):
            print(s+str(i)+".txt", "NOT exist. closing...")
            return False
    for i in range(3):
        s2=s+str(i)+".txt"
        print("Loading:",s2)
        readSess(s2,M[i],True)
    

    return True

def _initFI(ID):
    global _U2N,_N2U,SPATH
    s=SPATH+str(ID)+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+"_LU.txt"
    if not exists(s):
        print("Error:",s,"Not exist")
        return False
    getURLrefFromLU(_U2N,_N2U,s)
    return True
def job(ID,mode,target=-1):
    global M, _N2U
    sp=[{},{},{}]
    ep=[{},{},{}]
    for i in range(len(M)):
        for each in M[i]:
            if mode:
                if target==-1:
                    print("ERROR: Target not set")
                    return
                flag=False
                for ea in each.S:
                    if ea.n ==int(target):
                        flag=True
                        break
                if not flag:
                    #print("ss")
                    continue
            first=each.S[0]
            last=each.S[len(each.S)-1]
            it1=sp[i].get(int(first.n))
            it2=ep[i].get(int(last.n))
            if not it1:
                sp[i][int(first.n)]=1
            else:
                sp[i][int(first.n)]+=1

            if not it2:
                ep[i][int(last.n)]=1
            else:
                ep[i][int(last.n)]+=1
        ## start pages
        val =sp[i].values()
        su=sum(val)
        counter=0
        print()
        print()
        if not mode:
            print(str(ID)+"_"+str(i),"Start pages")
        else:
            print(str(ID)+"_"+str(i),"Start pages with item","("+str(target)+") -",_N2U.get(int(target)))
        for key,val in sorted(sp[i].items(),key=itemgetter(1),reverse=True):
            print(key,':',val,val/su, _N2U.get(int(key)))
            counter+=1
            if counter>=10:
                break
        print("Total:",su)
        C_T=[]
        _init_CAT(C_T)
        for key,val in sp[i].items():
            C_T[getCATid(CAT,_N2U.get(int(key)))]+=val
        print_CT(C_T)
        print()
        ##End pages
        val =ep[i].values()
        su=sum(val)
        counter=0
        if not mode:
            print(str(ID)+"_"+str(i),"End pages")
        else:
            print(str(ID)+"_"+str(i),"End pages with item","("+str(target)+") -",_N2U.get(int(target)))
        for key,val in sorted(ep[i].items(),key=itemgetter(1),reverse=True):
            print(key,':',val,val/su, _N2U.get(int(key)))
            counter+=1
            if counter>=10:
                break
        print("Total:",su)
        C_T=[]
        _init_CAT(C_T)
        for key,val in ep[i].items():
            C_T[getCATid(CAT,_N2U.get(int(key)))]+=val
        print_CT(C_T)
    return







if __name__=="__main__":
    ch=-1
    ID=-1
    CAT2.append(["Home page"])
    CAT2.append(["Uncategorized"])
    try:
        ID=int(input("Enter ID: "))
    except:
        print("Error acepting ID.\nClosing...")
        quit()

    try:
        ch=int(input("Enter 2 for targeted start-end page analysis: "))
    except:
        pass
   
    
    if ch==2:
        print("MODE: Targeted start-end mode")    
    else:
        print("MODE: Global start-end mode")
    if not _init_S(ID):
        quit()
    if not _initFI(ID):
        quit()
    if ch==2:
        ta=-1
        try:
            ta=int(input("Enter target-num: "))
        except:
            print("ERROR: invalid target")
            quit()
        job(ID,True,ta)
    else:
        job(ID,False)
