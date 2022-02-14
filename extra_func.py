import url_session as US
import datetime as dt
from numpy import array
from copy import deepcopy
from delim import SPLIT_PARAM as SPLIT_PARAM
from delim import SPLIT_PARAM2 as SPLIT_PARAM2


def writeSess(ST,ST2,M,_cond): ##write sesssions Session DATA for SSession Class
	f=open(ST,"w")
	f2=open(ST2,"w")
	if not f:
		print("error creating file to write",f)
		return
	if not f2:
		print("error creating file to write",f2)
		return
	for each in M:
		f.write(each.ip)
		f.write(SPLIT_PARAM)
		f.write(each._stime.strftime("%Y/%m/%d %H:%M:%S"))
		f.write(SPLIT_PARAM)
		f.write(each._etime.strftime("%Y/%m/%d %H:%M:%S"))
		f.write(SPLIT_PARAM)
		
		for i, ea in enumerate(each.S):
		    if i>0:
		        f.write(SPLIT_PARAM2)
		        f2.write(SPLIT_PARAM)
		    if _cond:
		    	f.write(str(ea.n))
		    else:
		    	f.write(ea.url)
				
		    
		    f2.write(str(ea.browser))
		    f2.write(SPLIT_PARAM2)
		    f2.write(str(ea.os))
		f.write("\n")
		f2.write("\n")
	f.close()
	f2.close()
	
def readSess(ST,M,_cond): ##write sesssions Session DATA for SSession Class
	f=open(ST,"r")
	if not f:
		print("error opening file to read",ST)
		return
	line=f.readline()
	while line:
		if line[len(line)-1]=="\n":
			line=line[:-1]
		sep=line.split(SPLIT_PARAM)
		if len(sep)!=4:
			print("split "+SPLIT_PARAM+" parts not as expected",sep)
			continue
		ip=sep[0]
		
		_st=dt.datetime.strptime(sep[1],'%Y/%m/%d %H:%M:%S')
		_et=dt.datetime.strptime(sep[2],'%Y/%m/%d %H:%M:%S')
		temp=US.SSession(ip)
		
		for i,ea in enumerate(sep[3].split(SPLIT_PARAM2)):
			if _cond:
				ea=int(ea)
			if i ==0:
				temp.addS(US.SNode(ea),_st)
			else:
				temp.addS(US.SNode(ea),_et)
		M.append(temp)
		line=f.readline()
	f.close()
def str2time(st,tz):
	temp=st.split(':')
	if len(temp)<4:
		print(st,"invalid date time1")
		return None
	t=temp[1:]
	d=temp[0]
	d=d.split('/')
	if len(d)<3:
		print(st,"invalid date time2")
		return None
		
	if d[1]=="Dec":
		d[1]=12
	elif d[1]=="Nov":
		d[1]=11
	elif d[1]=="Oct":
		d[1]=10
	elif d[1]=="Sep":
		d[1]=9
	elif d[1]=="Aug":
		d[1]=8
	elif d[1]=="Jul":
		d[1]=7
	elif d[1]=="Jun":
		d[1]=6
	elif d[1]=="May":
		d[1]=5
	elif d[1]=="Apr":
		d[1]=4
	elif d[1]=="Mar":
		d[1]=3
	elif d[1]=="Feb":
		d[1]=2
	elif d[1]=="Jan":
		d[1]=1
	f=None

	try:
		f=dt.datetime(int(d[2]),int(d[1]),int(d[0]),int(t[0]),int(t[1]),int(t[2]))
	except ValueError as e:
		print(st,e)
		return None
	
	return f
	
def str2tz(st):
	if not st:
		print("timezone invalsetid")
		return dt.timedelta(hours=0)
	if len(st)!=5:
		print("timezone size invalid")
		return dt.timedelta(hours=0)
	if st[0]=="+":
		sign=True
	elif st[0]=="-":
		sign=False
	else:
		print("timezone sign invlaid")
		return dt.timedelta(hours=0)
			
	h=int(st[1:3])
	#print("h:",h)
	if st[3:5] != "00":
		print("timezone strange minutes param",st[3:5])
		
	if sign:
		return dt.timedelta(hours=h)
	else:
		return -dt.timedelta(hours=h)

