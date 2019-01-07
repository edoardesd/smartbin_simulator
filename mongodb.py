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

		self.values = self._createHistoryCollection(self.historydb, my_time)


	def available_dbs(self):
		print(self.myclient.list_database_names())

	##### STORING FUNCTIONS #####
	def updateFinalDB(self, my_bins):
		final_update = []
		local_update = {}
		query = []
		for key, value in my_bins.items():
			update = {"levels": value['levels']}

			query.append({"_id": value["bin_id"]})
			final_update.append(update)
			local_update[value["bin_id"]] = update

		local_update["_id"] = my_bins[0]["timestamp"]
		self._store_final_values(query, final_update)
		self._store_values(local_update)

	def storeUpdate(self, my_config):
		coord = []
		dimension = []
		usage = []
		old_val = []
		for key, value in my_config.items():
			coord.append({"_id": value["bin_id"],
						  "x": value["coordinates"]["x"],
						  "y": value["coordinates"]["y"],
						  "building": value["building"],
						  "floor": value["floor"], 
						  "description": value["description"]})
			dimension.append({"_id": value["bin_id"], "total_height": value["total_height"]})
			usage.append({"_id": value["bin_id"], "usage": value["usage"]})
			old_val.append({"_id": value["bin_id"],
							"levels": value['levels']
						    })

		self._createCol("coordinates", coord)
		self._createCol("dimension", dimension)
		self._createCol("usage", usage)
		self._createCol("restore_values", old_val)

	def storeConstants(self, my_config):
		constants = [{"_id": "config",
						"collection_day": my_config["collection_day"],
				   	    "collection_hour": my_config["collection_hour"],
				   	    "speed": my_config["speed"],
				   	    "waste_rec_level": my_config["waste_rec_level"]}]

		self._createCol("constants", constants)

	##### QUERYING FUNCTIONS #####
	def getUsage(self, my_id):
		_where = {"_id": my_id}
		_select = {"_id": 0, "usage": 1}
		for x in self.usage.find(_where, _select):
			return x['usage']

	def last_values(self, my_id):
		_where = {"_id": my_id}
		_select = {"_id": 0, "levels": 1}
		for x in self.restore.find(_where, _select):
			return x["levels"]

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

	def getConstants(self):
		constants = self.mydb["constants"]
		x = constants.find_one()
		return x["collection_day"], x["collection_hour"], x["speed"], x["waste_rec_level"]



	##### PRIVATE METHODS #####
	def _createHistoryCollection(self, db_name, coll_name):
		simulation_name = "simulation_"+str(coll_name)[:-7].replace(" ", "_")
		return db_name[simulation_name]

	def _store_final_values(self, my_query, my_update):
		for q, u in zip(my_query, my_update):
			x = self.restore.update(q, u)

	def _store_values(self, my_update):
		x = self.values.insert(my_update)

	def _createCol(self, my_col, my_update):
		col = self.mydb[my_col]
		col.delete_many({})	

		for u in my_update:
			x = col.insert(u)
