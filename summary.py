from operator import itemgetter
from url_tree import UTree as UT
from multiprocessing import Process
from copy import deepcopy
from extra_func import getCATid, getDiv, getURLrefFromLU, readFI
from _CAT import CAT as CAT
from _APvalues import min_sup as min_sup
from _APvalues import min_conf as min_conf

PATH="gen/" 
SPATH="comp/cros/"
APATH="a_res/"
_U2N={}
_N2U={}
TOPnPAGES=10

alpha=0.1
beta=0.5
CAT2=deepcopy(CAT)

def _init_CAT(C_T):
    global CAT2
    for i in range(len(CAT2)):      ##Total hits for Categories
         C_T.append(0)

def _init_FI(ID,FI,_i):
    global CAT,APATH
    s=APATH+str(ID)+"_"+str(_i)+"_SUP"+str(min_sup)+"_CON"+str(min_conf)+"_fi.txt"
    lines=[]
    readFI(s,lines)
    for line in lines:
        FI.append(line)


def _init_from_LU(ID,_pages):                ##GEt all page and hits from LU table
    global SPATH
    
    s=SPATH+str(ID)+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+"_LU.txt"
    f=open(s,"r")
    if not f:
        print("ERROR File not Found",s)
        return
        
    lines=f.readlines()
    for line in lines:
        line=line.split(" : ")
        if len(line)<3:
            continue
        for ii in range(len(line)):
            while line[ii][len(line[ii])-1]==" " or line[ii][len(line[ii])-1]=="\n":
                line[ii]=line[ii][:-1]
            while len(line)>0 and (line[ii][0]==" " or line[ii][0]=="\n"):
                line[ii]=line[ii][1:]
        #print(line[2],getCATid(CAT,line[2]))

        #input()
        _pages.append([line[2],int(line[1])])
       #index,tmp._Hits,div
           # C_T[]+=int(line[1])
    f.close()
    
def _init_from_Tree(L,tmp=None,strs=[]):       ##Gets page and  Hits from Tree
    if not tmp:
        print("tmp is NULL")
        return
    strs=deepcopy(strs)
    strs.append(tmp.name)

    s=""
    for each in strs:
        s+=each+"/"
    #print(s)
    if tmp.id:
        L.append([s,tmp._Hits])
 

    if len(tmp.child)==0:
        return

    for each in tmp.child:
        _init_from_Tree(L,each,strs)
def print_CT(C_T):
    tot=sum(C_T)
    C_T2=[]
    for i,each in enumerate(C_T):
        C_T2.append([CAT2[i][0],int(each)])
    C_T2.sort(key=itemgetter(1),reverse=True)
    
    print("Total:",tot)
    print("%3s %20s %10s %10s"%("ID","Category","No","Prob"))
    for i,each in enumerate(C_T2):
        print("%3d %20s %10d %10f"%(i, each[0],each[1],each[1]/tot))
def FI_by_CAT2(_pages,_i=0):    
    global CAT                 
    C_T=[]

    print(ID,"-",_i,"Total Hits per Category Results")
    print_CT(C_T)
def Hits_by_CAT(pages,_i=0):
    global CAT
    div_s=["E","C","B"]
    C_T=[]
    _pag=[]
    _init_CAT(C_T)
    for each in pages:
        if getDiv(each[0],div_s[_i]):
            C_T[getCATid(CAT,each[0])]+=each[1]
            _pag.append(deepcopy(each))

    print(ID,"-",_i,"Total Hits per Category Results")
    print_CT(C_T)
    
    print()
    
    tot=sum(C_T)
    for i in range(len(_pag)):
        topic_prob=(C_T[getCATid(CAT,_pag[i][0])] + alpha)/(tot + ((len(C_T)-1)*alpha))
        page_prob_given_topic=(_pag[i][1] + beta )/(C_T[getCATid(CAT,_pag[i][0])] + ((len(C_T)-1)*beta))
        ## Page probabilty may be wrong
        ## i think it  should be length of words * beta 
        ## i currently have length of topics * beta (2021.Dec.19)
        final_page_prob=topic_prob*page_prob_given_topic
        ## TO print Uncategorized
        ##if getCATid(CAT,_pag[i][0])==len(CAT)+1:
            ##print(_pag[i][0] ,_pag[i][1])
        #print(i)
        _pag[i].append(final_page_prob)
    
    _pag.sort(key=itemgetter(2),reverse=True)
    print(ID,"-",_i,"LDA top("+str(TOPnPAGES)+") pages probability")
    for i in range(TOPnPAGES):
        try:
            print(_pag[i])
        except:
            break

def FI_by_CAT(FI,_i):
    global _N2U, CAT
    C_T=[]
    _init_CAT(C_T)
    for each in FI:
        for e in each:
            C_T[getCATid(CAT,_N2U.get(int(e)))]+=1
            
    print()
    print(ID,"-",_i,"FI Hits per Category")
    print_CT(C_T)

def job(_pages,ID=10,_i=0):
    global CAT
    global alpha, beta
    print(ID,"-",_i,"Summary Start")
    #Hits_by_CAT(ID,_i)

    Hits_by_CAT(_pages,_i)
    FI=[]
    _init_FI(ID,FI,_i)
    FI_by_CAT(FI,_i)
    
    
    
    
    #print(FI)
    

    print(ID,"-",_i,"Summary Complete")
if __name__=="__main__":
    CAT2.append(["Home page"])
    CAT2.append(["Uncategorized"])

    ID=int(input("ID: "))
    i =0
    _p=[None,None,None]
    
    _pages=[]
    _init_from_LU(ID,_pages)
    
    s=SPATH+str(ID)+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+"_LU.txt"
    getURLrefFromLU(_U2N,_N2U,s)
    #U=UT()
    #U.readTree(PATH+str(ID)+"_IN_Tree.txt")
    #_init_from_Tree(_pages,U.head)         ##Read in from tree

    #_p=[None]           ##TESTING PURPOSES ONLY
    for i in range(len(_p)):
        #_p[i]=Process(target=job, args=(ID,i))
        #_p[i].start()
        print()
        job(_pages,ID,i)
        print()
        print()
    #for i in range(len(_p)):
        #_p[i].join()


