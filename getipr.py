from datapackage import Package

package = Package('https://datahub.io/core/geoip2-ipv4/datapackage.json')

# print list of all resources:
print(package.resource_names)

# print processed tabular data (if exists any)
f=open("iplist.txt","w")
print("Working...")
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
        lines=resource.read()
        for i,line in enumerate(lines):
            ip=line[0].split("/")
            _first=ip[0]
            _temp=ip[0].split(".")
            _sec=_temp[0]+"."+_temp[1]+"."+_temp[2]+"."+ip[1]
            _con=line[5]
            if not _con:
                _con="NA"
            if _con=="-":
                _con="NA"

            if i!=0:
                f.write("\n")
                
            f.write(_first)
            f.write(",")
            f.write(_sec)
            f.write(",")
            f.write(str(_con))
            
f.close()
print("Complete")