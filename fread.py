from os.path import isfile,exists
from operator import itemgetter
import url_tree as UT
import url_session as US
import datetime as dt
import copy
import numpy as np
from threading import Lock
import datetime
from extra_func import urlCorrector, writeSess, treeCheck,str2time,str2tz, getDiv, isValidURL, getEnv
from os import getpid
import psutil
import sys

class Fread:
	OFILE="mymeta.txt"
	LFILE="list.txt"
	IDIR="data/"
	ODIR="gen/"
	_osDIR="os.txt"			
	_bDIR="browser.txt"
	_botDIR="bot.txt"	
	
	_osList=[]		##os List (Static)
	_bList=[]		##browser List (Static)
	_botList=[]		##botList (STATIC)

	L=[]
	
	##_tfs=60 ##Default Time for sessions
	_tfs=2826.07/60
	def try_line_cout(self,t):
		try:
			for i in range(len(self._try_line_c)):
				if self._try_line_c[i][0]==t:
					self._try_line_c[i][1]+=1
					return
			self._try_line_c.append([t,1])
		except:
			self._try_line_c=[]
			self._try_line_c.append([t,1])

	def try_line_cout2(self,t):
		try:
			for i in range(len(self._try_line_c2)):
				if self._try_line_c2[i][0]==t:
					self._try_line_c2[i][1]+=1
					return
			self._try_line_c2.append([t,1])
		except:
			self._try_line_c2=[]
			self._try_line_c2.append([t,1])
	def try_line_cout3(self,t):
		try:
			for i in range(len(self._try_line_c3)):
				if self._try_line_c3[i][0]==t:
					self._try_line_c3[i][1]+=1
					return
			self._try_line_c3.append([t,1])
		except:
			self._try_line_c3=[]
			self._try_line_c3.append([t,1])

			
	def _initL():			##static function should be called before Fread object creation
		try:
			f=open(Fread.LFILE,'r')
		except:
			print("Error opening file",Fread.LFILE)
			return False
		lines=f.readlines()
		for line in lines:
			if line[len(line)-1]=='\n':
				l=line[:-1]
			else:
				l=line
			Fread.L.append(l)
		f.close()
		return True	
	def _initD(self):
		flag=False
		if not(exists(self.IDIR)):
			print("Error Directory path doesnt exist",self.IDIR)
			return False
		if not(exists(self.ODIR)):
			print("Error Directory path doesnt exist",self.ODIR)
			return False
			
		for i in range(self._start,self._end):
			
			if i>=len(self.L):
				flag=True
				print("index outside of L range")
				break
			elif i<0:
				flag=True
				print("not properly initialized")
				break
			l=self.L[i]
			if not(isfile(self.IDIR+l)):
				print(l,"file missing.")
				flag= True
		if flag:
			return False
		else:
			return True
	def _initT(self):
		try:
			for i in range(len(self.T)):
				self.T[i]=UT.UTree(self._cond)
		except ValueError as e:
			raise e
	def _initOther(self):
		try:
			f=open(Fread._botDIR,'r')
		except:
			print("Error opening file",Fread._botDIR)
			return False
		lines=f.readlines()
		for line in lines:
			if line[len(line)-1]=='\n':
				line=line[:-1]

			Fread._botList.append(line)
		f.close()
		############
		try:
			f=open(Fread._osDIR,'r')
		except:
			print("Error opening file",Fread._osDIR)
			return False
		lines=f.readlines()
		for line in lines:
			if line[len(line)-1]=='\n':
				line=line[:-1]
			line=line.split(" ")
			if len(line)!=2:
				f.close()
				print(Fread._osDIR,"Browser param file expected 2 items")
				return False
			Fread._osList.append([line[0],line[1]])
		f.close()
		################
		try:
			f=open(Fread._bDIR,'r')
		except:
			print("Error opening file",Fread._bDIR)
			return False
		lines=f.readlines()
		for line in lines:
			if line[len(line)-1]=='\n':
				line=line[:-1]
			line=line.split(" ")
			if len(line)!=2:
				f.close()
				print(Fread._bDIR,"Browser param file expected 2 items")
				return False
			Fread._bList.append([line[0],line[1]])
		f.close()

		if len(Fread._osList)==0:
			print("_osList is empty")
			return False
		if len(Fread._bList)==0:
			print("_bList is empty")
			return False

		return True		
	def __init__(self,s,e,pid,cond):
		self._start_time=datetime.datetime.now()
		self._end_time=None
		self._start=s
		self._end=e
		self.total_line_read=0
		self.total_english_read=0
		self.total_chinese_read=0
		self.total_both_read=0
		self.total_other_read=0
		self._http_status_skip=0
		self._get_skip=0
		self._badline_skip=0
		self._bot_skip=0
		self._notvalidurl_skip=0
		self._bbutnot_e_c=0

		self.max_curr=[0,0,0,0]
		
		self.Mlock=[Lock(),Lock(),Lock(),Lock()]
		self.lock_t=Lock()
		self.lock_e=Lock()
		self.lock_c=Lock()
		self.lock_o=Lock()
		self.lock_b=Lock()
		
		self.p_ref=pid
		self._cond=cond				##False - Tree not generated  ##True - Tree generated
		
		self.M= [[],[],[],[]]		##meta data ##closed sessions for English only
		
		
		#self.M_C=[]		##meta data ##closed sessions for Chinese only
		#self.M_B=[]		##meta data ##closed sessions for both Chinese and English
		#self.M_O=[]		##meta data ##closed sessions for disregarded items
		self.T=[None,None]   ##meta tree structure for English only
		#self.T_C=None     ##meta tree structure for Chinese only
		#self.T_B=None     ##meta tree id structure for both English and Chinese
		#self.T_O=None     ##meta tree id structure for disregarded items
		
		if len(self.L)==0:
			raise ValueError("static List L not intialized")
		
		if not(self._initD()):
			raise ValueError("Error File checking")

		if not(self._initOther()):
			raise ValueError("Other initializer Error")

		try:
			self._initT()
		except ValueError as e:
			raise e
	def summary(self):			## ONly call this function at the end before deconstructing
		print("Fread:",self.p_ref,"From:",self._start,"to",self._end)
		print("Start:",self._start_time)
		self._end_time=datetime.datetime.now()
		print("end:",self._end_time)
		print("Time Diff:",str(self._end_time-self._start_time))
		print("Mem:",psutil.Process(getpid()).memory_info().rss / 1024 ** 2,"MB")
	def __del__(self):
		#self.summary()
		for i in range(len(self.M)):
			for m1 in self.M[i]:
				self.M[i].remove(m1)
				del m1
				
			
	def getDiv(self,url,div):
		return getDiv(url,div)
	def inc_tlr(self):
		#self.lock_t.acquire()
		self.total_line_read+=1
		#self.lock_t.release()
	def inc_ter(self):
		#self.lock_e.acquire()
		self.total_english_read+=1
		#self.lock_e.release()
	def inc_tcr(self):
		#self.lock_c.acquire()
		self.total_chinese_read+=1
		#self.lock_c.release()
	def inc_tor(self):
		#self.lock_o.acquire()
		self.total_other_read+=1
		#self.lock_o.release()
	def inc_tbr(self):
		#self.lock_b.acquire()
		self.total_both_read+=1
		#self.lock_b.release()
		
	def manip1(self,time,current,U,x,url,ip,b,o):
		flag=False
		y=0
		while y<len(current):	
			if current[y].ip==ip:
				if (time-current[y]._etime).total_seconds()<dt.timedelta(minutes=self._tfs).total_seconds():
					flag=True
					if self._cond:
						tmp=U.id
						current[y].addS(US.SNode([tmp,time,b,o]),time)
					else:
						tmp2=url
						current[y].addS(US.SNode([tmp2,time,b,o]),time)
				
				else:
					
					self.Mlock[x].acquire()
					self.M[x].append(current[y])
					self.Mlock[x].release()
					current.remove(current[y])
					y-=1
				
			else:
				if (time-current[y]._etime).total_seconds()>=dt.timedelta(minutes=self._tfs).total_seconds():
					self.Mlock[x].acquire()
					self.M[x].append(current[y])
					self.Mlock[x].release()
					current.remove(current[y])
					y-=1
			if self.max_curr[x]<len(current):
				self.max_curr[x]=len(current)
			#print(x,y,"  ",len(current),len(current[y].S))			
			y+=1
		#print(x,len(current))			
		return flag
	
								
	def genMeta(self,s=0,e=0):
		
		if s==0:
			s=self._start
		else:
			self._start=s
		if e==0 or e>self._end:
			e=self._end
		else:
			self._end=e
		current=[[],[],[],[]] ##current Sessions ## Sessions stil open
		
		U=[None,None,None,None]
		print("ID"+str(self.p_ref),"Gen from:",s,"to",e)
		for i in range(s,e):
			f=open(Fread.IDIR+Fread.L[i],"r")
			olr=-1						## Overall Line REads
			while True:
				line=f.readline()
				if not line:
					break
				olr+=1
				for oo in range(len(U)):
					U[oo]=None
					
				line=line.split(' ')
				if len(line)>=8:
					
					
					self.inc_tlr()
					ip=line[0]
					time=line[3][1:]
					
					tz=line[4][:-1]
					time=str2time(time,tz)
					#print(time)
					time-=str2tz(tz)
					if (line[5][1:].upper()!="GET"):
						self._get_skip+=1
						continue

					if (line[8]!="200" and line[8]!="201" and line[8]!="202" and line[8]!="203" and line[8]!="204" and line[8]!="205" and line[8]!="206"):
						self._http_status_skip+=1
						continue
					
					_browser,_os=getEnv(line,Fread._bList,Fread._osList,Fread._botList)
					#if _os:
						#if "compatible" in _os:
							#print(line)
					if "Bot" in _browser or "Bot" in _os:
						self._bot_skip+=1
						continue

					#print(line)								##TestING
					#input()									##TESTING
					
					try:
						self.try_line_cout3(_browser)				##TESTING
						self.try_line_cout2(_os)					##TESTING
						##self.try_line_cout3(line[13])				##TESTING
					except:
						pass
					
					

					url=line[6]
					url=urlCorrector(url)

					if not(isValidURL(url)):
						self._notvalidurl_skip+=1
						continue

					#print("ll:",url)
					flag=False
					if self.getDiv(url,'B'):
						f2=False
						self.inc_tbr()
						if self._cond:
							U[2]=self.T[0].addItem(url)
						if not self.manip1(time,current[2],U[2],2,url,ip,_browser,_os):
							if not(self._cond):
								_s=US.SSession(ip)	
								_s.addS(US.SNode([url,time,_browser,_os]),time)
								current[2].append(_s)
							else:
								tmp=U[2].id
								_u=US.SSession(ip)
								_u.addS(US.SNode([tmp,time,_browser,_os]),time)
								current[2].append(_u)

						if self.getDiv(url,'E'):
							self.inc_ter()
							f2=True
							if self._cond:
								U[0]=self.T[0].find(url)
							if not self.manip1(time,current[0],U[0],0,url,ip,_browser,_os):
								if not(self._cond):
									_s=US.SSession(ip)	
									_s.addS(US.SNode([url,time,_browser,_os]),time)
									current[0].append(_s)
								else:
									tmp=U[0].id
									_s=US.SSession(ip)
									_s.addS(US.SNode([tmp,time,_browser,_os]),time)
									current[0].append(_s)
								
						if self.getDiv(url,'C'):
							self.inc_tcr()
							f2=True
							if self._cond:
								U[1]=self.T[0].find(url)
							if not self.manip1(time,current[1],U[1],1,url,ip,_browser,_os):
								if not(self._cond):
									_s=US.SSession(ip)	
									_s.addS(US.SNode([url,time,_browser,_os]),time)
									current[1].append(_s)
								else:
									tmp=U[1].id
									_s=US.SSession(ip)
									_s.addS(US.SNode([tmp,time,_browser,_os]),time)
									current[1].append(_s)
						if not f2:
							self._bbutnot_e_c+=1
					else:
						self.inc_tor()
						if self._cond:
							U[3]=self.T[1].addItem(url)
						if not self.manip1(time,current[3],U[3],3,url,ip,_browser,_os):
							if not(self._cond):
								_s=US.SSession(ip)	
								_s.addS(US.SNode([url,time,_browser,_os]),time)
								current[3].append(_s)
							else:
								tmp=U[3].id
								_s=US.SSession(ip)
								_s.addS(US.SNode([tmp,time,_browser,_os]),time)
								current[3].append(_s)
							
					#print("kk:",len(current[0]),len(current[1]),len(current[2]),len(current[3]))
				else:
					self._badline_skip+=1
						
			f.close()
		for m in range (len(self.M)):		
			for each in current[m]:
				self.M[m].append(each)
			
		print("ID"+str(self.p_ref),"Gen Complete from:",s,"to",e)

		return
	def writeSessions(self): ##write sesssions Session DATA for SSession Class
		PATH=Fread.ODIR
		for x in range(len(self.M)):
			fn=PATH+str(self.p_ref)+"_"+str(x)+".txt"
			fn2=PATH+str(self.p_ref)+"_"+str(x)+"_ENV.txt"
			writeSess(fn,fn2,self.M[x],self._cond)
		print("ID"+str(self.p_ref),"Session Write Complete from:",self._start,"to",self._end)
	def genTreefromM(self):
		print("ID"+str(self.p_ref),"GenTreefromM from:",self._start,"to",self._end)
		self.T[0]._genOnadd=True
		self.T[1]._genOnadd=True
		for i in range(len(self.M)-1,-1,-1):
			tt=0
			count=0
			#print(i)
			for j in range(len(self.M[i])):
				for k in range(len(self.M[i][j].S)):
					url=self.M[i][j].S[k].url
					#print("eg:","'"+url+"'")
					if self.getDiv(url,'B'):
						if i==2:
							N=self.T[0].addItem(url)
						else:
							N=self.T[0].find(url)
					else:
						N=self.T[1].addItem(url)
					self.M[i][j].S[k].n=N.id
					#self.M[i][j].S[k].url=None
					
					count+=1
					
			#print("Total SNodes;",count)
	
		self._cond=True
		print("ID"+str(self.p_ref),"GenTreefromM Complete from:",self._start,"to",self._end)
		return
	def writeTrees(self):
		if not self._cond:		
			print("ID"+str(self.p_ref),"writeTees(): No tree.")
			return
			
		PATH=self.ODIR
		fn=PATH+str(self.p_ref)+"_"
		self.T[0].writeTree(fn+"IN_Tree.txt")
		self.T[1].writeTree(fn+"OUT_Tree.txt")
		
		print("ID"+str(self.p_ref),"Tree Write Complete from:",self._start,"to",self._end)
		return
		
	def showSess(self,x=0,to=-1):
		m=self.M[x]
		for i,m1 in enumerate(m):
			if to>0:
				if i>to:
					break
			print(m1.ip)
			for j, en in enumerate(m1.S):
				if en.n:
					if j>0:
						if not en.url:
							print(end=' ')
					print(en.n,end="")
				if en.url:
					if j>0:
						if not en.n:
							print(end='\n')
					print("  ",j,en.url)
			if not en.url:
				print()
			print("start:",m1._stime,"end:",m1._etime)
			print("delta:",(m1._etime-m1._stime).total_seconds(),'\n')
	
		
