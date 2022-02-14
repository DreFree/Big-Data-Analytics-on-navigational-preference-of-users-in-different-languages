from extra_func import isValidURL
from operator import itemgetter
from url_tree import UTree as UT
url= "www.csie.ndhu.edu//.css.js"

PATH="gen/"
ID= 15

print(isValidURL(url))
url=url.replace("//","/")
print(url)

U=UT()

ID=int(input("ID: "))
i =0
U.readTree(PATH+str(ID)+"_"+str(i)+"_Tree.txt")
#U.showTree()
U.equalizer()
#U.showTree()
L=[]

U.getDLevel(L,3)
L.sort(key=itemgetter(1),reverse=True)
print()
tot=0
for each in L:
    tot+=each[1]
print("Total: ",tot)
for each in L:  
    print("%30s %10d %10f"%(each[0],each[1],each[1]/tot))

print("List len",len(L))