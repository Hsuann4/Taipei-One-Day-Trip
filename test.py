import mysql.connector
from mysql.connector import pooling 
from mysql.connector import connect





conn = mysql.connector.connect(
    user='root', password='Dennis860404_', database='Taipei_API'
)
conn.reconnect(attempts=1,delay=0)
cursor = conn.cursor()


cursor = conn.cursor(buffered=True)
query = "SELECT DISTINCT category FROM Attraction;"
cursor.execute(query)
catList = cursor.fetchall()

finalList = []
for i in range(len(catList)):
    finalList.append(catList[i][0])
    
print(finalList)
