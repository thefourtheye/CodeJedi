import json

class GenericModel:

	_aData = {}
	def __init__(self, aData = {}) :
		self._aData = self.createModel(aData)
	
	def asDict(self) :
		return self.createDict(self._aData)

	def asJson(self):
		return json.dumps(self.asDict())

	def getClassFields (self) :
		return self._aData.keys()

	def setx(self, attr, *args, **kwargs):
		if kwargs :
			self._aData[attr] = kwargs;
		elif len(args) == 1 :	
			self._aData[attr] = args[0]

	def getx(self, attr, *args, **kwargs):
		return self._aData[attr]

	def hasx(self, attr, *args, **kwargs):
		if attr in self._aData.keys(): return True
		return False

	def delx(self, attr, *args, **kwargs):
		del self._aData[attr]

	def isScalar(self, value):
		return isinstance(value,(type(None),str,int,float,bool))

	def addx(self, attr, *args, **kwargs):
		if attr not in self._aData.keys():
			self._aData[attr] = []
		if self.isScalar(self._aData[attr]):
			self._aData[attr] = [self._aData[attr]]
		self._aData[attr].append(args[0])

	def createModel	(self, aData) :
		data = {}
		for key, value in aData.iteritems() :
			data[key.lower()] = value if not isinstance(value, dict) else self.__class__(value)
		return data	

	def __getattr__(self, method):
		try:
			if method in ("__str__", "__repr__") :
				def default(*args, **kwargs):
					return str(self.asDict())
				return default
			if method[:3] not in ['get', 'set', 'has', 'add', 'del'] :
				raise Exception('No such method Exists')
			else :
				def default(*args, **kwargs):
					return getattr(self, method[:3] + 'x')(method[3:].lower(), *args, **kwargs);
				return default
		except Exception as ex:
			print "Exception : " , ex.args 

	def createDict(self, aData) :
		data = {}
		for key, value in aData.iteritems() :
			data[key] = value if not isinstance(value, type(self)) else value.asDict()
		return data	

	"""
		This generic model is an abstraction over all the data classes.
		This model abstracts out data entirely from behaviour.
		By using this you don't need to worry about structure of the data objects.
		How to use :
			You can instantiate this class without any data like GenericModel()
			or you can pass dictionary data into it like GenericModel({"data1":"Hello", "data2" : "World"})	
			You also can have nested dictionary like {"data" : {"data1":"Hello world"}}
			You can set a data like "Name" by simply calling	 setName("Hello")
			Similarly you can get a data by calling 	getName() (which will return Hello)
			If any of the value is of type list, and if you want to add data to list(with name say address),
				call      addAddress("221B Baker's street"), it will add to list of addresses
			You can check whether a data (say Name) is present or not using  	hasName(), which will return you boolean values.
			Likewise you can remove a data using 	delName(), which will delete the name attribute from the class
			Other useful functions are 	asDict() which will return you the whole data,
										getClassFields() which returns you all the attribute names
										asJson() which will convert the data to json.

		Examples :	
			d = GenericModel({"name" : "jeeva", "sampleData" : {"Hello":"Hi"}})
			print d.getClassFields()
			print d.getSampleData().getHello()
			d.setName("Hell")
			print d.getName()
			print d.hasName()
			d.delName()
			print d.hasName()
			print d.hasValue()
			print d.hasName()
			d.addValue("AAA")
			print d.getValue()
			d.addValue(['BBB', 'CCC'])
			print d.getValue()
			print d.asJson()
			print d.getClassFields()
	"""
