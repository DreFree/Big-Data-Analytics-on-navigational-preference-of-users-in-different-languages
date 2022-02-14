from sklearn.cluster import KMeans

from yellowbrick.cluster import KElbowVisualizer
import numpy as np
from os.path import exists
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy
from scipy import stats
import random
from math import floor
from multiprocessing import Process
import sys


cent=None
SHOW= False
TDIR="tgen/"
noc=-1

def check(id=-1):
	global TDIR
	if id<0:
		for i in range(3):
			if not exists(TDIR+"tdelta"+str(i)+".txt"):
				return False
	else:
		if not exists(TDIR+"tdelta"+str(id)+".txt"):
			return False
			
	return True
def zero_reduction(var):
	temp=[]
	print("ZERO REduction ENABLED")
	for eac in var:
		if eac!=0:
			temp.append(eac)
	return np.array(temp)
	
def IQR_outlier_reduction(var):
	var2=deepcopy(var)
	var2.sort()
	q_1,q_3 = np.percentile(var2, [25,75])
	IQR= q_3 - q_1
	fact=3
	lower_bound = q_1 - (IQR * fact)
	upper_bound = q_3 + (IQR * fact)
	print("IQR Reduction @",str(fact)+"*IQR")
	print("quater1:",q_1,"quater3:",q_3)
	print("bounds:",lower_bound,"to",upper_bound)
	temp=[]
	for each in var2:
		if each>lower_bound and each<upper_bound:
			temp.append(each)
			
	return np.array(temp)
	
def selected_outlier_reduction(var,lo_b,up_b):
	var2=deepcopy(var)
	var2.sort()
	print("Pre-Selected outlier Reduction")
	print("bounds:",lo_b,"to",up_b)
	temp=[]
	for each in var:
		if each>lo_b and each<up_b:
			temp.append(each)
			
	return np.array(temp)
def z_score_outlier_reduction(var):
	threshold=3
	print("Z-score threshold @3 reduction ENABLED")
	var_mean= np.mean(var)
	var_sd=np.std(var)
	z_scores = [(i-var_mean)/var_sd for i in var]
	temp=[]
	for each in var:
		if (each-var_mean)/var_sd < threshold:
			temp.append(each)
			
	return np.array(temp)
	
def readTD(id=0):
	global L
	if not check():
		print("Check test failed.")
		return False
	F=open(TDIR+"tdelta"+str(id)+".txt", "r")
	lines=F.readlines()
	F.close()
	for line in lines:
		sec=line.split(",")
		for eac in sec:
			if eac[len(eac)-1]=="\n":
				eac=eac[:-1] 
			L.append(eac)

	return True
def binner(var,b):
	l3=deepcopy(var)
	l3.sort()
	
	hist, bin_edges=np.histogram(l3,bins=b,density=False)
	
	
	t_h=0
	for h in hist:
		t_h+=h
	print()
	print("BINs data:")
	print("%12s   %12s %12s    %4s"%("From","To","AMT","Per%"))
	
	for i,h in enumerate(hist):
		print("%12.2f   %12.2f %12d    %4.2f"%(bin_edges[i],bin_edges[i+1],h,(h/t_h)*100))
	print("Total AMT of timedeltas:",t_h)
	return hist, bin_edges
def hist(L,id=0,b=50,cond=False):
	global SHOW
	hist, bin_edges=binner(L,b)
	l3=deepcopy(L)
	l3.sort()
	print()
	print("ID",id,"Histogram data")
	print("Total number of Bins",len(hist))
	dist = pd.DataFrame(l3,columns=['a'])
	print(dist.agg(['min', 'max', 'mean', 'std','median']).round(decimals=2))
	
	#plt.hist(hist)
	if SHOW:
		n, bins, patches = plt.hist(x=l3, bins=bin_edges, color='#0504aa',alpha=0.7,rwidth=0.85)
		plt.grid(axis='y',alpha=0.75)
		plt.xlabel('TimeDelta')
		plt.ylabel('Frequency')
		plt.title('Visualization')
		if cond:
			maxfreq = hist.max()
		else:
			maxfreq =5500
		plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
		plt.show()
	
