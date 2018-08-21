from getData import *

class Table():

    def __init__(self,name):

        self.name = name
        self.fields = get_table_fields(name)
        self.rows = get_table_rows(name)
        self.cols = []
        numcols = len(self.fields)
        numrows = len(self.rows)
        for col in range(numcols):
            arr = []
            for i in range(numrows):
                try:
                    arr.append(float(self.rows[i][col])) 
                except:
                    arr.append(self.rows[i][col]) 
            self.cols.append(arr)
            
    def get_sum(self,colname):

        if(type(colname) == str):
            ind = self.fields.index(colname)
        else:
            ind = colname
        col = self.cols[ind]
        ans = 0
        for i in range(len(col)):
            ans = ans + col[i]

        return ans

    def get_avg(self,colname):

        if(type(colname) == str):
            ind = self.fields.index(colname)
        else:
            ind = colname
        col = self.cols[ind]
        ans = 0
        for i in range(len(col)):
            ans = ans + col[i]

        return float(ans/len(col))

    def get_min(self,colname):

        if(type(colname) == str):
            ind = self.fields.index(colname)
        else:
            ind = colname
        col = self.cols[ind]
        ans = col[0]
        for i in range(len(col)):
            if(col[i] < ans):
                ans = col[i]

        return ans


    def get_max(self,colname):

        if(type(colname) == str):
            ind = self.fields.index(colname)
        else:
            ind = colname
        col = self.cols[ind]
        ans = col[0]
        for i in range(len(col)):
            if(col[i] > ans):
                ans = col[i]

        return ans
