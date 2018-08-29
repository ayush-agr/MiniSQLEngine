import sys,os,glob
from  getData import *
from table import *
from multColsTbs import *
import re

table_objects = {}
arrtbobj = []

def printInstruction():
    print("Please enter the query in right format and give proper spaces i.e, :")
    print("select [column(s) name(s) seperated by comma] from [table(s) name(s) seperated by comma] where [single join condition(optional) or condtion on columns]")

def processQuery(query):

    if('select' not in query):
        print("Invalid query")
        printInstruction()
        return

    if('from' not in query):
        print("Invalid query")
        printInstruction()
        return

    patr1 = query[query.index('select')+1 : query.index('from')]
    part2 = ''.join(patr1)
    #print(part2.split(','))

    try:
        part3 = query[query.index('from')+1 : query.index('where')]
    except:
        part3 = query[query.index('from')+1 :]

    part4 = ''.join(part3)
    #print(part4.split(','))

    quetemp = query
    query = ["select",part2,"from",part4]

    whr = 0
    andd = 0
    orr = 0
    conds = []


    if('where' in quetemp):
        whr = 1
        whrcond = quetemp[quetemp.index('where')+1:]
        whrcond=' '.join(whrcond)

        if('AND' in whrcond):
            whrcond = whrcond.split('AND')
            andd = 1
        elif('OR' in whrcond):
            whrcond = whrcond.split('OR')
            orr = 1
        else:
            whrcond = [whrcond]
        # print(whrcond)
        for k in whrcond: 
            conds.append(k.split())
    # print(conds)

    #print(query)

    ret = tableData(part4)
    if(ret == 0):
        print("Table/s don't exist")
        return

    clms = part2.split(',')
    dist = 0

    tempcols = ""
    for i in range(len(clms)):
        
        q1 = re.search('distinct(.*)',clms[i],re.IGNORECASE)
        
        if(q1 == None):
            tempcols = tempcols + clms[i] + ","
        else:
            dist = 1
            tempcols = tempcols + q1.group(1)[1:-1] + ","

    part2 = tempcols[:-1]
    #print(part2)


    #try:
    #return

    try:
        multColsMult(arrtbobj,part2,table_objects,dist,andd,orr,conds)
    except:

        if(whr == 1):
            print("Please enter valid where condition")
            printInstruction()

        else:
            try:

                if(len(query) == 4):
                    table = query[3]
                    obj = table_objects[table]

                    if(query[1] == "*" ):
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

                    elif(query[1] in obj.fields):
                        col = obj.cols[obj.fields.index(query[1])]
                        print(table+"."+query[1])
                        for i in col:
                            print(i)

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

            except:
                printInstruction()


def tableData(query):
    # try:
    #     tables = query[query.index('from')+1 : query.index('where')]
    # except:
    #     tables = query[query.index('from')+1 :]

    # temp = ' '.join(tables)
    tables = query.split(',')
    tables = [table.strip() for table in tables]

    files = []
    for f in glob.glob("*.csv"):
        files.append(f)


    for table in tables:
        if(table+".csv" not in files):
            return 0
        table_objects[table] = Table(table)
        arrtbobj.append(table_objects[table])


    return 1

que = sys.argv[1].split()
processQuery(que)