def KDE():
	global L
	means = L.mean()
	stdevs = np.std(L)
	dist = pd.DataFrame(L,columns=['a'])
	print("TimeDetla (seconds) summary")
	print(dist.agg(['min', 'max', 'mean', 'std','median']).round(decimals=2))
	
	fig, ax = plt.subplots()
	dist.plot.kde(ax=ax, legend=False, title='Histogram: A')
	dist.plot.hist(density=True, ax=ax)
	ax.set_ylabel('Probability')
	ax.grid(axis='y')
	ax.set_facecolor('#d8dcd6')
	
	#plt.ylim(ymax=0.00000005)
	plt.show()

def KMean(L,id =0,noc=1):
	global F,cent
	L2=np.array([[abs(n)] for n in L])
	hist(L,id,100,True)
	kmeans = KMeans(n_clusters=noc, random_state=0)
	res=kmeans.fit_predict(L2)
	cent=kmeans.cluster_centers_
	cent=cent.astype(int)
	
	F=[]
	for i,eac in enumerate(res):
		F.append([eac,L2[i][0]])
	
	return 

def MD(var):			##Mean deviation
	sum=0
	mean=np.mean(var)
	for eac in var:
		sum+=(abs(eac-mean))
	return sum/len(var)
	
def final(id=0):
	global F,cent
	
	
	"""
	for i in range(len(cent)):
		if cent[select]<cent[i]:
			select=i
	"""
	T=[]
	t_sum=0
	for i in range(len(cent)):
		T1=[]
		for eac in F:
			if eac[0]==i:
				T1.append(eac[1])
		tl=len(T1)
		t_sum+=tl
		T.append(T1)
	print()
	print("ID",id,"Cluster Centers:")
	print("%9s   %9s   %5s   %9s   %9s   %9s"%("C_center","AMT","Per%","STD","Mean-Dev","Proposed"))

	for i in range(len(cent)):
		tl=len(T[i])
		std=np.std(T[i])
		print("%9d   %9d   %5.2f   %9.2f   %9.2f   %9.2f"%(cent[i],tl,tl/t_sum*100,std,MD(T[i]),std+cent[i]))
	print()	
	
def select_k(L):		##Elbow Method for K-means
	global SHOW
	model = KMeans()
	L2=np.array([[abs(n)] for n in L])
	# k is range of number of clusters.
	visualizer = KElbowVisualizer(model, k=(2,10), timings= True)
	visualizer.fit(L2)        # Fit data to visualizer
	print("Elbow Method seleted k:",visualizer.elbow_value_)
	if SHOW:
		visualizer.show() 
	return visualizer.elbow_value_
def select_k2(L):		##Elbow Method for K-means
	global SHOW
	max_c=10
	min_c=2
	L2=np.array([[abs(n)] for n in L])
	dis=[]
	iner=[]
	# k is range of number of clusters.
	for i in range(min_c,max_c+1):
		model = KMeans(n_clusters=i)
		model.fit(L2)
		iner.append(model.inertia_)

	from kneed import KneeLocator
	x = range(min_c, len(iner)+min_c)
	kn = KneeLocator(x, iner, curve='convex', direction='decreasing')
	print("Elbow Method seleted k:",kn.knee)
	if SHOW:
		plt.xlabel('number of clusters k')
		plt.ylabel('Sum of squared distances')
		plt.plot(x, iner, 'bx-')
		plt.vlines(kn.knee, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')
		plt.show()
	return kn.knee
	
def job(id,k=-1):
	global L, L2,noc
	L=[]
	L2=[]
	div=["ENGLISH","CHINESE","BOTH"]
	if not readTD(id):
		quit()
	if len(L)==0:
		print("L is empty")
		quit()
	L=np.array(L)
	L=L.astype(float)
	L=np.array([abs(n) for n in L])
	
	#print(L)
	print()
	print("FOR:",div[id])
	print(L)
	##h,e=binner(L,100)
	hist(L,id,100,True)
	print()
	L=zero_reduction(L)
	#L=selected_outlier_reduction(L,e[0],e[2])
	L=IQR_outlier_reduction(L)
	#L=z_score_outlier_reduction(L)

	print()
	print(L)
	
	
	##L2=np.array([[abs(n)] for n in L])
	if k<0:
		k=select_k2(L);
	else:
		print("Pre-selected K:",k)
	
	#hist(b=4)
	KMean(L,noc=k,id=id)
	final(id)
	return
	
if __name__=="__main__":
	k=-1
	if len(sys.argv)>1:
		if sys.argv[1].upper()=="-S":
			SHOW=True
		if len(sys.argv)>2:
			if sys.argv[2].isnumeric():
				k=int(sys.argv[2])

	job(2,k)
		
	
	#hist()
	#KDE()
	
