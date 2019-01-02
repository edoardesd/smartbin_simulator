#!/usr/bin/python3

import pymongo

class MyDB():

	def __init__(self, db_type):
		self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mydb = self.myclient[db_type]
		
	def _createCol(self, my_col, my_update):
		col = self.mydb[my_col]
		col.delete_many({})	

		for u in my_update:
			x = col.insert(u)


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
							"weight": value["weight"],
						    "height": value["height"]})

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

