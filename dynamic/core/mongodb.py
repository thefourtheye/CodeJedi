from pymongo import MongoClient
from bson.objectid import ObjectId
from genericmodel import GenericModel
from common import Context
from sys import exit

class MongoDb :

	def __init__(self, dbName = None, host = None, port = None, userName = None, password = None) :
		_host     = Context.Config.getDB().getHost()      if (host == None)     else host
		_port     = Context.Config.getDB().getPort()      if (port == None)     else port
		_dbName   = Context.Config.getDB().getDB()        if (dbName == None)   else dbName
		_username = Context.Config.getDB().getUser()      if (userName == None) else userName
		_password = Context.Config.getDB().getPwd()       if (password == None) else password
		_prefix   = "" if (_username == "") else _username+":"+_password+"@"
		ConnectionString = "mongodb://" + _prefix + _host + ":" + _port + "/" + _dbName
		self._db = None
		try:
			connection = MongoClient(ConnectionString)
			self._db = connection[_dbName]
		except Exception:
			print Exception
			print ConnectionString
			exit(0)

	def insert(self, data, collection) :
		return self._db[collection].insert(data.asDict())
	
	def remove(self, pattern, collection) :
		self._db[collection].remove(pattern)

	def removeById(self, _id, collection) :
		self._db[collection].remove({"_id" :  ObjectId(_id)})
	
	def update(self, pattern, data, collection, option = 'set', _upsertStatus = False) :
		_data = data.asDict()
		if 'id' in _data :
			raise TypeError("id can not be changed. Try removing id from the data to be saved/updated")
		if 'id' in pattern :
			pattern['_id'] = ObjectId(pattern['id'])
			del pattern['id']
		self._db[collection].update(pattern, { '$' + option : _data}, upsert = _upsertStatus)
	
	def save(self, pattern, data, collection, option = 'set') :
		self.update(pattern, data, collection, option, True)

	def count (self, pattern, collection) :
		return self._db[collection].find(pattern).count()
	
	def find(self, pattern, collection) :
		resultSet = self._db[collection].find(pattern)
		return [self._processResult(document) for document in resultSet]
	
	def _processResult(self, result) :
		result['id'] = str(result['_id'])
		del result['_id']
		return GenericModel(result)
	
	def findById(self, _id, collection) :
		result = self._db[collection].find_one({"_id": ObjectId(_id)})
		if result is None: return result
		return self._processResult(result)

def getConf(conf) :
	return Context.Config.getDB()[conf]
