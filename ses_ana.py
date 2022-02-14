import url_session as US
from copy import deepcopy
from os.path import isfile,exists
from extra_func import str2time,str2tz, getDiv,isValidURL, urlCorrector, getEnv
import sys 
from os import getpid
import psutil
import datetime 
from multiprocessing import Process

class SA:
	TDIR="tgen/"
	LFILE="list.txt"
	IDIR="data/"
	ODIR="tgen/"
	L=[]
	_osDIR="os.txt"			
	_bDIR="browser.txt"
	_botDIR="bot.txt"	
	
	_osList=[]		##os List (Static)
	_bList=[]		##browser List (Static)
	_botList=[]		##botList (STATIC)

	def _initL():			##static function should be called before Fread object creation
		try:
			f=open(SA.LFILE,'r')
		except:
			print("Error opening file",SA.LFILE)
			return False
		lines=f.readlines()
		for line in lines:
			if line[len(line)-1]=='\n':
				l=line[:-1]
			else:
				l=line
			SA.L.append(l)
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
	def __init__(self,s,e):
		self._start=s
		self._end=e
		self.lines=[]
		self.total_english_read=0
		self.total_chinese_read=0
		self.total_both_read=0
		self.total_other_read=0
		if len(self.L)==0:
			raise ValueError("static List L not intialized")
		
		if not(self._initD()):
			raise ValueError("Error File checking")
		if not self._initOther():
			raise ValueError("init Other failed")

	def readBlock(self):
		_start_time=datetime.datetime.now()
		for i in range(self._start,self._end):
			f=open(SA.IDIR+SA.L[i],"r")
			temp_lines=f.readlines()	
			f.close()
			for line in temp_lines:
				line=line.split(" ")
				if len(line)>=8:
					self.lines.append(line)
		
		_end_time=datetime.datetime.now()
		print()
		print("REadBLock complete")
		print("Start:",_start_time)
		print("end:",_end_time)
		print("Time Diff:",str(_end_time-_start_time))
		print("Mem:",psutil.Process(getpid()).memory_info().rss / 1024 ** 2,"MB")
	def manip2(self,time,x,url,ip):
		flag=False
		y=0
		while y<len(self.current):	
			if self.current[y].ip==ip:
				flag=True
				
				tmp2=url
				self.current[y].addS(US.SNode(tmp2,time),time)
			y+=1
		#print(x,len(current))			
		return flag
	def _initOther(self):
		try:
			f=open(SA._botDIR,'r')
		except:
			print("Error opening file",SA._botDIR)
			return False
		lines=f.readlines()
		for line in lines:
			if line[len(line)-1]=='\n':
				line=line[:-1]

			SA._botList.append(line)
		f.close()
		############
		try:
			f=open(SA._osDIR,'r')
		except:
			print("Error opening file",SA._osDIR)
			return False
		lines=f.readlines()
		for line in lines:
			if line[len(line)-1]=='\n':
				line=line[:-1]
			line=line.split(" ")
			if len(line)!=2:
				f.close()
				print(SA._osDIR,"Browser param file expected 2 items")
				return False
			SA._osList.append([line[0],line[1]])
		f.close()
		########
		try:
			f=open(SA._bDIR,'r')
		except:
			print("Error opening file",SA._bDIR)
			return False
		lines=f.readlines()
		for line in lines:
			if line[len(line)-1]=='\n':
				line=line[:-1]
			line=line.split(" ")
			if len(line)!=2:
				f.close()
				print(SA._bDIR,"Browser param file expected 2 items")
				return False
			SA._bList.append([line[0],line[1]])
		f.close()
		##########
		if len(SA._osList)==0:
			print("_osList is empty")
			return False
		if len(SA._bList)==0:
			print("_bList is empty")
			return False
		return True
	def job(self, div,id):
		if div!="E" and div!="C" and div!="B":
			print(id,"JOB Div=",div,"Invalid")
			return
		print("Job Gen"+str(id),"  '"+div+"' Start")
		_start_time=datetime.datetime.now()
		self.current=[]
		for line in self.lines:
			if len(line)<8:
				continue

			ip=line[0]
			time=line[3][1:]
			
			tz=line[4][:-1]
			time=str2time(time,tz)
			#print(time)
			time-=str2tz(tz)
			
			if (line[5][1:].upper()!="GET"):
				continue
			
			if (line[8]!="200" and line[8]!="201" and line[8]!="202" and line[8]!="203" and line[8]!="204" and line[8]!="205" and line[8]!="206"):
				continue
			_browser,_os=getEnv(line,SA._bList,SA._osList,SA._botList)
			if "Bot" in _browser or "Bot" in _os:
				continue

			url=line[6]
			url=urlCorrector(url)

			if not(isValidURL(url)):
				continue

			if getDiv(url,div):
				self.total_english_read+=1
				if not self.manip2(time,id,url,ip):
					_s=US.SSession(ip)	
					_s.addS(US.SNode(url,time),time)
					self.current.append(_s)
		_end_time=datetime.datetime.now()
		print()
		print("Gen"+str(id)+"  '"+div+"' complete")
		print("Start:",_start_time)
		print("end:",_end_time)
		print("Time Diff:",str(_end_time-_start_time))
		print("Mem:",psutil.Process(getpid()).memory_info().rss / 1024 ** 2,"MB")
		self.wirteTimeDelta(id)
		
	def gentimeDelta(self,s=0,e=0):
		_start_time=datetime.datetime.now()
		if s==0:
			s=self._start
		else:
			self._start=s
		if e==0 or e>self._end:
			e=self._end
		else:
			self._end=e
		print("Gen from",s,"to",e)
		self.readBlock()		##Read block before FORK below....so read block is duplicated across each sub child
		print()
		_p=[None,None,None]
		_div=["E","C","B"]
		for j in range(3):
			_p[j]=Process(target=self.job, args=(_div[j],j,))
			_p[j].start()
		for j in range(3):
			_p[j].join()
		_end_time=datetime.datetime.now()
		print()
		print("Overall process complete")
		print("Start:",_start_time)
		print("end:",_end_time)
		print("Time Diff:",str(_end_time-_start_time))
		return	
	def wirteTimeDelta(self,id):
		print()
		print("Job Writing File"+str(id),"Start")
		_start_time=datetime.datetime.now()
		
		t_min=None
		t_max=None
		
		m =self.current
		F=open(SA.TDIR+"tdelta"+str(id)+".txt","w")
		for S in m:
			temp=None
			i =0
			for n in S.S:
				if temp:
					if i!=0:
						F.write(",")
					t=(n.time-temp).total_seconds()
					if not t_min:
						t_min=t
					elif t_min>t:
						t_min=t
					if not t_max:
						t_max=t
					elif t_max<t:
						t_max=t
						
					F.write(str(t))
					i+=1
				temp=n.time
			if i>0:
				F.write("\n")
		F.close()
		_end_time=datetime.datetime.now()
		print("Job",id,"T-Delta min:",t_min)
		print("Job",id,"T-Delta max:",t_max)

		print("Job Writing File"+str(id),"Complete")
		print("Start:",_start_time)
		print("end:",_end_time)
		print("Time Diff:",str((_end_time-_start_time)))
		
		
		return
if __name__=="__main__":
	TEST=False
	if len(sys.argv)>1:
		if sys.argv[1].upper()=="-T":
			TEST=True
	if not(SA._initL()):
		print("Error creating L list")
		quit()
	total=len(SA.L)
	try:
		TF=SA(0,total)
	
	except ValueError as e:
		print (e)
		quit()
	
	print("TIME DELTA CSV generator")
	if TEST:
		print("##Test-Mode::ENABLED##")
		print()	
		TF.gentimeDelta(0,10)
	else:
		print()	
		TF.gentimeDelta()
	
	print()	
	print("Len: ",len(TF.lines))
	print("first-line[0]:")
	
	print(TF.lines[0])
	
	#TF.wirteTimeDelta()
	
