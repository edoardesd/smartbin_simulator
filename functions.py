#!/usr/bin/python3
import random
import numpy as np
import config

class Functions():
	def __init__(self, const, db):
		self.const = const
		self.db = db

	###### CONFIG #####
	def load_configuration(self, my_config_file, ts):
		starting_bins = {}
		#already in msg, fix new and old
		my_config = config.MyConfig(my_config_file)
		self.const.loadConstants()
		bins_coord = self.db.get_coordinates()

		for _index, _coord in enumerate(bins_coord):
			last_height, last_weight = self.db.last_values(_coord["_id"])
			starting_bins[_index] = {
				"bin_id": _coord["_id"],
				"coordinates": {"x": _coord["x"],
								"y": _coord["y"]},
				"timestamp": ts.getFullTs(),
				"usage": self.db.getUsage(_coord["_id"]),
				"weight": last_weight,
				"height": last_height,
				"total_height": self.db.get_dimension(_coord["_id"])
			}

		self.day_distribution(self.behavior(ts.dayOfWeek(), ts.getHour()), starting_bins)

		return starting_bins

	###### BINS FUNCTIONS ######
	def behavior(self, today, starting_hour = 0):
		if today in ["Sunday", "Saturday"]:
			return self.const.getBinEnd()[starting_hour:]
		else:
			return (self.const.getBinWeek()[starting_hour:])


	def _distribution(self, use):
		if use=="very_low":
			size_waste=abs(np.random.normal(loc=10, scale=8))
			weight_waste=abs(np.random.normal(loc=1, scale=1))
		if use=="low":
			size_waste=abs(np.random.normal(loc=30, scale=10))
			weight_waste=abs(np.random.normal(loc=2.5, scale=1.5))
		if use=="mid":
			size_waste=abs(np.random.normal(loc=50, scale=15))
			weight_waste=abs(np.random.normal(loc=5, scale=2))
		if use=="high":
			size_waste=abs(np.random.normal(loc=70, scale=10))
			weight_waste=abs(np.random.normal(loc=7.5, scale=1.5))
		if use=="very_high":
			size_waste=abs(np.random.normal(loc=90, scale=8))
			weight_waste=abs(np.random.normal(loc=10, scale=1))

		return size_waste, weight_waste

	def day_distribution(self, behavior, my_bins):
		for key, val in my_bins.items():
			d_height, d_weight = self._distribution(val["usage"])
			val['distribution_height'] = np.outer(d_height, behavior)[0]
			val['distribution_weight'] = np.outer(d_weight, behavior)[0]
			val['distribution_height'] = val['distribution_height'].tolist()
			val['distribution_weight'] = val['distribution_weight'].tolist()

		return my_bins


	###### RECOLLECTION ######
	def recollect(self, my_bins, force=False):
		print("Empty the bins!")

		for key, value in my_bins.items():
			if value['height'] > self.const.getWasteRec() or force:
				value['height'] = 0
				value['weight'] = 0
		return my_bins

	def check_recollection(self, my_bins, my_day, my_hour):
		if my_day in self.const.getCollDay() and my_hour == self.const.getCollHour():
			return self.recollect(my_bins)
		else:
			return my_bins 



