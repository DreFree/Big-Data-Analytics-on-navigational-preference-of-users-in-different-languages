from operator import itemgetter
from url_tree import UTree as UT
from multiprocessing import Process
from copy import deepcopy
from extra_func import getCATid, getDiv
from _CAT import CAT as CAT


PATH="gen/" 
SPATH="comp/cros/"


alpha=0.1
beta=0.5
CAT2=deepcopy(CAT)

def _init_CAT(C_T):
    global CAT2
    print("len(CAT):",len(CAT2))
    for i in range(len(CAT2)):      ##Total hits for Categories
         C_T.append(0)

def getALLURL(ID,C_T,i):                ##GEt allURL per Language (E,C or B)
    global SPATH
    div_s=["E","C","B"]
    s=SPATH+str(ID)+"_LU.txt"
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
        if getDiv(line[2],div_s[i]):
            C_T[getCATid(CAT,line[2])]+=int(line[1])
    f.close()
    
def traverse(C_A,L,tmp=None,strs=[]):
    if not tmp:
        print("tmp is NULL")
        return
    strs=deepcopy(strs)
    strs.append(tmp.name)
    flag=False

    s=""
    for each in strs:
        s+=each+"/"
    #print(s)
    if tmp.id>=1:
        index=getCATid(CAT,s)
        L.append([s,index,tmp._Hits])
        C_A[index]+=tmp._Hits
        flag=True

    if len(tmp.child)==0:
        if not flag:
            index=getCATid(s)
            L.append([s,index,tmp._Hits])
            C_A[index]+=tmp._Hits
        return

    for each in tmp.child:
        traverse(C_A,L,each,strs)

def job(ID=10,_i=0):
    global PATH, CAT
    global alpha, beta
    print(ID,"-",_i,"LDA Start")
    C_T=[]
    _pages=[]
    _init_CAT(C_T)

    U=UT()
    U.readTree(PATH+str(ID)+"_IN_Tree.txt")
    U.counter=0
    U.genId()
    U.equalizer()
    
    ##traverse(C_T,_pages,U.head)
    getALLURL(ID,C_T,_i)
    tot=sum(C_T)
    print(ID,"-",_i,"LDA Results")
    print("Total:",tot)
    
    print("%3s %20s %10s %10s"%("ID","Category","No","Prob"))
    for i,each in enumerate(C_T):
        print("%3d %20s %10d %10f"%(i, CAT2[i][0],each,each/tot))
    
    print()
    for i in range(len(_pages)):

        topic_prob=(C_T[_pages[i][1]] + alpha)/(tot + ((len(C_T)-1)*alpha))
        page_prob_given_topic=(_pages[i][2] + beta )/(C_T[_pages[i][1]] + ((len(C_T)-1)*beta))
        final_page_prob=topic_prob*page_prob_given_topic
        ## Need to add the Gibbs alpha nad K, Beta and V params
        _pages[i].append(final_page_prob)
    _pages.sort(key=itemgetter(3),reverse=True)

    for i in range(20):
        try:
            print(_pages[i])
        except:
            break

    print(ID,"-",_i,"LDA Complete")
if __name__=="__main__":
    CAT2.append(["Home page"])
    CAT2.append(["Uncategorized"])

    ID=int(input("ID: "))
    i =0
    _p=[None,None,None]
    #_p=[None]           ##TESTING PURPOSES ONLY
    for i in range(len(_p)):
        #_p[i]=Process(target=job, args=(ID,i))
        #_p[i].start()
        job(ID,i)
        print()
    #for i in range(len(_p)):
        #_p[i].join()


