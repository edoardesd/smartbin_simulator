#!/usr/bin/python3
import random
import pprint as pp

import DBStore
import constants as c




class MyConfig():
	def __init__(self, conf_type, file_conf = None):
		self.type = conf_type

		if self.type == "old":
			print("Load old configuration")
		elif self.type == "new":
			self.file_conf = file_conf
			self.bins = self._createNewConfig(self.file_conf)
			self._storeConstants(self.file_conf, self.bins)
		else:
			print("FUCKIJNG ERROR!")

	def _createNewConfig(self, my_config):
		print("Create a new configuration")
		bins = {}
		usage = random.choices(population=c.USAGE_TYPE, weights=self._create_weight(my_config["usage"]), k=my_config["n_of_bins"])

		for i in range(my_config["n_of_bins"]):
			_x, _y = self._position(my_config["area"]["x1"], my_config["area"]["x2"], my_config["area"]["y1"], my_config["area"]["y2"])
			bins[i] = {
					"bin_id": "bin"+str(i),
					"coordinates": {"x": _x,
									"y": _y},
					"timestamp": "NULL",
					"usage": usage[i],
					"weight": 0,
					"height": 0,
					"total_height": my_config["bin_dimension"],
					"building": "NULL",
					"floor": "NULL",
					"description": "NULL"
				}
		return bins

	def _position(self, sizex1, sizex2, sizey1, sizey2):
	    posx = random.uniform(sizex1, sizex2)
	    posy = random.uniform(sizey1, sizey2)
	    return posx, posy


	def _create_weight(self, my_usage):
		if my_usage == "mid":
			w = [.1, .2, .4, .2, .1]
		if my_usage == "high":
			w = [.1, .1, .2, .4, .2]
		if my_usage == "very_high":
			w = [.1, .1, .2, .2, .4]
		if my_usage == "low":
			w = [.2, .4, .2, .1, .1]
		if my_usage == "very_low":
			w = [.4, .2, .2, .1, .1]
		
		return w

	def _storeConstants(self, my_config, my_bins):
		my_db = DBStore.MyDB("bin_simulation") 
		my_db.storeUpdate(my_bins)
		my_db.storeConstants(my_config)
		print("DONE\n")



#generate bins
	#coordinates
	#usage

#speed
#recollection day
#recollection hour