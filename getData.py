import sys
import csv


def get_tables(tables):

    tablesdata = {}
    for table in tables:
        tablesdata[table] = get_table_rows(table)

    return tablesdata

def get_table_rows(table):

    rows = []
    with open(table+".csv",'r') as csvfile:

        csvreader = csv.reader(csvfile)

        for row in csvreader:
            rows.append(row)

    return rows

def get__fields(tables):

    fields = {}
    for table in tables:
        fields[table] = get_table_fields(table)
    return fields

def get_table_fields(table):

    f = open("metadata.txt",'r')
    lines = f.readlines()
    lines = [line.rstrip("\r\n") for line in lines]
    
    ind = lines.index(table) + 1
    fields = []
    while(lines[ind] != "<end_table>"):
        fields.append(lines[ind])
        ind = ind + 1

    
    f.close()
    return fields

