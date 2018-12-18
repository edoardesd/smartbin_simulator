#!/usr/bin/python3

import pymongo

class MyDB():

	def __init__(self):
		self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mydb = self.myclient["bin_simulation"]
		self.coordinates = self.mydb["coordinates"]
		self.dimension = self.mydb["dimension"]
		self.restore = self.mydb["restore_values"]


	def available_dbs(self):
		print(self.myclient.list_database_names())

	def store_final_values(self, my_query, my_update):
		for q, u in zip(my_query, my_update):
			x = self.restore.update(q, u)

	def last_values(self, my_id):
		_where = {"_id": my_id}
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

	def create_collection(self, name):
		self.mycol = self.mydb[name]
		self.mydict = { "name": "John", "address": "Highway 37" }

		self.x = self.mycol.insert_one(self.mydict)
		print(self.x)
		self.collist = self.mydb.list_collection_names()
		print(self.collist)
		if name in self.collist:
			print("The collection exists.")
			return True
		else: 
			return False