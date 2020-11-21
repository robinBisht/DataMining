# for nominal values

def dissimilar_nominal(row):
	nom = []
	n = len(row)
	for i in range(1,n):
		li = []
		for j in range(i):
			if(row[i] == row[j]):
				li.append(0)
			else:
				li.append(1)
		nom.append(li)

	return nom

# for assymetric binary values
def dissimilar_asymmetric(row):
	assymetric = []
	n = len(row)
	for i in range(1,n):
		li = []
		for j in range(i):
			if(row[i] == row[j] and row[i] == 1 ):
				li.append(0)
			elif (row[i] == row[j] and row[i] == 0) :
				li.append(-1)
			else:
				li.append(1)
		assymetric.append(li)

	return assymetric

# for ordinal values
# ranks = { 'high':1,'mid':2,'low':3 }
def dissimilar_ordinal(row,ranks):
	ordinal = []

	for i in row:
		ordinal.append(ranks[i])


	ordinal_normal = []
	n = len(ranks)
	M = float(n-1)	
	for i in ordinal:
		ordinal_normal.append( (i-1)/M )

	return dissimilar_numeric(ordinal_normal)

# for numeric values
# using manhattan distance
def dissimilar_numeric(row):
	numeric = []
	ma = max(row)
	mi = min(row)
	diff = float( ma-mi )
	n = len(row)
	for i in range(1,n):
		li = []
		for j in range(i):
			li.append( round( abs( row[i]- row[j] ) / diff , 2) )
		numeric.append(li)

	return numeric

# combining all

# type = {'t1':'nominal'}
# attributes = {'t1':[],'t2':[]}

def dissimilar_matrix(attributes,type_of):
	init_matrix = []

	for attr,lis in attributes.items():
		if type_of[attr] == 'nominal' or type_of[attr] == 'symmmetric_binary' :
			init_matrix.append( dissimilar_nominal(lis) )
		elif type_of[attr] == 'assymetric_binary':
			init_matrix.append( dissimilar_asymmetric(lis) )
		elif type_of[attr] == 'ordinal':
			init_matrix.append( dissimilar_ordinal(lis[0:-1],lis[-1]) )
		elif type_of[attr] == 'numeric':
			init_matrix.append( dissimilar_numeric(lis) )

	#		t1				t2			t3
	# [ [[], [], [] ] ,[ [],[],[] ], [[],[],[]] ]
	final_matrix = []

	l = len(attributes)
	
	for i in range(0,l-1):
		li = []
		for j in range(0,i+1):
			
			dist = 0
			n = l
			for att in init_matrix:
				
				if( att[i][j] == -1 ):
					n= n-1
				else:
					dist  = dist+att[i][j]
			li.append( round(dist/float(n),2) )
		final_matrix.append(li)

	return final_matrix

# main function
if __name__ == '__main__':

	t1 = ['white','brown','black','black']
	t2 = ['small','medium','small','large', {'large':3,'small':1,'medium':2}  ]
	t3 = ['1','0','1','0']
	t4 = [65,60,65,70]
	
	attributes = {'test1':t1,'test2':t2,'test3':t3,'test4':t4}
	type_of = {'test1':'nominal','test2':'ordinal','test3':'assymetric_binary','test4':'numeric'}

	# attr = {1:'nominal',2:'assymetric_binary',3:'symmmetric_binary',4:'numeric',5:'ordinal'}
	# attributes = {}
	# type_of = {}
	# n = int(input("Number of: attributes: "))
	# r = int(input("Number of rows: "))
	# print()
	# l =[]
	# for i in range(n):
	# 	li = []
	# 	val = int(input("Enter 1 for nominal; 2 for assymetric binary; 3 for symmmetric binary; 4 for numeric and 5 for ordinal "))
	# 	name = input("Enter name of attribute: ")
	# 	print()
	# 	type_of[name] = attr[val]
	# 	for x in range(r):
	# 		li.append( input("Enter value for row {}: ".format(x+1)) )
	# 	if val == 4:
	# 		li = [int(a) for a in li]
	# 	elif val == 5:
	# 		new_li = {}
	# 		se = set(li)
	# 		for j in se:
	# 			rnk = int(input("Provide rank of {}: ".format(j)))
	# 			new_li[j] = rnk
	# 		li.append(new_li)
	# 	elif val == 2:
	# 		se = set(li)
	# 		for i in se:
	# 			x = int(input("0/1 for {}: ".format(i) ))
	# 			li = [ x for i in li ]
	# 	attributes[name] = li
	# 	print()

	# # for i in 


	matr = dissimilar_matrix(attributes,type_of)
	for i in matr:
		print(i)