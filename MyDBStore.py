#!/usr/bin/python3

import pymongo

class MyDB2():

	def __init__(self, db_type):
		self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mydb = self.myclient[db_type]
		print("asd")
		#self.coordinates = self.mydb["coordinates"]
		#self.dimension = self.mydb["dimension"]
		#self.restore = self.mydb["restore_values"]
		#self.usage = self.mydb["usage"]

		def _create_col(self, my_col, my_query, my_update):
			col = self.mydb[my_col]
			col.delete_many({})	

			for q, u in zip(my_query, my_update):
				x = col.insert(u)

		def ciao(self):
			pass

		def store_update(self, my_config):
			print("ciao")
			query = []
			coord = []
			dimension = []
			usage = []
			old_val = []
			for key, value in my_config.items():
				query.append({"_id": value["bin_id"]})
				coord.append({"x": value["coordinates"]["x"],
							  "y": value["coordinates"]["y"],
							  "building": value["building"],
							  "floor": value["floor"], 
							  "description": value["description"]})
				dimension.append({"total_height": value["total_height"]})
				usage.append({"usage": value["usage"]})
				old_val.append({"weight": value["weight"],
							   "height": value["height"]})

			self._create_col("coordinates", query, coord)
			self._create_col("dimension", query, dimension)
			self._create_col("usage", query, usage)
			self._create_col("restore_values", query, usage)

			return True