def getDiv(url,div):
	if not isinstance(url, str) or not isinstance(div, str):
		print("invalid param")
		return False
	L=['en']
	L2=['']
	C=['zh_tw','zh']
	C2=['-zh_tw']
	div=div.upper()
	
	
	urls=url.split("/")
	flag1=False
	flag2=False
	#print(urls,div)
	for each in urls:
		if div=="E":
			if "https://www.csie.ndhu.edu.tw/en" == url or "www.csie.ndhu.edu.tw/en" == url:
				return True
			if "https://www.csie.ndhu.edu.tw/en/" == url or "www.csie.ndhu.edu.tw/en/" == url:
				return True
			for ea in L:
				if ea == each:
					return True
			#for ea in L2:
				#if ea in each:
					#return True
		if div=="C":
			if "https://www.csie.ndhu.edu.tw" == url or "www.csie.ndhu.edu.tw" == url:
				return True
			if "https://www.csie.ndhu.edu.tw/" == url or "www.csie.ndhu.edu.tw/" == url:
				return True
			for ea in C:
				if ea == each:
					return True
			for ea in C2:
				if ea in each:
					return True
		elif div=="B":
			flag1=getDiv(url,'E')
			flag2=getDiv(url,'C')
			if flag1 or flag2:
				return True
		
	return False
def isValidURL(st):
		if not isinstance(st,str):
			print("IsValid Url Expected str")
			return False
		
		if st[(-len(".css")):]==".css":
			return False
		if st[(-len(".js")):]==".js":
			return False
		if st[(-len(".xml")):]==".xml":
			return False

		return True
def urlCorrector(url):
	url=url.split('?')[0]
	url_r=url.replace("//","/")
	while url!=url_r:
		url=url_r
		url_r=url.replace("//","/")
		
	if len(url)==0:
		url="https://www.csie.ndhu.edu.tw/"
		#print(line)	
	if not("https://www.csie.ndhu.edu.tw" in url):
		if url[0]=="/":
			url="https://www.csie.ndhu.edu.tw"+url
		else:
			url="https://www.csie.ndhu.edu.tw/"+url


	while len(url)>0 and (url[len(url)-1]=="/" or url[len(url)-1]=="*"):
		url=url[:-1]

	url_s=url.split("/")
	while len(url)>0 and (url_s[-1]=="embed" or url_s[-1]=="print" or url_s[-1]=="feed"):
		url_s=url_s[:-1]
	while len(url_s)>1 and url_s[len(url_s)-2]=="page":
		url_s=url_s[:-2]
	
	n_url=""
	for i,item in enumerate(url_s):
		if i!=0:
			n_url+="/"
		n_url+=item
	return n_url
def _treeCheck(id,T1,T2,st=None,i=0,):		## Checks if all element in T1 is in T2 ## only one way check
	if i==0:
		T1=T1.head
		st="https://www.csie.ndhu.edu.tw"
		
	if not T1:
		return True
	TT=T2.find(st)
	if not TT:
		return False
		
	if T1.name != TT.name:
		print(id,i,"Name missmatch",T1.name,",",TT.name,st)
		return False
	if len(T1.child) != len(TT.child):
		print(id,i,"Sub child missmatch",len(T1.child),",",len(TT.child),st)
		return False
	if T1._Hits != TT._Hits:
		print(id,i,"num of hits mismath",T1._Hits,",",TT._Hits,st)
		return False
		
	for each in T1.child:
		if(not _treeCheck(id,each,T2,st+"/"+each.name,i+1)):
			return False
	return True
	
def treeCheck(T1,T2,st=None,i=0):
	if _treeCheck(0,T1,T2):
	 	if _treeCheck(1,T2,T1):     ## Do one way check the 2 way to ensure exactly identical
	 		return True
	return False

def sesToarr(M):
	L=[]
	for m in M:
		temp=[]
		for sn in m.S:
			temp.append(int(sn.n))
		L.append(array(temp,dtype=int))
	return array(L,dtype=object)


