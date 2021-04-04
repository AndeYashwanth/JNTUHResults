import requests
import sys
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from collections import defaultdict
from dotenv import load_dotenv
import os
load_dotenv()

######################################################################
rollnos = ['17BD1A0000', '17BD1A0001'] # Enter rollno's here
######################################################################

servers = ['http://202.63.105.184/results/resultAction',
           'http://results.jntuh.ac.in/resultAction']

optional_result_url_params = ['result', 'grad', 'type']
all_result_url_params = ['degree', 'examCode',
                         'etype', 'result', 'grad', 'type']
# servers_up = []  # will be appnded after checking server status
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
RESULT_URL = os.environ.get("RESULT_URL")

try:
    connection = mysql.connector.connect(host=DB_HOST,
                                         database=DB_NAME,
                                         user=DB_USER,
                                         password=DB_PASS,
                                         autocommit=True)
    cursor = connection.cursor(dictionary=True)
except Error as e:
    sys.exit("Error while connecting to MySQL", e)


def extract_query_params_from_url(url):
    query = requests.utils.urlparse(url).query
    params = dict(x.split('=') for x in query.split('&'))
    return params


result_url_params = extract_query_params_from_url(RESULT_URL)  # result is dict


def validate_url_params():
    for param in all_result_url_params:
        if param not in result_url_params.keys():
            if param in optional_result_url_params:
                result_url_params[param] = 'null'
            else:
                sys.exit("Missing param '" + param + "' in url")


validate_url_params()
exam_code = result_url_params['examCode']
table_name = exam_code
is_table_exists = False

# def is_server_up(url):
#     status_code = requests.get(url, timeout=3).status_code
#     if status_code == 200:
#         return True
#     return False

# for server in servers:
#     if is_server_up(server):
#         servers_up.append(server)


def create_results_table(subject_codes, cursor):
    repeat = "` ENUM ('O','A+','A','B+','B','C','F') NOT NULL, `"
    query = "create table IF NOT EXISTS `" + table_name + "` ( \
        `rollno` varchar(10) PRIMARY KEY, \
        `name` varchar(40) NOT NULL, `" \
        + f"{repeat.join(subject_codes)}{repeat}"\
        + "grade` varchar(4) default NULL);"
    cursor.execute(query)


def create_subject_name_table(cursor):
    cursor.execute("create table if not exists `subject_names` ( \
        `exam_code` varchar(4) NOT NULL, \
        `subject_code` varchar(5) NOT NULL, \
        `subject_name` varchar(100)); ")


def insert_subject_table(dict1, cursor):
    # get subject names already in db
    cursor.execute(
        f"select * from `subject_names` where `exam_code`={exam_code};")
    subject_codes = [row['subject_code'] for row in cursor.fetchall()]
    dict2 = defaultdict()

    for key, value in dict1.items():  # to only insert rows that are not present
        if key not in subject_codes:
            dict2[key] = value

    for subject_code, subject_name in dict2.items():
        sql = f"insert into `subject_names` (`exam_code`, `subject_code`, `subject_name`) values ('{exam_code}', '{subject_code}', '{subject_name}');"
        cursor.execute(sql)


for rollno in rollnos:
    with requests.Session() as c:
        credit_sum = 0
        result_url_params['htno'] = rollno
        r = c.post("http://202.63.105.184/results/resultAction",
                   data=result_url_params)

        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll("table")

        if tables == []:
            print(rollno + " is invalid or some error has occured")
            continue
        table1 = tables[0]
        rollno = str(table1.find("tr").findAll("td")[1].find("b").contents[0])
        name = str(table1.find("tr").findAll("td")[3].find("b").contents[0])

        table2 = tables[1].findAll("tr")
        table2_column_names = [
            content.text for content in table2[0].findAll('b')]
        grade_index = table2_column_names.index("GRADE")
        subject_name_index = table2_column_names.index("SUBJECT NAME")
        subject_code_index = table2_column_names.index("SUBJECT CODE")
        subject_credits_index = table2_column_names.index("CREDITS(C)")
        table2_rows = table2[1:]

        grade_dict = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5}
        d = defaultdict()
        sub_name_dict = defaultdict()
        grade = 0

        for row in table2_rows:
            columns = row.findAll('td')
            subject_code = str(
                columns[subject_code_index].find("b").contents[0])
            subject_name = str(
                columns[subject_name_index].find("b").contents[0])
            subject_grade = str(columns[grade_index].find("b").contents[0])
            subject_credits = int(
                columns[subject_credits_index].find("b").contents[0])
            credit_sum += subject_credits
            d[subject_code] = subject_grade
            sub_name_dict[subject_code] = subject_name

            if subject_grade == "F" or subject_grade == "Ab":
                grade = 'null'
                break
            else:
                grade += grade_dict[subject_grade] * subject_credits

        if grade != 'null':
            grade = round(grade/credit_sum, 2)

        if connection.is_connected():
            # create table if not exists
            if not is_table_exists:
                create_results_table(d.keys(), cursor)
                create_subject_name_table(cursor)
                insert_subject_table(sub_name_dict, cursor)
                is_table_exists = True

            placeholders = ', '.join(['%s'] * (len(d) + 3))
            columns = "`rollno`, `name`, `" + \
                '`, `'.join(d.keys()) + "`, `grade"
            sql = "INSERT INTO `{table}` ( {columns}` ) VALUES ( {values} );".format(
                table=table_name, columns=columns, values=placeholders)
            cursor.execute(sql, [rollno, name] + list(d.values()) + [grade])
            print(rollno)
        else:
            sys.exit("Disconnected")


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
