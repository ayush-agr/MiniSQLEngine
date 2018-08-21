import sys
from  getData import *
from table import *
import re

table_objects = {}

def processQuery(query):

    ret = tableData(query)
    if(ret == 0):
        print("tables don't exist")
        return

    if(len(query) == 4):
        table = query[3]
        obj = table_objects[table]

        if(query[1] == "*"):
            rows = obj.rows
            fields = obj.fields
            num = len(fields)

            for i in range(num):
                if(i == num-1):
                    print(table+"."+fields[i])
                else:
                    print(table+"."+fields[i]+',',end='')

            for row in range(len(rows)):
                for i in range(num):
                    if(i == num-1):
                        print(rows[row][i])
                    else:
                        print(rows[row][i]+',',end='')
        else:
            table = query[3]
            obj = table_objects[table]
            fields = obj.fields

            qval = -1

            q1 = re.search('sum(.*)',query[1],re.IGNORECASE)
            qval = 1

            if(q1 == None):
                q1 = re.search('avg(.*)',query[1],re.IGNORECASE)
                qval = 2

            if(q1 == None):
                q1 = re.search('average(.*)',query[1],re.IGNORECASE)
                qval = 2

            if(q1 == None):
                q1 = re.search('max(.*)',query[1],re.IGNORECASE)
                qval = 3

            if(q1 == None):
                q1 = re.search('min(.*)',query[1],re.IGNORECASE)
                qval = 4

            if(q1 == None):
                print("No such column exist in the table")
                return

            col = q1.group(1)[1:-1]
            if(col not in fields):
                print("No such column exist in the table")
                return

            ans = 0.0

            if(qval == 1):
                ans = obj.get_sum(col)
            elif(qval == 2):
                ans = obj.get_avg(col)
            elif(qval == 3):
                ans = obj.get_max(col)
            elif(qval == 4):
                ans = obj.get_min(col)

            print(ans)

    else:
        pass


def tableData(query):
    try:
        tables = query[query.index('from')+1 : query.index('where')]
    except:
        tables = query[query.index('from')+1 :]

    temp = ' '.join(tables)
    tables = temp.split(',')
    tables = [table.strip() for table in tables]

    if('table1' not in tables and 'table2' not in tables):
        return 0

    for table in tables:
        table_objects[table] = Table(table)


    return 1

que = sys.argv[1].split()
processQuery(que)