def getCATid(CAT, url):
    url=url.lower()
    L=[-1 for i in range(len(CAT))]
    min_p=None
    min_i=None
    for i, C2 in enumerate(CAT):
        n=0
        for item in C2:
            p=url.find(item)
            if p>0:
                if not min_p:
                    min_p=p
                    min_i=i
                elif p<min_p:
                    min_p=p
                    min_i=i
    
    if not min_p:
        if url[:8]=="https://":
            url=url[8:]
        if url=="www.csie.ndhu.edu.tw/" or url=="www.csie.ndhu.edu.tw":
            return len(CAT)
        if url=="www.csie.ndhu.edu.tw/en" or url=="www.csie.ndhu.edu.tw/en/":
            return len(CAT)
        return len(CAT)+1
    if min_p<0:
        return len(CAT)+1
    else:
        return min_i

def getEnv(line,bList,osList,botList,lonly=False):
	_E=[None,None,None,None,None]
	_n=len(_E)
	b=None
	os=None
	for i in range(_n):
		try:
			_E[i]=line[11+i].lower()
		except:
			if i==0:
				return "NA","NA"
			else:
				pass


	for item in botList:
		for i in range(_n):
			if _E[i]:
				if item.lower() in _E[i]:
					return "Bot","Bot"
	

	for item in bList:
		if item[0].lower() in _E[0]:
			b=item[1]
			break

	if not os:
		for item in osList:
		
			for i in range(_n-1,0,-1):	
				if _E[i]:
					if item[0].lower() in _E[i]:
						os=item[1]
						break
	if not lonly:		##List only param to return only values if founf in list(s)
		if not os:
			if _E[1]:
				os=_E[1]
				if os[len(os)-1]=="\n":
					os=os[:-1]
			else:
				os="NA"
		if not b:
			if _E[0]:
				b=_E[0]
				if b[len(b)-1]=="\n":
					b=b[:-1]
			else:
				b="NA"
	else:
		if not os:
			os="Other"
		if not b:
			b="Other"

	return b,os
def getBrowser(line,bList):
	_first=None
	
	ret=None
	try:
		_first=line[12]
	except:
		return "NA"
	try:
		_second=line[13]
	except:
		pass

	for item in bList:
		if item in _first:
			ret=item
			break
	if ret==None:
		ret="Other"
	if (_second):
		ret+=" "
		ret+=_second
	
	return ret

def getURLrefFromTree(_U2N,_N2U,tmp=None,strs=[]):
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
    if tmp.id:
    	if tmp.id>0:
    		it=_U2N.get(s)
    		it2=_N2U.get(tmp.id)
    		if tmp.id>=1:
    			if not it:
    				_U2N[s]=[tmp.id,tmp._Hits]
    			if not it2:
    				_N2U[tmp.id]=s


    for each in tmp.child:
        getURLrefFromTree(_U2N,_N2U,each,strs)

def getURLrefFromLU(_U2N,_N2U,F):
	f=open(F,"r")
	if not f:
		print("Error: File not found",F)
		return
	lines=f.readlines()
	for line in lines:
		line=line.split(" : ")
		while len(line[2])>0 and (line[2][len(line[2])-1]=="\n" or line[2][len(line[2])-1]==" "):
			line[2]=line[2][:-1]

		_U2N[line[2]]=[int(line[0]),int(line[1])]
		_N2U[int(line[0])]=line[2]
	return

def readFI(tag,L):
	if not isinstance(L,list):
		print("Error L expected list")
		return
	f=open(tag,'r')
	if not f:
		print("Error opening file",tag)
		return

	lines = f.readlines()
	for line in lines:
		if line[len(line)-1]=="\n":
			line=line[:-1]
		if line[len(line)-1]==" ":
			line=line[:-1]
		
		line_s=line.split(" ")
		
		for li in line_s:
			li=li[1:-1]
			l=li.split(",")
			L.append(l)

	f.close()
	return

def Alt_trans(data):
	import numpy as np

	for a,each in enumerate(data):
		i=0
		while i < len(each)-1:
			if each[i]==each[i+1]:
				data[a]=np.delete(each,i)
				i-=1
			i+=1
	return
