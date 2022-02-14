import socket
from threading import Thread
import fread as FR
from multiprocessing import cpu_count, Process
from os import listdir, mkdir, getpid
from os.path import isdir, isfile, exists
from shutil import copyfile
from time import sleep
from math import floor
import url_tree as UT
import url_session as US
import datetime
from socket import gethostname
from extra_func import readSess, writeSess
import psutil
import sys

class Client:
	HOST=None
	PORT=None
	s=None
	workers=0
	_chunk_size=0
	_start=0
	_end=0
	P=[]
	cond=True
	gen_on_last=True
	NOD=4
	
	def recv(self):
		print("Hmmm")
		
	def job(self,pid):
		self.F[pid].genMeta()
		#if not Client.cond:
			#self.F[pid].genTreefromM()
		self.F[pid].summary()
		self.F[pid].writeSessions()
		if Client.cond:
			self.F[pid].writeTrees()
		
		return
		
	def _init(self, H,P):
		self.HOST=H
		self.PORT=P
		try:
			self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		except:
			print("Error creating socket")
			return False
		try:
			print("Connecting to:",self.HOST,self.PORT)
			self.s.connect((self.HOST,self.PORT))
		except:
			print("Error connecting to server",self.HOST, self.PORT)
			return False
		return True	

	def map(self):
		
		print("Chunk size",Client._chunk_size,"Start:",Client._start,"End:",Client._end)
		_p=[]
		for i in range(self.workers):
			_p.append(None)
		j=0
		_start_time=datetime.datetime.now()
		for i in range(Client._start,Client._end,Client._chunk_size):
			
			end=i+Client._chunk_size
			if (end>Client._end):
				end=Client._end
			try:
				self.F[j]=FR.Fread(i,end,Client.P[j],Client.cond)
			except ValueError as e:
				print (e)
				return
				
			_p[j]=Process(target=self.job, args=(Client.P[j],))
			##multi process here
			
			_p[j].start()
			j+=1
		for j in range(self.workers):
			_p[j].join()
		
		_end_time=datetime.datetime.now()
		print("Chunk size",Client._chunk_size,"Start:",Client._start,"End:",Client._end,"Complete")
		print("Start:",_start_time)
		print("End:",_end_time)
		print("Delta:",str(_end_time-_start_time)+"\n")
		return
	def readThread (st, tree):
		tree.readTree(st)

	def job2(self,f1,f2,path):
		if not exists(path+"gen/"):
			print("Path doesn't exists:",path+"gen/")
		print("Tree accu:",path,f1,"to",f2)
		_start_time=datetime.datetime.now()
		for i in range (4):
			_p=[None,None]
			s1=path+str(f1)+"_"+str(i)+"_Tree.txt"
			if not isfile(s1):
				print (s1,"file doesnt exist")
				return
			s2=path+str(f2)+"_"+str(i)+"_Tree.txt"
			if not isfile(s2):
				print(s2,"file doesnt exist")
				return
			tree1=UT.UTree(Client.cond)
			tree2=UT.UTree(Client.cond)
			_p[0]=Thread(target=Client.readThread,args=(s1,tree1,))
			_p[1]=Thread(target=Client.readThread,args=(s2,tree2,))
			_p[0].start()
			_p[1].start()
			_p[0].join()
			_p[1].join()
			tree1.mergeTree(tree2)
			tree1.writeTree(path+"gen/"+str(floor(f1/2))+"_"+str(i)+"_Tree.txt")
			
		_end_time=datetime.datetime.now()
		
		
		print("Tree accu",path,f1,"to",f2,"Complete")
		print("Start:",_start_time)
		print("End:",_end_time)
		print("Delta:",str(_end_time-_start_time))
		print("Mem:",psutil.Process(getpid()).memory_info().rss / 1024 ** 2,"MB\n")
		
	def advFile(self, st,num,num2):

		for i in range(4):
			f1.open(st+str(num)+"_"+str(i)+"_Tree.txt","r")
			f2.open(st+"gen/"+str(num2)+"_"+str(i)+"_Tree.txt","w")
			line=f1.readline()
			while line: 
				f2.write(line[:-1])
				line=f1.readline()
			f1.close()
			f2.close()
	
	def job3(self,f1,f2,path):
		if not exists(path+"gen/"):
			print("Path doesn't exists:",path+"gen/")
		print("Session accu:",path,f1,"to",f2)
		_start_time=datetime.datetime.now()
		max_m=0
		for i in range (4):
			M=[]
			_p=[None,None]
			s1=path+str(f1)+"_"+str(i)+".txt"
			if not isfile(s1):
				print (s1,"file doesnt exist")
				return
			s2=path+str(f2)+"_"+str(i)+".txt"
			if not isfile(s2):
				print(s2,"file doesnt exist")
				return
			s3=path+"gen/"+str(floor(f1/2))+"_"+str(i)+".txt"
			M1=[]
			M2=[]
			#print(s1,s2)
			_p[0]=Thread(target=readSess,args=(s1,M1,Client.cond,))
			_p[1]=Thread(target=readSess,args=(s2,M2,Client.cond,))
			_p[0].start()
			_p[1].start()
			_p[0].join()
			_p[1].join()
			#print("test")
			min_time=M2[0]._stime
			l_m2=len(M2)
			l_m1=len(M1)
			x=1
			C=[]
			while True:
				if x>=l_m2:
					break
				if M2[x]._stime<min_time:
					min_time=M2[x]._stime
				elif (M2[x]._stime-min_time).total_seconds()>=datetime.timedelta(minutes=60).total_seconds():
					break	
				x+=1
			#print(x)
			y=l_m1-1
			while True:
				if y<0:
					break
				if (min_time-M1[y]._etime).total_seconds()<datetime.timedelta(minutes=60).total_seconds():
					_temp=M1[y]
					t=0
					while t<x:
						if M2[t].ip==_temp.ip:
							for each in M2[t].S:
								##maybe have issue
								#print(each)
								_temp.addS(each,M2[t]._etime)
							M2.remove(M2[t])
							t-=1
							C.append(_temp)
						t+=1
						
					
				else:
					break
				y-=1
			#print (y)
			new_M=[]
			for a in range(y+1):
				new_M.append(M1[a])
			for a in range (len(C)):
				new_M.append(C[a])
			for a in range (len(M2)):
				new_M.append(M2[a])
			temp_m=psutil.Process(getpid()).memory_info().rss / 1024 ** 2
			if temp_m>max_m:
				max_m=temp_m
			writeSess(s3,new_M,self.cond)
			del M1
			del M2
			del C 
			#print (M1,M2,C) 		##test if really delete
		print("Session accu:",path,f1,"to",f2, "Complete")
		_end_time=datetime.datetime.now()
		print("Start:",_start_time)
		print("End:",_end_time)
		print("Delta:",str(_end_time-_start_time))
		print("Mem max:",max_m,"MB\n")
		return	
	def job4(st,i,j):
		print("Tree Gen at LAST",i," ",j,"start")
			
		_start_time=datetime.datetime.now()
		st1=st+str(i)+"_"
		st2=st+str(i)+"_"+str(j)+"_Tree.txt"
		M=[]
		T=UT.UTree(True)
		

		readSess(st1+str(j)+".txt",M,Client.cond)
		for n in range(len(M)):
			for x in range(len(M[n].S)):
				U=T.addItem(M[n].S[x].url)
				M[n].S[x].n=U.id
		
		print("Tree Gen at LAST:",i," ",j, "Complete")
		_end_time=datetime.datetime.now()
		print("Start:",_start_time)
		print("End:",_end_time)
		print("Delta:",str(_end_time-_start_time))
		temp_m=psutil.Process(getpid()).memory_info().rss / 1024 ** 2
		print("Mem max:",temp_m,"MB\n")
		writeSess(st1+str(j)+".txt",M[m],True)
		T.writeTree(st2)
		return	
	def reduce(self):
		max_w=self.workers
		
		st="./"+FR.Fread.ODIR
		if not exists(st):
			print("No gen data")
			return
		i=0
		while True:
			
			D=listdir(st)
			D.sort()

			t_files_p1=[]
			t_files_p2=[]
			t_files_p3=[]
			t_files_p4=[]
			files_p1=[]
			files_p2=[]
			files_p3=[]
			files_p4=[]		
			for d in D:
				#print(d)
				if Client.cond:
					if str(len(t_files_p1))+"_0_Tree.txt"== d:
						t_files_p1.append(d)
					elif str(len(t_files_p2))+"_1_Tree.txt" == d:
						t_files_p2.append(d)
					elif str(len(t_files_p3))+"_2_Tree.txt" == d:
						t_files_p3.append(d)
					elif str(len(t_files_p4))+"_3_Tree.txt" == d:
						t_files_p4.append(d)
				if str(len(files_p1))+"_0.txt"== d:
					files_p1.append(d)
				elif str(len(files_p2))+"_1.txt" == d:
					files_p2.append(d)
				elif str(len(files_p3))+"_2.txt" == d:
					files_p3.append(d)
				elif str(len(files_p4))+"_3.txt" == d:
					files_p4.append(d)
			if Client.cond:
				l1=len(t_files_p1)
				l2=len(t_files_p2)
				l3=len(t_files_p3)
				l4=len(t_files_p4)
			
			f1=len(files_p1)
			f2=len(files_p2)
			f3=len(files_p3)
			f4=len(files_p4)
			
			if Client.cond:
				if l1!=l2 or l3!=l4 or l1!=l4:
					print(i,"ERROR: tree file missmatch discreancies my division")
					break
			if f1!=f2 or f3!=f4 or f1!=f4:
				print(i,"ERROR: session file missmatch discreancies my division")
				break
			if Client.cond:
				if l1!=f1:
					print(i,"ERROR: tree to session file missmatch discreancies my division")
					break
			
			times=floor(f1/2)
						
			if times>max_w:
				print(i,"ERROR: more files than expected workers")
				return
			_p=[]
			_m=[]
			if f1>1:
				if not isdir(st+"gen/"):
					mkdir(st+"gen/")
			print("\nSTAGE#:"+str(i),"path="+st+"' items:",f1)				
			if Client.cond:	
				for j in range(times):
					_p.append(None)
					_p[j]=Process(target=self.job2, args=(2*j,(2*j)+1,st,))
					_p[j].start()
			for j in range(times):
				_m.append(None)
				_m[j]=Process(target=self.job3, args=(2*j,(2*j)+1,st,))
				_m[j].start()
			if  f1%2 !=0 and f1>1:
				_o=Process(target=self.advFile, args=(st,f1-1,times+1,))
				_o.start()
			for j in range(times):
				if Client.cond:
					_p[j].join()
				_m[j].join()
			if  f1%2 !=0 and f1>1:
				_o.join()
			if not exists(st+FR.Fread.ODIR):
				print("Merge Complete...")
				break
			st+=FR.Fread.ODIR
			i+=1
		if not Client.cond and Client.gen_on_last:  ##Gen tree at end here if Client.cond is False
			_d=[]
			for j in range(Client.NOD):
				_d.append(None)
				_d[j]=Process(target=Client.job4, args=(st,0,j,))
				_d[j].start()
			for j in range(Client.NOD):
				_d[j].join()			
				
	def __init__(self,H,P,w):
		
		self._end_time=None
		self.F=[]
		print("Initializing..")
		if(not(self._init(H,P))):
			raise ValueError("Error Initializing")
		print("Connected.")
		t=int.from_bytes(self.s.recv(8),"big")
		if w>cpu_count() or w<=0:
			raise ValueError("worker param invalid")
		if not(FR.Fread._initL()):
			print("Error creating L list")
			quit()
		self.workers=w
		for i in range(0,self.workers):	
			Client.P.append(i)
			self.F.append(None)
		self._start_time=datetime.datetime.now()	
		print (Client.P)
		print("Workers:",self.workers)
		if t==5:
			self.s.send(int.to_bytes(self.workers,1,"big"))
			
			temp=self.s.recv(128).decode("utf-8")
			temp=eval(temp)
			print(temp)
			Client._chunk_size=int(temp[0])
			Client._start=int(temp[1])
			Client._end=int(temp[2])
			Client.cond=bool(temp[3])
			if Client.cond:
				print("Client mode: Tree FIRST mode")
			else:
				print("Client mode: Tree LAST mode")
			##Works starts here
			self.map()
			self.reduce()
			
			self.s.send(int.to_bytes(255,1,"big"))
	def summary(self):
		print("Client:",gethostname())
		print("Start:",self._start_time)
		self._end_time=datetime.datetime.now()
		print("end:",self._end_time)
		print("Time Diff:",str(self._end_time-self._start_time))
		
	def __del__(self):
		self.summary()
		if self.s:
			print("closing socket")
			self.s.close()
			
	def print(self):
		self.F.writeTrees()
		#self.
	
if __name__=="__main__":
	if len(sys.argv)>1:
		if sys.argv[1].upper()!="-L":
			Client.gen_on_last=False
	_max_now=cpu_count()
	_now=int(input("Enter number of workers:"))				##NUmber of workers
	
	while _now>_max_now or _now<=0:
		_now=int(input("Enter number of workers:"))
	
	ip=str(input("IP: "))
	try:
		port=int(input("port:"))
	except:
		print("Invalid Port")
		quit()
	try:
		c=Client(ip,port,_now)	
	except ValueError as e:
		print(e)
		quit()
	except:
		print("Unknow Error")
		quit()
	
	
