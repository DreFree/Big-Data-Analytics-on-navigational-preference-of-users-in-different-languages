from fread import Fread
from operator import itemgetter

OFILE="gen_bots.txt"
L=[]
def add(val):
    global L
    for item in L:
        if val==item[0]:
            item[1]+=1
            return
    L.append([val,1])

if __name__ =="__main__":
    if not Fread._initL():
        print("List error")
        quit()

    try:
        F=Fread(0,342,9,False)
    except:
        print('ERror')
        quit()


    DIR=Fread.IDIR
    for i in range(len(Fread.L)):
        f=open(Fread.IDIR+Fread.L[i],"r")
        lines=f.readlines()
        for line in lines:
            line=line.split(" ")
            if (line[5][1:].upper()!="GET"):
                continue

            if "robots.txt" in line[6]:
                #temp=[]
                #for i in range(1):
                   # try:
                     #   temp.append(line[13])
                  #  except:
                     #   break
                #L.append(temp)
                try:
                    add(line[13])
                except:
                    try:
                        add(line[12])
                    except:
                        try:
                            add(line[11])
                        except:
                            add("NA")
        f.close()

    L.sort(key=itemgetter(1))
    f=open(OFILE,"w")
    if not f:
        print("FAiled to create file")
        quit()
    for item in L:
        f.write(item[0])
        f.write(" , ")
        f.write(str(item[1]))
        f.write("\n")
    f.close()
