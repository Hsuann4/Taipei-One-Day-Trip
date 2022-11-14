import json
import re
import os
import mysql.connector

src = "/Users/tingyuhsu/Desktop/Wehelp Bootcamp/Period 2/taipei-day-trip/data/taipei-attractions.json"

data = open(src, "r")
middle = json.load(data)
clist = middle["result"]["results"] #讀入資料


emptylist = []
for i in clist:
   
    RawList = i["file"].split("http")

    FilteredList = [name for name in RawList if name.lower().endswith((".jpg",".png"))]
    
 

    print(FilteredList)
    


    

    
# for j in range(len(FilteredList)):
#     FilteredList = "http" + FilteredList[j]

#     print(FilteredList)
    



     # print(str(i["_id"])+","+i["name"]+ ","+ i["CAT"]+"," +i["description"]+","+ i["address"]+","+ i["direction"]+","+ i["MRT"]+","+i["latitude"]+ i["longitude"]+","+i["file"] + "\n")
    



    
       

    

    



