# CREATE TABLE results_32 (
#     rollno varchar(10) PRIMARY KEY,
#     name varchar(30) NOT NULL,
#     `13508` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     `13510` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     `13534` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     `13537` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     `135AE` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     `135AF` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     `135AR` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     `135BM` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     `135CX` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
#     grade varchar(4) default NULL
#  )
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from collections import defaultdict

# rollnos = [input() for _  in range(72)]
# for rollno in rollnos:
#     print("'"+rollno+"'",end=',')

rollnos = ['17BD1A0541','17BD1A0542','17BD1A0543','17BD1A0544','17BD1A0545','17BD1A0546','17BD1A0547','17BD1A0548','17BD1A0549','17BD1A054A','17BD1A054B','17BD1A054C','17BD1A054D','17BD1A054E','17BD1A054F','17BD1A054G','17BD1A054H','17BD1A054J','17BD1A054K','17BD1A054L','17BD1A054M','17BD1A054N','17BD1A054P','17BD1A054Q','17BD1A054R','17BD1A054T','17BD1A054U','17BD1A054V','17BD1A054W','17BD1A054X','17BD1A054Y','17BD1A054Z','17BD1A0551','17BD1A0552','17BD1A0553','17BD1A0554','17BD1A0555','17BD1A0556','17BD1A0557','17BD1A0558','17BD1A0559','17BD1A055A','17BD1A055B','17BD1A055C','17BD1A055D','17BD1A055E','17BD1A055F','17BD1A055G','17BD1A055H','17BD1A055J','17BD1A055K','17BD1A055L','17BD1A055M','17BD1A055N','17BD1A055P','17BD1A055Q','17BD1A055R','17BD1A055T','17BD1A055U','17BD1A055V','18BD5A0525','18BD5A0526','18BD5A0527','18BD5A0528','18BD5A0529','18BD5A0530','18BD5A0531','18BD5A0532','18BD5A0533','18BD5A0534','18BD5A0535','18BD5A0536']

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='JNTUH',
                                         user='root',
                                         password='root')
except Error as e:
    print("Error while connecting to MySQL", e)
for rollno in rollnos:
    with requests.Session() as c:
        r = c.post("http://202.63.105.184/results/resultAction", headers = {"Host": "202.63.105.184","Content-Length": "87","Cache-Control": "max-age=0","Origin": "http://202.63.105.184","Upgrade-Insecure-Requests": "1","DNT": "1","Content-Type": "application/x-www-form-urlencoded","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://202.63.105.184/results/jsp/SearchResult.jsp?degree=btech&examCode=1387&etype=r16&type=grade16",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en-IN;q=0.9,en;q=0.8",
        "Cookie": "JSESSIONID=D94B28C0780051CCC8C6BB695203302D"},
        data = {"degree":"btech","examCode":"1387","etype":"r16","result":"null","grad":"null","type":"grade16","htno":rollno})
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll("table")
        rollno = tables[0].find("tr").findAll("td")[1].find("b").contents[0]
        name = tables[0].find("tr").findAll("td")[3].find("b").contents[0]
        rows = tables[1].findAll("tr")[1:]

        grade_dict = {"O":10,"A+":9,"A":8,"B+":7,"B":6,"C":5}
        credits_dict = {"13508":2,"13510":2,"13534":2,"13537":0,"135AE":4,"135AF":4,"135AR":3,"135BM":4,"135CX":3}
        d = defaultdict()
        grade = 0
        flag = 0
        credit_sum = 24
        for row in rows:
            columns = row.findAll('td')
            d[columns[0].find("b").contents[0]] = columns[2].find("b").contents[0]
            if columns[2].find("b").contents[0] == "F" or columns[2].find("b").contents[0] == "Ab":
                grade='null'
                flag=1
            if flag==0:
                grade+=grade_dict[columns[2].find("b").contents[0]]*credits_dict[columns[0].find("b").contents[0]]
        if grade!='null':
            grade = round(grade/credit_sum,2)

        if connection.is_connected():
            cursor = connection.cursor()
            query = "insert into results_32 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            val = (rollno,name,d['13508'],d['13510'],d['13534'],d['13537'],d['135AE'],d['135AF'],d['135AR'],d['135BM'],d['135CX'],grade)
            cursor.execute(query,val)
            print("success")
connection.commit()



# POST /results/resultAction HTTP/1.1
# Host: 202.63.105.184
# Content-Length: 87
# Cache-Control: max-age=0
# Origin: http://202.63.105.184
# Upgrade-Insecure-Requests: 1
# DNT: 1
# Content-Type: application/x-www-form-urlencoded
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# Referer: http://202.63.105.184/results/jsp/SearchResult.jsp?degree=btech&examCode=1387&etype=r16&type=grade16
# Accept-Encoding: gzip, deflate
# Accept-Language: en-US,en-IN;q=0.9,en;q=0.8
# Cookie: JSESSIONID=0DD55E1833C6832B795BB80C4212282E
# Connection: close
#
# degree=btech&examCode=1387&etype=r16&result=null&grad=null&type=grade16&htno=17BD1A0525
