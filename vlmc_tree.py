from math import log2,log
from copy import deepcopy
from url_tree import UTree 
from operator import itemgetter

class VNode:
    def __init__(self,label):
        if isinstance(label,str):
            self.L=label       ##VNode label
            self.n=1    	    ##VNode hits
            self.p=None 	    ##VNode Probability to this node
            self.p2=None		##VNode Tree overal tree probability
            self.kl=None		##VNode Kullback-Leibler divergence param
            self.child=[]
        else:
            print("ERRror: VNode Expected type str for labels")
            self.L=None
            self.n=None
            self.p=None
            self.p2=None
            self.kl=None
            self.child=[]
    ##Since this structure will represent a VLMC, n represent the number of time the 
    ## substring to this postion have been seen. Same rule applies for p - probabilty
    def hit(self):
        if self.n:
            self.n+=1
        else:
            print("Error: VNode n not properly set")
        return

class VTree:
    k=None
    Q=None
    def __init__(self):
        self.isRES=False
        self.head=None
        self.isKL_mode=False
        self.isCWKL_mode=False
        self.RES=[]
        if not VTree.k:
            raise ValueError("VTree k not set")
        if not VTree.Q:
            raise ValueError("VTree Q not set")

    def _addItem(self,tmp,item,i,n):
        if i>n:
            return False
        if len(tmp.child)>0:
            for ech in tmp.child:
                if ech.L==item[i]:
                    #print("s:",item[i])
                    U=self._addItem(ech,item,i+1,n)
                    ech.hit()
                    return True
                    
        
        t=VNode(item[i])
        tmp.child.append(t)
        U=self._addItem(tmp.child[len(tmp.child)-1],item,i+1,n)
 
        return True

    def addItem(self,L,hit=0):						
        if not isinstance(L, list):
            print("Expected L as type list")
            return False
        n=len(L)-1
        if "*"!=L[0]:
            print("Expected starting symbol as '*'")
            return False
        if self.head:
            self.head.hit()
        else:
            self.head=VNode("*")
        U=self._addItem(self.head,L,0+1,n)
        return

    def genprobCWKL(self,tmp=None):
        if not(self.head):
            print("Context-Tree is empty")
            return
        if not tmp:
            tmp=self.head
            tmp.p=1.0
            tmp.p2=1.0
        tmp.kl=0.0
        temp_wp=0.0
        for i in range(len(tmp.child)):
            tmp.child[i].p=(tmp.child[i].n/tmp.n)
            tmp.child[i].p2=tmp.child[i].p*tmp.p2
            tmp.kl=(((tmp.child[i].p2*log(tmp.child[i].p2/tmp.child[i].p))-tmp.child[i].p2+tmp.child[i].p)*tmp.child[i].n)+tmp.kl
            temp_wp+=tmp.child[i].n*tmp.child[i].p
            tmp.kl=tmp.kl/temp_wp
            ##Corrected Weighted Kullback-Leibler (CWKL) Divergence
            
            self.genprobCWKL(tmp.child[i])
        self.isCWKL_mode=True
    def genprobKL(self,tmp=None):
        if not(self.head):
            print("Context-Tree is empty")
            return
        if not tmp:
            tmp=self.head
            tmp.p=1.0
            tmp.p2=1.0
            tmp.kl=0.0

        temp_wp=0.0
        for i in range(len(tmp.child)):
            tmp.child[i].p=(tmp.child[i].n/tmp.n)
            tmp.child[i].p2=tmp.child[i].p*tmp.p2
            
            tmp.child[i].kl=(tmp.child[i].p2 * log2(tmp.p2/tmp.child[i].p2))+tmp.kl
            ##Accumultaed information gain above including parents information gain into children
            
           
            ##Kullback-Leibler (KL) Divergence
            ##log() parameter inverted to gain positiv vale for kl divergence
            self.genprobKL(tmp.child[i])
        self.isKL_mode=True
    def prune(self,tmp=None):
        
        if not(self.head):
            print("context-Tree is empty")
            return True
        if (self.isKL_mode and self.isCWKL_mode)or(not self.isKL_mode and not self.isCWKL_mode):   
            print("Error both mode enabled/disabled",self.isKL_mode,self.isCWKL_mode)
            return

        if not tmp:
            self.p_tot=1
            self.p_num=0
            tmp=self.head
        i=0
        while i<len(tmp.child):
            each=tmp.child[i]
            #print(each.L)
            self.p_tot+=1
            if (self.prune(each)):
                if self.isKL_mode:
                    if (each.kl<VTree.k):
                        i-=1
                        self.p_num+=1
                        #print(each.L,each.n,each.kl)
                        tmp.child.remove(each)
                elif self.isCWKL_mode:
                    if (each.kl<VTree.k):
                        i-=1
                        self.p_num+=1
                        #print(each.L,each.n,each.kl)
                        tmp.child.remove(each)
            i+=1   	
                
        if len(tmp.child)==0:
            return True
        else:
            return False
    def _show_pruneamt(self):
       return str("Evaluated:"+str(self.p_tot)+" | Pruned:"+str(self.p_num)+" - "+str(self.p_num/self.p_tot))
    def showTree(self,i=0,curr=None,jj=-1):
        if i==0:
            curr=self.head
        if jj!=-1:
            if i==jj:
                return

        for j in range(i):
            print("|---",end="")
        print(">",end="")
        print(curr.L,end="")
        print("    #"+str(curr.n),str(curr.p2)," | ",str(curr.kl),end="")
        print()
        for each in curr.child:
            self.showTree(i+1,each,jj)
    def genResults(self,f=-1,t=-1,tmp=None,L=[]):
        if not self.head:
            print("Context tree is empty")
            return
        if not VTree.Q:
            print("static Q not initialized")
            return
        if not tmp:
            tmp=self.head
        L=deepcopy(L)
        L.append(tmp.L)
        if len(tmp.child)==0:
            return
        l=len(L)-1
        if (f==-1 or l>=f) and (l<=t or t==-1):
            if tmp.p2>=VTree.Q:
                self.RES.append([L,tmp.kl, tmp.n])

        for each in tmp.child:
            self.genResults(f,t,each,L)
        if tmp==self.head:
            self.isRES=True
            self.RES.sort(key=itemgetter(2),reverse=False)

    def showResults(self):      ##Use after genResults
        if not self.isRES:
            print("Results not generated")
            return
        ##self.isRES=False
        
        for each in self.RES:
            print(each)
        #self.RES.clear()

    def writeResults(self,OUTFILE):
        if not self.isRES:
            print("Results not generated")
            return
        F=open(OUTFILE,"w")
        if not F:
            print("Error creating file",OUTFILE)
            return
        ##self.isRES=False
        self.RES.sort(key=itemgetter(2),reverse=True)
        for i,each in enumerate(self.RES):
            if i!=0:
                F.write("\n")
            for j,it in enumerate(each):
                if j!=0:
                    F.write(" ")
                if j==2:
                    F.write("#")

                F.write(str(it))
        F.close()
        
        #self.RES.clear()

if __name__ =="__main__":
    L=["*","2","1","3","4","5"]
    L2=["*","2","1","2","4","5"]
    L3=["*","1","6","2","4","5"]
    k=0.7
    VTree.k=k
    VTree.Q=0.00000001
    try:
        v1 = VTree()
    except ValueError as e:
        print(e)
        quit()
	    
    v1.addItem(L)
    v1.addItem(L2)
    v1.addItem(L2)
    v1.addItem(L3)
    print("prune factor:",k)
    v1.genprobKL()
    v1.showTree()
    print("SHOWing tree jj=2")
    v1.showTree(jj=2)
    print("########")
    v1.prune()
    print(v1._show_pruneamt())
    v1.showTree()
    v1.genResults()
    v1.showResults()
    v1.writeResults("try_VLMC.txt")
    print("End...")
