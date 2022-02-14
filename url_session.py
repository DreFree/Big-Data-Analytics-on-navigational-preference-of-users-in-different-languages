from multiprocessing import Lock
class SNode:
	def __init__(self,n,time=None):
		if isinstance(n, int):
			if time:
				self.time=time
			self.n=n
			self.url=""
			self.os=None
			self.browser=None

		elif isinstance(n, str):
			if time:
				self.time=time
			self.n=None
			self.url=n
			self.os=None
			self.browser=None
		elif isinstance(n, SNode):
			if time:
				self.time=time
			self.n=n.n
			self.url=n.url
			self.os=n.os
			self.browser=n.browser
		elif isinstance(n,list) and len(n)==4:
			if time:
				self.time=n[1]
			self.n=None
			self.url=""
			if isinstance(n[0], int):
				self.n=n[0]
			elif isinstance(n[0], str):
				self.url=n[0]
			self.browser=n[2]
			self.os=n[3]
		else:
			print("unknown n:",n,type(n))
			self.time=None
			self.n=None
			self.url=""
			self.os=None
			self.browser=None
	def setN(self,n):
		if isinstance(n, int):
			self.n=n
		else:
			print("param expected int",type(n))
		return
		
	def clearUrl(self):
		self.url=""
		return
	def getN(self):
		return self.n
	
class SSession:
	def __init__(self,ip):
		if isinstance(ip,str):
			self._stime=0
			self._etime=0
			self.ip=ip
			self.S=[]
		elif isinstance(ip,SSession):
			self._stime=ip._stime
			self._etime=ip._etime
			self.ip=ip.ip
			self.S=[]
			for each in ip.S:
				self.S.append(SNode(each))
				
	def __del__(self):
		for each in self.S:
			#self.S.remove(each)
			del each
	def addS(self, n,time):
	
		if self._stime==0:
			self._stime=time
		self.S.append(n)
		self._etime=time
	
		

