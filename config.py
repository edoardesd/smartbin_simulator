#!/usr/bin/python3
import random
import pprint as pp
import mongodb


class MyConfig():
	def __init__(self, file_conf, const):
		self.file_conf = file_conf
		self.const = const

		if self.file_conf["prev_config"]:
			print("Load old configuration")
		else:
			self.bins = self._createNewConfig(self.file_conf)
			self._storeAll(self.file_conf, self.bins)
		

	def _createNewConfig(self, my_config):
		print("Create a new configuration")
		bins_conf = {}
		
		print("number of bins", int(my_config["n_of_bins"]))

		usage = random.choices(population=self.const.getUsage(),
							   weights=self._create_weight(my_config["usage"]),
							   k=my_config["n_of_bins"])

		for i in range(my_config["n_of_bins"]):
			_x, _y = self._position(my_config["area"]["x1"], my_config["area"]["x2"], my_config["area"]["y1"], my_config["area"]["y2"])
			bins_conf[i] = {
					"bin_id": "bin"+str(i),
					"coordinates": {"lat": _x,
									"lng": _y},
					"timestamp": "NULL",
					"usage": usage[i],
					"levels": dict((el,0) for el in self.const.getNames()), #create dictionary with 0 from the WASTE_NAME list
					"total_height": my_config["bin_dimension"],
					"building": "NULL",
					"floor": "NULL",
					"description": "NULL"
				}

		pp.pprint(bins_conf)
		return bins_conf

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

	def _storeAll(self, my_config, my_bins):
		my_db = mongodb.MyDB("bin_simulation", "none")
		my_db.storeUpdate(my_bins)
		my_db.storeConstants(my_config)
		print("DONE\n")
