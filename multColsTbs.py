from copy import deepcopy
import operator

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def printT(tab):
	n = len(tab)
	m = len(tab[0])

	for i in range(n):
		for j in range(m):

			if(j==m-1):
				print(str(tab[i][j]),end='')
			else:
				print(str(tab[i][j])+",",end='')
		print()

def joinTable(tab1,tab2):

	ans = []
	tmpt1 = deepcopy(tab1)
	tmpt2 = deepcopy(tab2)
	# print(tmpt1)
	# print(tmpt2)

	for i in range(len(tmpt1)):
		for j in range(len(tmpt2)):
			cpy = deepcopy(tmpt1[i])
			for k in range(len(tmpt2[j])):
				cpy.append(tmpt2[j][k])
			ans.append(cpy)

	# print(len(ans))
	return ans



def transpose(arr):
	n = len(arr)
	m = len(arr[0])
	ans = [[j for j in range(n)] for i in range(m)]
	
	for i in range(n):
		for j in range(m):
			ans[j][i] = arr[i][j]

	return ans

def buildTable(cols,tableNames):

	for i in tableNames:
		cols[i] = transpose(cols[i])

	# print(tableNames)

	# for i in tableNames:
	lentb = len(cols[tableNames[0]])


	notbs = len(tableNames)
	final = deepcopy(cols[tableNames[0]])
	
	# print(notbs)
	i = 1
	while i < notbs:
		# print(final)
		# print(cols[tableNames[i]])
		final = joinTable(final,cols[tableNames[i]])
		i = i+1

	return final

def solveCond(arr,x,y,op):

	ans = [0 for i in range(len(arr))]

	# print(x)
	for i in range(len(arr)):
		# print(arr[i][x])
		if(op(arr[i][x],y)):
			ans[i] = 1
	return ans

def solveCond2(arr,x,y,op):

	ans = [0 for i in range(len(arr))]

	# print(x)
	for i in range(len(arr)):
		# print(arr[i][x])
		if(op(arr[i][x],arr[i][y])):
			ans[i] = 1
	return ans


def multColsMult(tables,cols,arrdict,dist,andd,orr,conds):

	numtbs = len(tables)
	coltb = {}
	if(cols == '*'):
		cols = []
		for table in tables:
			cols.extend(table.fields)
	else:
		cols = cols.split(',')

	cols = set(cols)
	cols = list(cols)
	

	for col in cols:
		for table in tables:
			if(col in table.fields):
				try:
					coltb[table.name].append(col)
				except:
					coltb[table.name] = []
					coltb[table.name].append(col)

	sm = 0
	for table in tables:
		sm = sm + len(coltb[table.name])
	
	if(sm != len(cols)):
		print("Column/Table names are ambiguous")
		return

	columns = {}


	for i in coltb:
		
		tableobj = arrdict[i]
		arr=[]
		coltb[i].sort()

		for j in coltb[i]:
			arr.append(tableobj.cols[tableobj.fields.index(j)])
		
		columns[i]=arr

	tableNames = []

	ind = 0
	mpind = {}

	for i in coltb:
		tableNames.append(i)
		for j in coltb[i]:
			print(i+"."+j,end=',')
			mpind[j] = ind
			ind =  ind + 1
	
	print()


	final = buildTable(columns,tableNames)
	if(dist==1):
		unique_d = [list(x) for x in set(tuple(x) for x in final)]
		final = unique_d

	# print("here")
	if(len(conds) > 0):

		# print(conds)

		ops = { "=":operator.eq,">=":operator.ge,"<=":operator.le,">":operator.gt,"<":operator.lt}
		arr = [[] for i in range(len(conds))]
		x = [cond[0] for cond in conds]
		y = [cond[2] for cond in conds]
		op = [cond[1] for cond in conds]	
		op = [ops[ab] for ab in op]

		# print("here")
		for i in range(len(conds)):
			if(is_number(y[i])):
				arr[i] = solveCond(final,mpind[x[i]],int(y[i]),op[i])
			else:
				arr[i] = solveCond2(final,mpind[x[i]],mpind[y[i]],op[i])

		ans = arr[0]
		# print(ans)
		if(andd == 1 and len(conds) == 2):
			for i in range(len(arr[1])):
				ans[i] = ans[i] and arr[1][i]

		if(orr == 1 and len(conds) == 2):
			for i in range(len(arr[1])):
				ans[i] = ans[i] or arr[1][i]

		finalans = []
		for i in range(len(final)):
			if(ans[i]):
				finalans.append(final[i])
		final  = finalans


	if final == []:
		print("No such rows found")
		return
	# print("hi")
	printT(final)
	# print(columns)
	# print(coltb)