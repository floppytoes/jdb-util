# jdbview.py 
# Jeremy Bloom
# this only supports some object types - NOT bulletproof

import numpy as np 
import pandas as pd
import time
import datetime


def getindent(depth = 0, cols=3):
	if depth > 0:
		s = " " * cols * depth
		#print(">{:s}<".format(s))
		return s
	else:
		return ""


def jview_helper_recurse(x):   # returns True if should recurse, False if it shouldn't
	#print("type(x):", type(x), x)

	#if hasattr(x, '__iter__'):
	#	return True



	if isinstance(x, str):
		return False
	try:
	    iterator = iter(x)
	except TypeError:
		return False
	else:
		# python 276 will see (some?) unicode as iterable, so also check with hasattr
		if not hasattr(x, '__iter__'):
			return False

		return True  # careful, might iterable but better printed like  str


def jview(x, depth = 0):
	# avoiding using end='' to help python 276 work
	assert(depth < 20)
	# in py276 list comes off as unicode someting
	#print("type(x):", type(x), x)

	if ((isinstance(x,str)) or (jview_helper_recurse(x) == False)):  # only recurse on iterable non-strings
		# try to format type better
		#print("{:s}{:}".format(getindent(depth), x), end="")
		s = "{:s}{:}".format(getindent(depth), x)
		col_to_show_type = 30
		spaces_needed = max(col_to_show_type - depth - len(str(x)), 0)
		while spaces_needed > 0:
			#print(" ",end="")
			s += " "
			spaces_needed -= 1
		print(s + str(type(x)))


	elif (isinstance(x,pd.core.frame.DataFrame)):
		print("{:s}<pandas.core.frame.DataFrame with {:d} rows and {:d} cols>".format(getindent(depth), x.shape[0],x.shape[1]))
	elif (isinstance(x,np.ndarray)):
		print("{:s}<numpy.ndarray with dimensions {:s}>".format(getindent(depth), str(x.shape)))

	else:
		#print("type(x):", type(x), x)



		if isinstance(x, dict):   # print keys and values
			print("{:s}{{".format(getindent(depth)))
			for k in x:
				if jview_helper_recurse(x[k]):
					print("{:s}{:}: ".format(getindent(depth+1), repr(k)))
					jview(x[k], depth+2)
				else:  # further recursion not needed
					print("{:s}{:}: {:}".format(getindent(depth+1), repr(k), repr(x[k])))
			print("{:s}}}".format(getindent(depth)))
		else:  	# no keys 
			print("{:s}[".format(getindent(depth)))
			#print("----", type(x), x)
			for i in x:
				jview(i, depth + 1)
			print("{:s}]".format(getindent(depth)))


def tests():

	print("Starting tests()")
	T1 = [34, "alpha", 19, 34.332]
	T2 = {"bacon" : "is loved", 34 : "friday", "34" : True}
	T3 = 237.12
	T4 = [T1, T2, T3]

	data = [['Alex',10],['Bob',12],['Clarke',13]]
	T5 = pd.DataFrame(data,columns=['Name','Age'])
	T6 = {"vac": T5, 42: T1}
	T7 = np.arange(10)
	T8 = np.arange(15).reshape(3,5) 
	T9 = np.arange(30).reshape(3,5,2) 
	T10 = [T7, T2, T4, T5, T9]
	T11 = time.time()
	T12 = datetime.datetime.now()
	T13 = ["23", 19, T12, T11]
	T14 = []
	T15 = [T7, T2, T4, T5, T11, T12, T9]
	tests = [T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15]




	for i in range(len(tests)):
		print("test {:2d}".format(i+1))
		#print("--test {:2d} input>>>".format(i + 1), end="")
		#print(str(tests[i]) + "<<<")
		jview(tests[i])

	print("Ending tests()")




#tests()

