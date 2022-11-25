import mysql.connector
from mysql.connector import pooling 
from mysql.connector import connect


dbconfig = {
  "database": "test",
  "user":     "joe",
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 3,
                                                      **dbconfig)

cnxpool.add_connection(cnx = None)
cnxpool.add_connection(cnx = None)

cnx = cnxpool.get_connection()


cursor = conn.cursor(buffered =True)
query = "SELECT DISTINCT category FROM Attraction;"
cursor.execute(query)
catList = cursor.fetchall()
   
finalList = []
for i in range((len(catList))):
    finalList.append(catList[i][0])
    
print(catList)
print(finalList)