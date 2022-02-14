from multiprocessing import Lock
from operator import itemgetter
from os.path import exists
class UNode:
    def __init__(self, name):
        #self.lock=Lock()
        self.name=name
        self.child=[]
        self.id=None
        self._Hits=0
    def __del__(self):
    	for each in self.child:
    		#self.child.remove(each)
    		del each
    	return
    def addChild(self,value):
    	if not isinstance(value,UNode):
        	print(ValueError("expected value as UNode object"))
        	return
    	#self.lock.acquire()
    	self.child.append(value)
    	#self.lock.release()
        
    def setId(self, n):
    	if not isinstance(n,int):
    		print(ValueError("param n expected int"))
    		return
    		
    	#self.lock.acquire()
    	self.id=n
    	#self.lock.release()
    def getId(self):
    	return self.id
    	
    def hit(self):
    	#self.lock.acquire()
    	self._Hits+=1
    	#self.lock.release()
    def getHits(self):
    	#self.lock.acquire()
    	temp=self._Hits
    	#self.lock.release()
    	return temp
    def addHits(self,h):
    	#self.lock.acquire()
    	self._Hits+=h
    	#self.lock.release()
    def _hasChild(self):
        if len(self.child)==0:
            return True
        return False


class UTree:
    _curr=None
    def __init__(self,goa=True):
        if not isinstance(goa, bool):
            raise ValueError("param expected bool:",goa)
        self.head=None
        self.elements=0
        self.counter=0
        self._genOnadd=goa		## Flag to activate gen id number on addItem function
        self.lock=Lock()
	        
    def _cleanup(self, tmp):
	    if len(self.child<=0):
	    	del tmp
	    	return
	    for each in tmp.child:
	        #tmp.child.remove(each)
	        self._cleanup(each)

	    
    def __del__(self):
        if not self.head:
            return
        del self.head
			
    def _find(self, tmp, item,i,n):
        if not(tmp):
            return None
        if i==n:
            if tmp.name==item[i]:
                return tmp
            else:
            	return None

        for eac in tmp.child:
            if i+1>n:
                return None
            if eac.name==item[i+1]:
                return self._find(eac, item,i+1,n)
        
        return None
    def _str2list(self, s):
        us=s
        while (us[len(us)-1]=="/" )and len(us)>0:
        	us=us[:-1]
        	
        us=us.split('/')[2:]
        while (us[len(us)-1]=="" or us[len(us)-1]=="*" or us[len(us)-1]==" ") and len(us)>0:
            us=us[:-1]
        
        return us
    def find(self,s):
        strs=self._str2list(s)
        
        n=len(strs)-1
        if not(self.head):
            return None
        return self._find(self.head,strs,0,n) 
    
    def count_inc(self):
	    self.lock.acquire()
	    self.counter+=1
	    tmp=self.counter
	    self.lock.release()
	    return tmp
		
    def _addItem(self,tmp,item,i,n,hit=0):
        if i>n:
            return None
        if len(tmp.child)>0:
            for ech in tmp.child:
                if ech.name==item[i]:
                    #print("s:",item[i])
                    U=self._addItem(ech,item,i+1,n,hit)
                    if(not U):
                    	if hit==0:
                    		ech.hit()
                    	elif hit>0:
                    		ech.addHits(hit)
                    	                    			
                    	if self._genOnadd:
                    	    if not ech.id:
                    		    tmp2=self.count_inc()
                    		    ech.setId(tmp2)   
                    	return ech
                    else: 
                    	return U
        
        t=UNode(item[i])
        tmp.addChild(t)
        U=self._addItem(tmp.child[len(tmp.child)-1],item,i+1,n,hit)
        if(not U):
            if hit==0:
                t.hit()
            elif hit>0:
                t.addHits(hit)
           
            if self._genOnadd:	
                if not t.id:
                    tmp=self.count_inc()
                    t.setId(tmp)
            return t
        else:
        	return U

        

    def addItem(self,s,hit=0):						
        if s=="" or s=="https://": 
        	print("invalid string",s)
        	return None
        strs=self._str2list(s)
        n=len(strs)-1
        
        self.lock.acquire()
        if not(self.head):
            self.head=UNode(strs[0])
        self.lock.release()
        U=self._addItem(self.head,strs,0+1,n,hit)
        if(not U):
            if hit==0:
            	self.head.hit()
            elif hit>0:
            	self.head.addHits(hit)
            	
            if self._genOnadd:
                if not self.head.id:
            	    tmp=self.count_inc()
            	    self.head.setId(tmp)
            return self.head
        else:
        	return U
    def _showTree(self,tmp,i):
       
        if not(tmp):
            return
        
        for l in range(i):
            for j in range(4):
                print('-',end='')
            print('|', end='')

        if tmp.id:
           print(">'"+tmp.name+"'","#"+str(tmp.id),tmp._Hits)
        else:
            print(">'"+tmp.name+"'")
        
            
        
        if len(tmp.child)>0:
            for each in tmp.child:
                self._showTree(each,i+1)
        return

    def showTree(self):
        if not(self.head):
            print("Tree has no elements")
            return
        
        self._showTree(self.head,0)
    def _genId(self,tmp):
        for each in tmp.child:
            self._genId(each)

        
        if tmp._Hits>0:
            tmp2=self.count_inc()
            tmp.setId(tmp2)
    def genId(self):
        if self.counter>0:
            print("ID already generated")
            return
        if not(self.head):
            print("Head not initialized")
            return
        self._genId(self.head)
        
    def _writeTree(self,tmp,i,F):
        if not(tmp):
            return
        for l in range(i):
            for j in range(4):
                F.write('-')
            F.write('|')
            
        
        if tmp.id:
            F.write(">'"+tmp.name+"' #"+str(tmp.id)+" "+str(tmp._Hits))
        else:
            F.write(">'"+tmp.name+"'")
        F.write("\n")
            
        
        if len(tmp.child)>0:
            for each in tmp.child:
                self._writeTree(each,i+1,F)
        return

    def writeTree(self,OUT_FILE):
        if not(self.head):
            print("Tree has no elements")
            return
        F=open(OUT_FILE,'w',encoding="utf-8")
        if not(F):
            print("Error creating file")
            return
        self._writeTree(self.head,0,F)
        F.close()
    def _readTree(self,F,strs,i):
    	line=F.readline()
    	if not line:
    		return 1
    		
    	first=line.split(">")[0]
    	rest=line.split(">")[1]
    	sep=rest.split(" ")
    	
    	url=sep[0][1:]
    	while len(url)>0 and (url[len(url)-1]=="'" or url[len(url)-1]=="\n"):
    		url=url[:-1]

    	print(url)
    	count=0
    	for ch in first:
    		if ch=="|":
    			count+=1
    	
    	for hmm in strs:
    		s+=hmm+"/"
    	print("o",s+url)	
    	self.addItem(s+url)		
    	return 1

    def readTree(self,FILE):
        d=FILE
        urls=[]  
        f_str="https://"  ##"https://www.csie.ndhu.edu.tw"
        if not exists(d):
            print("File doesn exist",d)
            return

        F=open(d,"r",encoding="utf-8")
        if not F:
            print("Error opening",d)
            return
        line=F.readline()
        prev=""
        prev_c=0
        f1=False
        while True:
        	if not line:
        		break
        	first=line.split(">")[0]
        	rest=line.split(">")[1]
        	sep=rest.split(" ")
        	url=sep[0][1:]
        	while len(url)>0 and (url[len(url)-1]=="'" or url[len(url)-1]=="\n"):
        		url=url[:-1]
	
        	count=0
        	for ch in first:
        		if ch=="|":
        			count+=1
        	
        	if count>prev_c:
        		urls.append(prev)
        		
        	elif count==prev_c:
        		#self.addItem(s+url)
        		op=0
        	else:
        		dif=prev_c-count
        		for h in range(dif):
        			urls.pop(len(urls)-1)
        	if len(sep)>1:
        		Id=sep[1]
        		hits=int(sep[2])
        		s=f_str
        		for hmm in urls:
        			s+=hmm+"/"
        		#print("o",s+url,hits)
        		U=self.addItem(s+url,hits) 
        		U.id=int(Id[1:])
        	prev=url
        	prev_c=count
        	line=F.readline()
        F.close()
        return
          
    def getNodebyId(self,n,_curr=None,st=""):
        if not self.head:
            return NULL, ""
        if not _curr:
            _curr=self.head
        if len(st)==0:
            st="https://www.csie.ndhu.edu.tw"
        
            
        if _curr.id==n:
            return _curr, st
		
        for each in _curr.child:
            s,t=self.getNodebyId(n,each,st+"/"+each.name)
            if s:
                return s,t
            		
		
        return None, ""
			
    def mergeTree(self,Tree2):
        if  not Tree2.head:
            print("Tree2 is empty")
            return
        if Tree2.counter==0:
        	Tree2.genId()

        for id in range (1,Tree2.counter+1):
            tmp,st=Tree2.getNodebyId(id)
            #print(id)
            if tmp:
                self.addItem(st,tmp._Hits)
                				
        self.counter=0
        self.genId()
		
		
	
    def getDLevel(self,L,N,tmp=None,i=1):
        #generate the total collection of items at level N
        if not isinstance(L,list):
            print("Error- expected L as list")
            return
        if not self.head:
            return
        if not tmp:
            tmp=self.head

        if len(tmp.child)==0:
            return
        
        if i==N-1:
            for each in tmp.child:
                L.append([each.name,each._Hits])
            return
        for each in tmp.child:
            self.getDLevel(L,N,each,i+1)
        

        ## need to decide how i will generate category tree
        ## whether as we read in and add or after all read-in
        ## and then traverse the tree again
      
    def equalizer(self,tmp=None ):
        if not self.head:
            return 0
        if not tmp:
            tmp=self.head

        if len(tmp.child)==0:
            return tmp._Hits
        val=0
        for each in tmp.child:
            val+=self.equalizer(each)
        if tmp.id:
            tmp._Hits+=val
        else:
            tmp.id=-1
            tmp._Hits=val
        
        return tmp._Hits
    def writeNewList(self,OUT_FILE):
        if not(self.head):
            print("Tree has no elements")
            return
        if self.counter<=0:
            print("Tree id not generated")
            return
        F=open(OUT_FILE,'w',encoding="utf-8")
        if not(F):
            print("Error creating file")
            return
        F.close()
        

	
