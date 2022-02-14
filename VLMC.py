from copy import deepcopy
from os import getpid
import multiprocessing
from threading import stack_size
import vlmc_tree as VT
from extra_func import readSess, sesToarr, Alt_trans
from os.path import exists
import sys
##import resource


sys.setrecursionlimit(10000)


IFILE="gen/"
OFILE="v_res/"
k= 0.005
Q=0.0000000001

def Alt_T(data):
	i=0
	while i<len(data)-1:
		if data[i]==data[i+1]:
			data.remove(data[i])
			i-=1
		i+=1

def job(ID,a):
	global k, Q,IFILE,OFILE
	print("ID "+str(ID)+" _ "+str(a)+" :","JOb started")
	v=None
	VT.VTree.k=k
	VT.VTree.Q=Q
	try:
		v=VT.VTree()
		
	except  ValueError as e:
		print(e)
		print("FAIL")
		return
	
	data=[]
	readSess(IFILE+str(ID)+"_"+str(a)+".txt",data,True)
	

	data=sesToarr(data)
	
	for each in data:
		L=[]
		for i,n in enumerate(each):
			if i==0:
				L.append("*")
			L.append(str(n))
		
		if len(L)<2500:
			Alt_T(L)
			v.addItem(L)
		#else:
			#print(L)

	v.genprobKL()
	#print()
	#print("OK")	
	#v.showTree(jj=3)
	
	v.prune()
	print("ID",ID,"_",a,":",v._show_pruneamt())
	#print()
	#v.showTree()		
	v.genResults(f=3)
	print("VTree write complete")
	v.writeResults(OFILE+str(ID)+"_"+str(a)+".txt")
	#print("VTree write complete")
	print("ID "+str(ID)+" _ "+str(a),":","JOb complete")
	return

if __name__=="__main__":
	
	if not exists(IFILE):
		print("Result director missing",IFILE)
		quit()

	ID=int(input("Enter ID value: "))
	print("k prune factor: ",k)
	_p=[None,None,None]
	#_p=[None]					##testing purposes

	for i in range(len(_p)):
		_p[i]=multiprocessing.Process(target=job, args=(ID,i,))
		_p[i].start()
	for i in range(len(_p)):
		_p[i].join()
	print("END")
	
