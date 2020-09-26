from django.shortcuts import render
import pandas as pd
import zipfile
import datetime
def home(request):
        if request.method == "POST":
            screenname = request.POST.get("handle", None)
            
            
            MTCstop = pd.read_csv('MTCdata/stop_times.txt', low_memory=False)
            MTCstop_name=pd.read_csv('MTCdata/stops.txt', low_memory=False)
            MTCroute=pd.read_csv('MTCdata/trips.txt', low_memory=False)
            MTCroutename=pd.read_csv('MTCdata/routes.txt', low_memory=False)
            MTCarrival=pd.merge(MTCstop,MTCstop_name,on="stop_id")
            MTCarrival=pd.merge(MTCarrival,MTCroute,on="trip_id")
            MTCarrival=pd.merge(MTCarrival,MTCroutename,on="route_id")
            MTCgrouped=MTCarrival.groupby("stop_name")


            CRMLstop = pd.read_csv('CRMLdata/stop_times.txt', low_memory=False)
            CRMLstop_name=pd.read_csv('CRMLdata/stops.txt', low_memory=False)
            CRMLroute=pd.read_csv('CRMLdata/trips.txt', low_memory=False)
            CRMLroutename=pd.read_csv('CRMLdata/routes.txt', low_memory=False)
            CRMLarrival=pd.merge(CRMLstop,CRMLstop_name,on="stop_id")
            CRMLarrival=pd.merge(CRMLarrival,CRMLroute,on="trip_id")
            CRMLarrival=pd.merge(CRMLarrival,CRMLroutename,on="route_id")
            CRMLgrouped=CRMLarrival.groupby("stop_name")

            st=screenname
            r=""
            if st in MTCgrouped.groups:
                group=MTCgrouped.get_group(st)
                r="MTC"

            else:
                group=CRMLgrouped.get_group(st)
                r="CRML"

            ctr=0
            ri=[]
            la=[]
            l=[]
            for i in range(len(group)) :
                
                if check(group.iloc[i].arrival_time):   
                    tm=group.iloc[i].arrival_time
                    ti=tm.split(":")
                    tm=datetime.time(int(ti[0])%24,int(ti[1]),int(ti[2]))
                    l.append([r+" "+str(group.iloc[i].route_long_name),tm])
                    ctr+=1
            l = sorted(l, key=lambda x: x[1])
            print("No of arrivals :"+str(ctr))
            for i in range(len(l)): 
                ri.append(l[i][0])
                la.append(l[i][1])
            print(ri)
            print(la)
            return render(request,'solution.html',{'data':zip(ri,la),'count':ctr})
            
        return render(request,'home.html',{})

# Create your views here.

def check(s):                                   #checks whether bus arrival time is within the next 30 minutes
    t1=datetime.datetime.now()
    t2=t1+datetime.timedelta(seconds=3600)
    t1=t1.time()
    t2=t2.time()
    s=s.split(":")
    s=list(map(int,s))
    s[0]=s[0]%24
    t=datetime.time(s[0],s[1],s[2])
    return t1<=t and t<=t2

def solution(request,st):
    with zipfile.ZipFile('MTC.zip', 'r') as file:                   #Extract zipfile and in data folder
        file.extractall('./data')
    stop = pd.read_csv('data/stop_times.txt', low_memory=False)     #find csv file in the path data/stop_times.txt and convert it to panda table. 
    stop_name=pd.read_csv('data/stops.txt', low_memory=False)       #I am only using stop_times.txt and stops.txt in the MTC zip file. So you need not use the zip file 
    arrival=pd.merge(stop,stop_name,on="stop_id")                   #Merge the 2 panda tables on the basis of common attribute stop_id
    st=input("Enter stop name: ")                                   #st is the stop name entered by user
    ctr=0
    for i in range(len(arrival)) :                                  
        if check(arrival.at[i,"arrival_time"]) and arrival.at[i,"stop_name"]==st:  #condition 1- check(entry arrival time in table) condition 2- table entry bus stop name == user entered bus stop name(st)   
            s=arrival.at[i,"trip_id"]
            s=s.split("_")
            print("route id: "+s[0]+" arrival time: "+arrival.at[i,"arrival_time"])
            ctr+=1
    return render(request,'solution.html',{})