def test2():
	st="https://www.csie.ndhu.edu.tw/en/category/newlist-en/"
	st2="https://www.csie.ndhu.edu.tw/en/category/newlist-en/photo"
	st3="https://www.csie.ndhu.edu.tw/en/category/newlist-en/photo2"
	st4="https://www.csie.ndhu.edu.tw/zh/categ/reference/"

	st5="https://www.csie.ndhu.edu.tw/zh/"
	st6="https://www.csie.ndhu.edu.tw/zh/uni"
	stt="https://www.csie.ndhu.edu.tw/en/category/"
	st7="https://www.csie.ndhu.edu.tw"
	try:
		myTree=UTree(True)
		myTree2=UTree(False)
	except ValueError as e:
		print(e)
		quit()

	
	myTree.addItem(st)

	myTree.addItem(st2)
	myTree.addItem(st3)
	myTree.addItem(st4)
	myTree.addItem(st5)
	myTree.addItem(st5)
	myTree.addItem(st7)
	myTree.addItem(st7)
	myTree.addItem(st7)
	
	myTree2.addItem(st)
	myTree2.addItem(st2)
	myTree2.addItem(st3)
	myTree2.addItem(st4)
	myTree2.addItem(st5)
	myTree2.addItem(st5)
	myTree2.addItem(st7)
	myTree2.addItem(st7)
	myTree2.addItem(st7)
	myTree2.genId()
	myTree.showTree()
	myTree2.showTree()
	