def test1():
##TESTING
	st="https://www.csie.ndhu.edu.tw/en/category/newlist-en/"
	st2="https://www.csie.ndhu.edu.tw/category/newlist-en/photo"
	st3="https://www.csie.ndhu.edu.tw/newlist-zh_tw/1.pdf"
	st4="https://www.csie.ndhu.edu.tw/zh/categ/reference/"
	print(F.getDiv(st,'z'),F.getDiv(st,'E'),F.getDiv(st,'C'),F.getDiv(st,'B'))
	print(F.getDiv(st2,'E'),F.getDiv(st2,'C'),F.getDiv(st2,'B'))
	print(F.getDiv(st3,'E'),F.getDiv(st3,'C'),F.getDiv(st3,'B'))
	print(F.getDiv(st4,'E'),F.getDiv(st4,'C'),F.getDiv(st4,'B'))


if __name__=="__main__":
	TEST=False
	ch_bool=True
	ID=10
	if len(sys.argv)>1:
		if sys.argv[1].upper()=="-T":
			TEST=True
	if not(Fread._initL()):
		print("Error creating L list")
		quit()
	total=len(Fread.L)
	print("Select:\n1. For tree FIRST mode\n2. For tree LAST mode\nChoice:      ",end=" ")
	try:
		choice=int(input())
		if choice==2:
			ch_bool=False
	except:
		print("Error choice input: default tree first mode enable")
	if not TEST:
		try:
			ch_id=int(input("Enter ID num: "))
			ID=ch_id
		except:
			pass
		try:
			_tfs=int(input("Enter _tfs: "))
			if _tfs != -1:
				Fread._tfs=_tfs
		except:
			pass
		
	print()
	try:
		F=Fread(0,total,ID,ch_bool)
	
	except ValueError as e:
		print (e)
		quit()
	
	print("_tfs:",F._tfs)
	print("Total files:",total)
	
	if (not F._cond):
		print("MODE:: Tree LAST Mode")

	else:
		print("MODE:: Tree FIRST Mode")
	
	if TEST:
		print("##Test-Mode::ENABLED##")
		print()	
		F.genMeta(0,2)
	else:
		print()	
		F.genMeta()
	
	
	"""
	#TESTING
	print ("comp:",len(F.M[0]),len(F2.M[0]))
	print ("compS:",len(F.M[0][0].S),len(F2.M[0][0].S))
	for yx in range(len(F.M)):
		for yy in range(len(F.M[yx])):
			if len(F.M[yx][yy].S)!=len(F2.M[yx][yy].S):
				print("UNMATCH SNODES")
				break
	"""
	##TRY LINE C
	
	"""
	ss=F._try_line_c
	ss2=F._try_line_c2
	print("Browser",len(ss))
	print(type(ss))
	ss.sort(reverse=True, key=itemgetter(1))
	ss2.sort(reverse=True, key=itemgetter(1))
	

	for i in range(20):
		try:
			print(ss[i][0],ss[i][1])
		except:
			break
	print()
	if (not F._cond):
		F.genTreefromM()
	print()
	
	print("OS", len(ss2))
	for i in range(20):
		try:
			print(ss2[i][0],ss[i][1])
		except:
			break
	print()
	"""

	"""
	print("Version")
	for item in F._try_line_c3:
		print(item[0],item[1])
	print()
	"""
	
	if (not F._cond):
		F.genTreefromM()
	F.summary()
	print()
	F.writeSessions()
	F.writeTrees()
	#F.showSess(0,5)
	
	"""
	#mode 1 vs mode 2 Testing
	F2.writeSessions()
	F2.writeTrees()
	#
	#print("next2")
	#F2.showSess(0,5)
	#
	#F2.summary()
	print("Tree Comparision Check =",treeCheck(F.T[0],F2.T[0]))
	#F.T[0].showTree()
	#F2.T[0].showTree()
	"""
	
	print("\nUnique items in tree:",F.T[0].counter)
	print("Unique items in Other tree:",F.T[1].counter)
	
	print("Sess English:",len(F.M[0]))
	print("Sess Chinese:",len(F.M[1]))
	print("Sess Both:",len(F.M[2]))
	print("Sess Other:",len(F.M[3]))
	#print("60 min:",dt.timedelta(minutes=60).total_seconds())
	print()
	print("Total Lines:",F.total_line_read)
	print("Total bad line Skipped:",F._badline_skip)
	print("Total Non-valid URL:",F._notvalidurl_skip)
	print("Total get line Filtering:",F._get_skip)
	print("Total http status Filtering:",F._http_status_skip)
	print("Total Bot filter:",F._bot_skip)
	print()
	print("Total English read:",F.total_english_read)
	print("Total Chinese read:",F.total_chinese_read)
	print("Total Both read:",F.total_both_read)
	print("Both but not English or Chinese",F._bbutnot_e_c)
	print("Total OTher read:",F.total_other_read)
	print()
	print("Max current English session",F.max_curr[0])
	print("Max current Chinese session",F.max_curr[1])
	print("Max current BOth session",F.max_curr[2])
	print("Max current Other session",F.max_curr[3])

	
