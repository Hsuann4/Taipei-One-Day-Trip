
import mysql.connector
import json
from flask import *
from flask import request
from flask import jsonify
from flask_cors import CORS




conn = mysql.connector.connect(
    user='root', password='Dennis860404_', database='Taipei_API'
)
conn.reconnect(attempts=1, delay=0)

app=Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False



# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")





#API


@app.route("/api/attractions") #第一隻api
def pageAndfilter():
    
        #網址抓值
        inputCondition_page = request.args.get("page")
        inputCondition_keyword = request.args.get("keyword")
        pageInput = int(request.args.get("page")) 
        keywordInput = str(request.args.get("keyword"))


        if  inputCondition_page is not None and inputCondition_keyword is None:
            #處理未篩選頁碼
            cursor = conn.cursor(buffered=True)
            pageCountquery = "SELECT ceil(count(*)/12) AS pageTotal FROM  Attraction;"
            cursor.execute(pageCountquery)
            pageTotal = cursor.fetchall()
            pageTotal1 = pageTotal[0][0]
            
            if pageInput + 1 < pageTotal1:
                nextpage = pageInput + 1
            elif pageInput + 1 >= pageTotal1:
                nextpage = None

            #處理未篩選內容
            page1query = "SELECT * FROM Attraction ORDER BY attid LIMIT %s , 12;"
            pageInfo = (str(((pageInput))*12),)
            cursor.execute(page1query, pageInfo)
            p1result = cursor.fetchall()

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

            conn.commit()

            return jsonify({"nextpage": nextpage,
                        "data": pageResultlist
            })
        
        
    
    
        elif inputCondition_page is not None and inputCondition_keyword is not None: 
            #下面是有篩選的
        

            #處理篩選資料後的頁碼
            cursor = conn.cursor(buffered=True)
            pageCountquery = "SELECT ceil(count(*)/12) FROM Attraction WHERE category LIKE %s OR REGEXP_LIKE(name, %s);"
            criteria = (keywordInput,keywordInput)
            cursor.execute(pageCountquery, criteria)
            pageTotal = cursor.fetchall()
            finalPagenumber = pageTotal[0][0] 
            if pageInput + 1 < finalPagenumber:
                nextpage = pageInput + 1
            elif pageInput + 1 >= finalPagenumber:
                nextpage = None
                
            #處理篩選資料後的內容
            keywordResultquery = "SELECT * FROM Attraction WHERE category LIKE %s OR REGEXP_LIKE(name, %s) LIMIT %s, 12 ;"
            criteria = (keywordInput, keywordInput,((pageInput)*12))
            cursor.execute(keywordResultquery,criteria)
            keywordResult = cursor.fetchall()
            
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

            conn.commit()

            return jsonify({"nextpage": nextpage,
                            "data": pageResultlist
            })
                



@app.route("/api/attraction/<attractionId>") #第二隻api
def findbyattid(attractionId):
    index = attractionId
    cursor = conn.cursor(buffered=True)
    
    errorcheckQuery = "SELECT attid FROM Attraction;"
    cursor.execute(errorcheckQuery)
    checkRawlist = cursor.fetchall()
    
    checklist =[]
    for i in range(len(checkRawlist)):
        checklist.append(checkRawlist[i][0])
    
    
    if int(index) in checklist:
    
        query = "SELECT *  FROM Attraction WHERE attid = %s;"
        criteria = (index, )
        cursor.execute(query, criteria)
        resultList = cursor.fetchall()
        imageRawlist = resultList[0][10]
        imagesplit = imageRawlist.split("http")
        imagesplit = ["http" + img for img in imagesplit]
        finalList = imagesplit[1:]
        # print(finalList)

        finalResult = {"id":resultList[0][1],
                    "name":resultList[0][2],
                    "category":resultList[0][3],
                    "description":resultList[0][4],
                    "address": resultList[0][5],
                    "transport":resultList[0][6],
                    "mrt":resultList[0][7],
                    "lat":resultList[0][8],
                    "lng":resultList[0][9],
                    "images": finalList
        }
    
        return jsonify({"data": finalResult })
    
    
    elif int(index) not in checklist:
        return jsonify({"error": True,
                       "message": "景點編號錯誤"})
    
    else:
        return jsonify({"error": True,
                        "message":"伺服器錯誤"})



@app.route("/api/categories") #第三隻api
def findCat():
	
	cursor = conn.cursor(buffered=True)
	query = "SELECT DISTINCT category FROM Attraction;"
	cursor.execute(query)
	catList = cursor.fetchall()
	
	finalList = []
	for i in range(len(catList)):
		finalList.append(catList[i][0])
	
	
	return jsonify({"data":finalList})


#error handler 500 錯誤
@app.errorhandler(500)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
            "error": True,
            "message": "錯誤"
    })
    response.content_type = "application/json"
    
    return response

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=3000, debug = True)