def test1():
	st="https://www.csie.ndhu.edu.tw/en/category/newlist-en/"
	st2="https://www.csie.ndhu.edu.tw/en/category/newlist-en/photo"
	st3="https://www.csie.ndhu.edu.tw/en/category/newlist-en/photo2"
	st4="https://www.csie.ndhu.edu.tw/zh/categ/reference"
	st5="https://www.csie.ndhu.edu.tw/zh/"
	st6="https://www.csie.ndhu.edu.tw/zh/uni"
	stt="https://www.csie.ndhu.edu.tw/en/category/"
	st7="https://www.csie.ndhu.edu.tw"
	
	s2t="https://www.csie.ndhu.edu.tw/en/category/newlist-en/"
	s2t2="https://www.csie.ndhu.edu.tw/en/category/newlist-en/photo"
	s2t3="https://www.csie.ndhu.edu.tw/en/category/johndoe/photo2"
	s2t4="https://www.csie.ndhu.edu.tw/zh/categ/reference/"

	s2t5="https://www.csie.ndhu.edu.tw/zh/lk"
	s2t6="https://www.csie.ndhu.edu.tw/zh/uni"
	
	try:
		myTree=UTree(False)
		myTree2=UTree(False)
		myTree3=UTree(True)
	except ValueError as e:
		print(e)
		quit()

	print(st)
	print(myTree.find(st))
	print(myTree._str2list(st))
	#myTree.addItem(st5)
	myTree.addItem(st)

	myTree.addItem(st2)
	myTree.addItem(st2)
	myTree.addItem(st3)
	myTree.addItem(st4)
	t1=myTree.addItem(st5)
	t2=myTree.addItem(st5)
	myTree.addItem(st7)
	myTree.addItem(st7)
	t3=myTree.find(st5)
	print("Add Item return:",t1,t2,t3)
	myTree.addItem(st6)
	myTree.genId()
	
	myTree2.addItem(s2t)
	myTree2.addItem(s2t2)
	myTree2.addItem(s2t3)
	myTree2.addItem(s2t4)
	myTree2.addItem(s2t5)
	myTree2.addItem(s2t5)
	myTree2.addItem(s2t6)
	myTree2.addItem(s2t6)
	myTree2.addItem(s2t6)
	myTree2.addItem(st7)
	myTree2.addItem(st7)
	myTree2.genId()
	print(myTree2.counter)
	##print(myTree.head.child)
	l=myTree.head.child
	print("test:",l[0].name,l[1].name)
	print()
	#myTree.showTree()
	#myTree.genId()
	myTree.showTree()
	myTree2.showTree()
	myTree.mergeTree(myTree2)
	print("Merged")
	myTree.genId()
	myTree.showTree()
	myTree.writeTree("testtreewrite.txt")
	
	print("Readin:")
	myTree3.readTree("testtreewrite.txt")
	myTree3.genId()
	myTree3.showTree()
	
	
	print("unique items:",myTree.counter)
	print(myTree.find(st5).id)
	print(myTree.find(st5).name)
	myTree.showTree()
	myTree.equalizer()
	print("After Equalization")
	myTree.showTree()
	L1=[]
	N=3
	myTree.getDLevel(L1,N)
	L1.sort(key=itemgetter(1))
	print("Items at depth",N)
	for each in L1:
		print(each)
	##Chinese tags
	L=['futurestudent-zh_tw','research-zh_tw','newlist-zh_tw','aboutus-zh_tw','course-zh_tw','activity-zh_tw','alumni-zh_tw','resource-zh_tw']
	#n ,m =myTree.genCatTree(L)
	
if __name__=="__main__":
	print("URL_TREE TEST ENABLED")
	test2()
	test1()
