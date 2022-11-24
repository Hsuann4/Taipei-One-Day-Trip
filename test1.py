import mysql.connector

conn = mysql.connector.connect(
    user='root', password='Dennis860404_', database='Taipei_API')

cursor = conn.cursor(buffered=True)

errorcheckQuery = "SELECT attid FROM Attraction;"
cursor.execute(errorcheckQuery)
checklist = cursor.fetchall()
print(checklist)

newlist =[]
for i in range(len(checklist)):
    newlist.append(checklist[i][0])
print(newlist)




x = 58
if x in newlist:
    print("yes")
else:
    print("damn")
	
conn.commit()
