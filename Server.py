import socket
import netifaces as ni
import multiprocessing
import threading
import os
import sys
import signal
from math import ceil

T=None
S1=None

class Server:
	s=None
	Q=1
	conn=[]
	c=0
	isTerminating=False
	PORT=None
	L=0
	workers=0
	_worker=[]
	chunk_size=0
	TEST=False		##to Enable test mode of 20 files
	_cond=False		##TRUE:to indicate client default to tree first mode 
	
	def _initServer(self, P):
		self.PORT=P
		iface=ni.interfaces()
		print("interface:",iface[len(iface)-1])
		HOST=ni.ifaddresses(iface[len(iface)-1])[ni.AF_INET][0]['addr']
		print("Initializing server socket: ",HOST,P)
		print(socket.gethostname())
		try:
			self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		except:
			print("Error creating socket")
			return False
		try:
			print("Binding..")
			self.s.bind((HOST,P))
		except:
			print("Error binding socket")
			return False
		return True	
	def _initList(self):
		l="list.txt"
		try:
			f=open(l,"r")
		except:	
			return False
		lines=f.readlines()
		self.L=len(lines)
		
		f.close()
		if self.L<=0:
			print(l,"is empty")
			return False
		print("List total:",self.L)
		return True	
		
	def __init__(self,PORT):
		if not(self._initList()):
			raise ValueError("List initialization error")
		if not(self._initServer(PORT)):
			raise ValueError("Initialization failed")
		

		
	def listen(self):
		con=None
		addr=None
		try:
			self.s.listen(self.Q)

		except:
			print("Error listening...")
		print("Awaiting connection. Total:",self.Q)
		for i in range(self.Q):
			try:
				con, addr=self.s.accept()
				self.conn.append(con)
				self.c+=1
			except:
				print("Error connecting",con,addr)
				
			print("Client",self.c, addr,"connected")
			##Mutext lock here maybe
			## but this is multiprocessed so dont need to
			## multi thread then maybe
			
		for each in self.conn:
			each.send(int.to_bytes(5,1,"big"))
			self._worker.append(int.from_bytes(each.recv(8),"big"))
			self.workers+=self._worker[len(self._worker)-1]
		
		L=self.L
		if Server.TEST:
			L=20
			
		self.chunk_size=ceil(L/self.workers)
		print("Chunk size:",self.chunk_size,"Workers:",self.workers)
		
		for i,each in enumerate(self.conn):
			if i==0:
				s=i*self.chunk_size*0
			else:
				s=i*self.chunk_size*self._worker[i-1]
			e=s+(self.chunk_size*self._worker[i])
			if (e>=self.L):
				e=self.L
			print("Client",i+1,':',s,'-',e,"  :",self._worker[i])
			packet=str([self.chunk_size,s,e,Server._cond])
			each.sendall(packet.encode())
		for i,each in enumerate(self.conn):
			tmp=int.from_bytes(each.recv(2),"big")
			if tmp==255:
				print("Client",i+1,': Completed')


			
			
	def _chunksize(self):
		return
		
	
	def accept(con):
		print("Hao",con)
		##NO con.close() will close in parent process
	
	def __del__(self):

		for each in self.conn:
			try:
				each.close()
			except:
				print("b")
		try:
			self.s.close()
		except:
			print("aaa")
			
		print("Closing server socket")
		
def cmdUI(Ppid,S1):
	while True:
		c=input("Enter Q to terminate\n")
		if c.upper()=='Q':
			print("Terminating input detected.")
			S1.__del__()		
			#os.kill(Ppid,signal.SIGSTOP)
			os._exit(os.EX_OK)
			
if __name__ =="__main__":
	
	try:	
		port=int(input("Port: "))
	except:
		print("Invalid port")
		quit()
	try:
		Q=int(input("Num of Clients:"))
	except:
		print("Expected number")
		quit()
	if Q>1:
		Server.Q=Q
	try:
		S1=Server(port)
	except ValueError as e:
		print(e)
		quit()
	if len(sys.argv)>1:
		if sys.argv[1].upper()=="-T":
			Server.TEST=True
			
	print("Default mode: Tree LAST mode")
	c=input("Type Y/y to switch to tree FIRST mode: ")
	print()
	if c.upper()=="Y":
		Server._cond=True
	if Server._cond:
		print("Mode: Tree FIRST mode")
	else:
		print("Mode: Tree LAST mode")
	
	if Server.TEST:
		print("TEST ENABLED...")
	print()
	#nstdin = os.fdopen(os.dup(sys.stdin.fileno()))
	T=threading.Thread(target=cmdUI,args=(os.getpid(),S1))
	T.start()
	S1.listen()
	T.join()			## process will wait for all threads to complete anyway
	
	
			
