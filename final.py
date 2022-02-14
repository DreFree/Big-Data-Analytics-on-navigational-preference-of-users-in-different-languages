from os.path import isdir, isfile, exists
import url_tree as UT
import url_session as US
import datetime
from multiprocessing import cpu_count, Process
from threading import Thread
from extra_func import readSess, writeSess
from math import floor
from os import listdir, mkdir, getpid
import sys
import fread as FR
import psutil

NOD=4
cond=False

def readThread (st, tree):
		tree.readTree(st)
def job2(f1,f2,path):
	global cond
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
		tree1=UT.UTree(cond)
		tree2=UT.UTree(cond)
		_p[0]=Thread(target=readThread,args=(s1,tree1,))
		_p[1]=Thread(target=readThread,args=(s2,tree2,))
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
	

def job3(f1,f2,path):
	global cond
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
		_p[0]=Thread(target=readSess,args=(s1,M1,cond,))
		_p[1]=Thread(target=readSess,args=(s2,M2,cond,))
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
		writeSess(s3,new_M,cond)
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
	global cond
	print("Tree Gen at LAST",i," ",j,"start")
		
	_start_time=datetime.datetime.now()
	st1=st+str(i)+"_"
	st2=st+str(i)+"_"+str(j)+"_Tree.txt"
	M=[]
	T=UT.UTree(True)
	
	
	readSess(st1+str(j)+".txt",M,cond)
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
	writeSess(st1+str(j)+".txt",M,True)
	T.writeTree(st2)
	return
		
def reduce():
	global NOD
	global cond
	max_w=2
	
	st="./fin/"

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
		if cond:
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
	if cond:
		l1=len(t_files_p1)
		l2=len(t_files_p2)
		l3=len(t_files_p3)
		l4=len(t_files_p4)
	
	f1=len(files_p1)
	f2=len(files_p2)
	f3=len(files_p3)
	f4=len(files_p4)
	
	if cond:
		if l1!=l2 or l3!=l4 or l1!=l4:
			print(i,"ERROR: tree file missmatch discreancies my division")
			return
	if f1!=f2 or f3!=f4 or f1!=f4:
		print(i,"ERROR: session file missmatch discreancies my division")
		return
	if cond:
		if l1!=f1:
			print(i,"ERROR: tree to session file missmatch discreancies my division")
			return
	
	times=floor(f1/2)
				
	if times>max_w:
		print(i,"ERROR: more files than expected workers")
		return
	_p=[]
	_m=[]
	if f1>1:
		if not isdir(st+"gen/"):
			mkdir(st+"gen/")
	print("\nSTAGE#:"+str(0),"path="+st+"' items:",f1)				
	if cond:	
		for j in range(times):
			_p.append(None)
			_p[j]=Process(target=job2, args=(2*j,(2*j)+1,st,))
			_p[j].start()
	for j in range(times):
		_m.append(None)
		_m[j]=Process(target=job3, args=(2*j,(2*j)+1,st,))
		_m[j].start()

	for j in range(times):
		if cond:
			_p[j].join()
		_m[j].join()

	if not exists(st+FR.Fread.ODIR):
		print("Merge Complete...")
		return
	
	st+="gen/"
	if not cond:  ##Gen tree at end here if Client.cond is False
		_d=[]
		for j in range(NOD):
			_d.append(None)
			_d[j]=Process(target=job4, args=(st,0,j,))
			_d[j].start()
		for j in range(NOD):
			_d[j].join()	
				
if __name__=="__main__":
	if len(sys.argv)<2:
		print("param missing")
		quit()
	if sys.argv[1].upper()=="-F":
		cond=True
	
	print("FINAL:")
	if cond:
		print("Tree FIRST mode")
	else:
		print("Tree LAST mode")
	reduce()		
