# jdbjsonextender.py 
# Jeremy Bloom
# this only supports some object types - NOT bulletproof

import json
import numpy as np 
import pandas as pd 
from  jdbview import jview
# extend JSON Encoder and Decoder to accomodate pandas dataframes and (multi-dim) ndarrays
# needs more testing but so far so good

PANDAS_DATAFRAME_SPECIAL_TYPE = "special.pandas.dataframe"
NUMPY_NDARRAY_SPECIAL_TYPE = "special.numpy.ndarray"

class JSONUpdatedEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, pd.core.frame.DataFrame):
			return {
				"_type": PANDAS_DATAFRAME_SPECIAL_TYPE,
				"value": obj.to_json() # a pandas call
			}
		elif isinstance(obj, np.ndarray):
			return {
				"_type": NUMPY_NDARRAY_SPECIAL_TYPE,
				"dims": obj.shape,
				#"value": json.JSONEncoder.default(self, obj.tolist())
				"value": json.dumps(obj.tolist())
				#"value": obj.tolist
			}


		else:
			return json.JSONEncoder.default(self, obj)


class JSONUpdatedDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

	def object_hook(self, obj):
		if '_type' not in obj:
			return obj
		elif obj['_type'] == PANDAS_DATAFRAME_SPECIAL_TYPE:
			return pd.read_json(obj["value"])
		elif obj['_type'] == NUMPY_NDARRAY_SPECIAL_TYPE:
			tmpList = json.loads(obj["value"])
			return np.array(tmpList).reshape(obj["dims"])
		else:		# has _type but not recognized 
			return obj


def tests():
	import jdbview


	print("Test 1...")


	print("MISC TESTING")

	data = [['Alex',10],['Bob',12],['Clarke',13]]
	tdf = pd.DataFrame(data,columns=['Name','Age'])


	tlist = ["27", 27, "Alpha", False, True, 3.1415926]
	tdict = {"zoo": 27, "frank": False}
	tm1 = np.arange(10)
	tm2 = np.arange(15).reshape(3,5) 
	tm3 = np.arange(30).reshape(3,5,2) 


	z1 = json.dumps(tm1, cls=JSONUpdatedEncoder)
	print(z1)
	z2 = json.dumps(tm2, cls=JSONUpdatedEncoder)
	print(z2)
	z3 = json.dumps(tm3, cls=JSONUpdatedEncoder)
	print(z3)
	z1b = json.loads(z1, cls=JSONUpdatedDecoder)
	z2b = json.loads(z2, cls=JSONUpdatedDecoder)
	z3b = json.loads(z3, cls=JSONUpdatedDecoder)
	print(type(tm1))
	print(type(z1b))
	print(tm1)
	print(z1b)

	print(type(tm2))
	print(type(z2b))
	print(tm2)
	print(z2b)

	print(type(tm3))
	print(type(z3b))
	print(tm3)
	print(z3b)



	test1_obj = [tdict, tlist]
	test1_json = json.dumps(test1_obj)
	test1_new = json.loads(test1_json)

	print("test1_json: ", test1_json)
	print("test1_obj:", test1_obj)
	print("test1_new:", test1_new)
	#jview(test1_obj)
	#jview(test1_new)
	print()



	test2_obj = [tdict, tdf, tlist]
	test2_json = json.dumps(test2_obj, cls=JSONUpdatedEncoder)
	test2_new = json.loads(test2_json, cls=JSONUpdatedDecoder)
	print("test2_json: ", test2_json)
	print("test2_obj:", test2_obj)
	print("test2_new:", test2_new)


	jview(test2_obj)
	print()
	print()
	print()
	print()
	print()
	print(test2_json)
	print()
	print(test2_new)

	jview(test2_new) # breaks in 276
	#exit()

	test3_obj = [tm1, tdict, tlist, tm2, tdf, tm3]
	test3_json = json.dumps(test3_obj, cls=JSONUpdatedEncoder)


	df = tdf

	#print(df)

	A = [19, "frank", False]
	B = {"zoo": 27, "frank": A}

	Aj = json.dumps(A)
	Bj = json.dumps(B)
	#print(Aj)
	#print(Bj)

	c0 = [19, "frank", False, df]
	print("c0: ", c0)
	print("type(c0):", type(c0))
	print("type(c0[3]):", type(c0[3]))
	print("c0[3]:", c0[3])
	print()

	cj = json.dumps(c0, cls=JSONUpdatedEncoder)

	print("cj: ", cj)
	print("type(cj): ", type(cj))
	print()

	c2 = json.loads(cj,cls=JSONUpdatedDecoder)

	print("c2:", c2)
	print("type(c2):", type(c2))
	print("type(c2[3]):", type(c2[3]))
	print("c2[3]:", c2[3])










