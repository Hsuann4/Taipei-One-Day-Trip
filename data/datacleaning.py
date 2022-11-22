import json
import re
import os
import mysql.connector

conn = mysql.connector.connect(
    user='root', password='Dennis860404_', database='Taipei_API'
)


src = "/Users/tingyuhsu/Desktop/Wehelp Bootcamp/Period 2/taipei-day-trip/data/taipei-attractions.json"

data = open(src, "r")
interpretdata = json.load(data)
datalist = interpretdata["result"]["results"] #讀入資料


FinalList = []
for i in datalist:
   
    RawList = i["file"].split("http")
    FilteredList = ["http" + name for name in RawList if name.lower().endswith((".jpg",".png"))]
    FinalList.append(f'{i["_id"]}, {i["name"]}, {i["CAT"]}, {i["description"]}, {i["address"]}, {i["direction"]}, {i["MRT"]}, {i["latitude"]}, {i["longitude"]}, {FilteredList}')
    x = ''.join(FilteredList)   
    

    cursor = conn.cursor(buffered = True)
    query = 'INSERT INTO  Attraction (attid, name, category, description, address, transport, mrt, lat,lng, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'
    
    content =(i["_id"], i["name"], i["CAT"], i["description"], i["address"], i["direction"], i["MRT"], i["latitude"], i["longitude"], x )
    # print(content)


    # contentforwrite = (f'{i["_id"]}, {i["name"]}, {i["CAT"]}, {i["description"]}, {i["address"]}, {i["direction"]}, {i["MRT"]}, {i["latitude"]}, {i["longitude"]}, {x}')
    # with open("data.csv","a",encoding="utf-8") as file:
    #     file.write()

    cursor.execute(query, content)
    conn.commit()


# print(FinalList)
# cursor = conn.cursor(buffered = True)
   
# query = "INSERT INTO  Attraction att_id, name, category, description, address, transport, mer, lat,lng, images  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


       

    

    



