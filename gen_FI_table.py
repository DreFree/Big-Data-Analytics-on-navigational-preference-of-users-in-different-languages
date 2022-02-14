from _APvalues import min_sup as min_sup
from _APvalues import min_conf as min_conf
from extra_func import readFI,getURLrefFromLU

APATH="a_res/"
CPATH="comp/cros/"
N=3

_L=[[],[],[]]
U2N={}
N2U={}

def _initFI(ID):
    global _L, APATH,N
    for i in range(N-1,-1,-1):
        s=APATH+str(ID)+"_"+str(i)+"_SUP"+str(min_sup)+"_CON"+str(min_conf)+"_fi.txt"
        readFI(s,_L[i])
        print(i)
def _initLU(ID):
    global U2N, N2U,CPATH
    s=CPATH+str(ID)+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+"_LU.txt"
    getURLrefFromLU(U2N,N2U,s)

def writeUniques(ID):
    global _L,CPATH,N2U
    
    
    for i in range(len(_L)):
        s=CPATH+str(ID)+"_"+str(i)+"_SUP"+str(min_sup)+"_CONF"+str(min_conf)+"_FI_LU.csv"
        f=open(s,"w")
        if not f:
            print("Error creating file to write",s)
            continue
        dic={}
        for j in range(len(_L[i])-1,-1,-1):
            
            for k in range(len(_L[i][j])-1,-1,-1):
                u=dic.get(_L[i][j][k])
                if not u:
                    dic[_L[i][j][k]]=1
                    if len(dic.items())!=1:
                        f.write("\n")
                    f.write(_L[i][j][k])
                    f.write(",")
                    U=N2U.get(int(_L[i][j][k]))
                    if not U:
                        print("ID not found")
                        f.write("not found")
                    else:
                        if U[len(U)-1]=="\n":
                            U=U[:-1]
                        f.write(U)
                else:
                    dic[_L[i][j][k]]+=1
        f.close()

    return
if __name__=="__main__":
    ID=10
    try:
        ID=int(input("Target: "))
    except:
        print("Error in input. ID default value is assigned (10)")

    _initFI(ID)
    _initLU(ID)
    print(_L[0][len(_L[0])-1])
    writeUniques(ID)