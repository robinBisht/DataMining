import itertools
import math
from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    s.sort()
    li = list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
    return li[1:len(li)-1]

def Apriori(df, min_support):
	supp = min_support
	C = []
	L = []
	store = {}
	for column in df:
		sup_cnt = sum(df[column])
		C.append([[column],sup_cnt])
		if sup_cnt >= supp:
			L.append([[column], sup_cnt])
	dfC = pd.DataFrame(C, columns = ['Itemset', 'Support Count'])
	dfL = pd.DataFrame(L, columns = ['Itemset', 'Support Count'])
	print(dfC)
	print()
	print(dfL)
	print("*"*40)
	for i in L:
		store[tuple(i[0])] = i[1]		
	k = len(df.columns)
	A = []
	B = []
	Pr = C.sort(key = lambda x: x[1])
	
	for index in range(2, k):
		C_index = []
		L_index = []
		for i in range(len(L)-1):
			for j in range(i+1,len(L)):
				li = L[i][0] + L[j][0]
				li = list(dict.fromkeys(li))
				li.sort()
				indices = list(range(0, len(df.index)))
				for item in li:
					indices1 = [ii for ii, x in enumerate(df[item]) if x]
					indices = list(set(indices) & set(indices1))
				sup_cnt = len(indices)
				if(len(li) == index):
					C_index.append([li, sup_cnt])
				if(sup_cnt >= supp and len(li) == index):
					L_index.append([li,sup_cnt])
		L = L_index
		if( len(L_index) == 0 ):
			break
		C_index.sort()
		L_index.sort()
		C_index = list(C_index for C_index,_ in itertools.groupby(C_index))
		L_index = list(L_index for L_index,_ in itertools.groupby(L_index))
		dfC = pd.DataFrame(C_index, columns = ['Itemset', 'Support Count'])
		dfL = pd.DataFrame(L_index, columns = ['Itemset', 'Support Count'])
		print(dfC)
		print()
		print(dfL)
		print("*"*40)
		A = L_index
		B = C_index
		for i in A:
			store[tuple(i[0])] = i[1]

	l = A[0][1]
	sett = set(A[0][0])  # { 1, 2 ,3 }
	st = set(powerset(sett))
	for i in st:
		a = set(i) #  { 1 , 2} => a-i = {3}
		n = l/float(store[i])
		n = n*100
		print("{} => {} :  confidence: {}% ".format( a ,sett-a , n ))
	# print(store)

import pandas as pd

from mlxtend.preprocessing import TransactionEncoder

dataset = [['Apple', 'Egg', 'Bread', 'Butter', 'Milk', 'Orange'],
           ['Cheese', 'Egg', 'Bread', 'Butter', 'Milk', 'Orange'],
           ['Apple', 'Butter', 'Orange', 'Milk'],
           ['Banana', 'Grapes', 'Kiwi', 'Mango', 'Melon'],
           ['Grapes', 'Guava', 'Mango', 'Orange', 'Pear']]

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)

Apriori(df, 3)