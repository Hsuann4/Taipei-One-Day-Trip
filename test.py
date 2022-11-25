import mysql.connector
from mysql.connector import pooling 
from mysql.connector import connect





conn = mysql.connector.connect(
    user='root', password='Dennis860404_', database='Taipei_API'
)
conn.reconnect(attempts=1,delay=0)
cursor = conn.cursor()


    
    #網址抓值
inputCondition_page = request.args.get("page")
inputCondition_keyword = request.args.get("keyword")
pageInput = 2
keywordInput ='台北'


if  inputCondition_page is not None and inputCondition_keyword is None:
        #處理未篩選頁碼
            
            cursor = conn.cursor(buffered =True)
            # cursor = conn.cursor(buffered= True)
           
            pageCountquery = "SELECT ceil(count(*)/12) AS pageTotal FROM  Attraction;"
            cursor.execute(pageCountquery)
            pageTotal = cursor.fetchall()
            pageTotal1 = pageTotal[0][0]
            conn.commit()
            # cursor.close()
            # cnx1.close()
            
            if pageInput + 1 < pageTotal1:
                nextpage = pageInput + 1
            elif pageInput + 1 >= pageTotal1:
                nextpage = None

            #處理未篩選內容
            cursor = conn.cursor(buffered =True)
            page1query = "SELECT * FROM Attraction ORDER BY attid LIMIT %s , 12;"
            pageInfo = ((str((pageInput)*12)),)
            print('this is query',page1query, pageInfo)
            cursor.execute(page1query, pageInfo)
            p1result = cursor.fetchall()
            conn.commit()
            # cursor.close()
            

            #處理未篩選圖片連結
            listtest = []
            for i in range(len(p1result)):
                    imageRawlist = p1result[i][10]
                    listtest.append(imageRawlist)
            
            #處理未篩選欄位值
            pageResultlist = []
            for i in range(len(p1result)):
                    imagesplit = listtest[i].split("http")
                    imagesplit = ["http" + img for img in imagesplit]
                    finalList = imagesplit[1:]

                    singleResult = {"id": p1result[i][1],
                                    "name": p1result[i][2],
                                    "category": p1result[i][3],
                                    "description": p1result[i][4],
                                    "address": p1result[i][5],
                                    "transport": p1result[i][6],
                                    "mrt": p1result[i][7],
                                    "lat": p1result[i][8],
                                    "lng": p1result[i][9],
                                    "images": finalList
                                    }
                    pageResultlist.append(singleResult)

            # conn.commit()
           

            return jsonify({"nextpage": nextpage,
                        "data": pageResultlist
            })
        
        
    
    
        elif inputCondition_page is not None and inputCondition_keyword is not None: 
            #下面是有篩選的
        

            #處理篩選資料後的頁碼
            cursor = conn.cursor(buffered =True)
            # cursor = cnx.get_connection()
            pageCountquery = "SELECT ceil(count(*)/12) FROM Attraction WHERE category LIKE %s OR REGEXP_LIKE(name, %s);"
            criteria = (keywordInput,keywordInput)
            cursor.execute(pageCountquery, criteria)
            pageTotal = cursor.fetchall()
            conn.commit()
            # cursor.close()
           
            
            finalPagenumber = pageTotal[0][0] 
            if pageInput + 1 < finalPagenumber:
                nextpage = pageInput + 1
            elif pageInput + 1 >= finalPagenumber:
                nextpage = None
            
            
            #處理篩選資料後的內容
            cursor = conn.cursor(buffered =True)
            # cursor = cnx.get_connection()
            keywordResultquery = "SELECT * FROM Attraction WHERE category LIKE %s OR REGEXP_LIKE(name, %s) LIMIT %s, 12 ;"
            criteria = (keywordInput, keywordInput,((pageInput)*12))
            cursor.execute(keywordResultquery,criteria)
            keywordResult = cursor.fetchall()
            conn.commit()
            # cursor.close()
           
            
            #處理篩選資料後的圖面網址
            listtest = []
            for i in range(len(keywordResult)):
                    imageRawlist = keywordResult[i][10]
                    listtest.append(imageRawlist)




            #處理篩選後的欄位值
            pageResultlist = []
            for i in range(len(keywordResult)):
                    imagesplit = listtest[i].split("http")
                    imagesplit = ["http" + img for img in imagesplit]
                    finalList = imagesplit[1:]

                    singleResult = {"id": keywordResult[i][1],
                                    "name": keywordResult[i][2],
                                    "category": keywordResult[i][3],
                                    "description": keywordResult[i][4],
                                    "address": keywordResult[i][5],
                                    "transport": keywordResult[i][6],
                                    "mrt": keywordResult[i][7],
                                    "lat": keywordResult[i][8],
                                    "lng": keywordResult[i][9],
                                    "images": finalList
                                    }
                    pageResultlist.append(singleResult)

            

            return jsonify({"nextpage": nextpage,
                            "data": pageResultlist
            })
    
   