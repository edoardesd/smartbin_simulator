#!/usr/bin/python3

import pymongo

class MyDB():

	def __init__(self, db_type, my_time):
		self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mydb = self.myclient[db_type]
		self.historydb = self.myclient["bin_historical"]
		self.coordinates = self.mydb["coordinates"]
		self.dimension = self.mydb["dimension"]
		self.restore = self.mydb["restore_values"]
		self.usage = self.mydb["usage"]
		self.constants = self.mydb["constants"]

		self.values = self.createHistoryCollection(self.historydb, my_time)


	def available_dbs(self):
		print(self.myclient.list_database_names())

	def _store_final_values(self, my_query, my_update):
		for q, u in zip(my_query, my_update):
			x = self.restore.update(q, u)

	def _store_values(self, my_update):
		x = self.values.insert(my_update)

	def getUsage(self, my_id):
		_where = {"_id": my_id}
		_select = {"_id": 0, "usage": 1}
		for x in self.usage.find(_where, _select):
			return x['usage']

	def last_values(self, my_id):
		_where = {"_id": my_id}
		print(my_id)
		_select = {"_id": 0, "height": 1, "weight": 1}
		for x in self.restore.find(_where, _select):
			return x['height'], x['weight']

	def get_dimension(self, my_id):
		_where = {"_id": my_id}
		_select = {"_id": 0, "total_height": 1}
		for x in self.dimension.find(_where, _select):
			return x['total_height']

	def get_coordinates(self, building=0):
		_bins = []
		_select = { "_id": 1, "x": 1, "y": 1}
		if building == 0:
			_where = {}
		else:
			_where = {"building": building }
			
		for x in self.coordinates.find(_where, _select):
				_bins.append(x)

		return _bins

	def updateFinalDB(self, my_bins):
		final_update = []
		local_update = {}
		query = []
		for key, value in my_bins.items():
			query.append({"_id": value["bin_id"]})
			final_update.append({"weight": value["weight"], "height": value["height"]})
			local_update[value["bin_id"]] = {"weight": value["weight"], "height": value["height"]}

		local_update["_id"] = my_bins[0]["timestamp"]
		self._store_final_values(query, final_update)
		self._store_values(local_update)

	def createHistoryCollection(self, db_name, coll_name):
		simulation_name = "simulation_"+str(coll_name)[:-7].replace(" ", "_")
		return db_name[simulation_name]

	#maybe_unused
	def getConstants(self):
		return self.constants.find_one()



