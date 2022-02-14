import os
from extra_func import readSess

m=[]
readSess("./gen/0_0.txt",m)
print(m[0])

L=os.listdir("./gen/")
if os.path.exists("./gen/"):
	print ("YEA")
	
#print(L)
"""
for l in L:
	if ".txt" in l:
		print(l)
	if os.path.isdir("./gen/"+l):
		print ("DIR:",l)
st="./gen"
"""
for i in range(5,0,-1):
	print (i)
	
#print (m)
#print (n)
