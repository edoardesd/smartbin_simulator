#!/usr/bin/python3
import random
import numpy as np
from scipy import spatial

import config


class Functions():
	def __init__(self, const, db):
		self.const = const
		self.db = db

	###### CONFIG #####
	def load_configuration(self, my_config_file, ts):
		starting_bins = {}
		#already in msg, fix new and old
		my_config = config.MyConfig(my_config_file, self.const)
		self.const.loadConstants()
		bins_coord = self.db.get_coordinates()

		for _index, _coord in enumerate(bins_coord):
			#last values as a dictionary
			last_vals = self.db.last_values(_coord["_id"])
			starting_bins[_index] = {
				"bin_id": _coord["_id"],
				"coordinates": {"x": _coord["x"],
								"y": _coord["y"]},
				"timestamp": ts.getFullTs(),
				"usage": self.db.getUsage(_coord["_id"]),
				"levels": last_vals,
				"distribution": {},
				"total_height": self.db.get_dimension(_coord["_id"]),
				"collection_name": self.db.getSimulationName()
			}

		self.bins = self.day_distribution(self.behavior(ts.dayOfWeek(), ts.getHour()), starting_bins)
	
		return self.bins

	###### BINS FUNCTIONS ######
	def behavior(self, today, starting_hour = 0):
		if today in ["Sunday", "Saturday"]:
			return self.const.getBinEnd()[starting_hour:]
		else:
			return (self.const.getBinWeek()[starting_hour:])


	def _distribution(self, use):
		dist = {}
		for waste_type in self.const.getNames():
			my_loc, my_scale = self._getLocScale(waste_type)
			if use=="very_low":
				dist[waste_type] = abs(np.random.normal(my_loc*1, my_scale-my_scale*0.5))
			if use=="low":
				dist[waste_type] = abs(np.random.normal(my_loc*3, my_scale-my_scale*0.35))
			if use=="mid":
				dist[waste_type] = abs(np.random.normal(my_loc*5, my_scale))
			if use=="high":
				dist[waste_type] = abs(np.random.normal(my_loc*7, my_scale-my_scale*0.35))
			if use=="very_high":
				dist[waste_type] = abs(np.random.normal(my_loc*9, my_scale-my_scale*0.5))

		return dist

	def _getLocScale(self, my_type):
		if my_type == "unsorted":
			return 10, 15
		if my_type == "plastic":
			return 8, 10
		if my_type == "paper":
			return 7, 8
		if my_type == "glass":
			return 1.3, 2

	def day_distribution(self, behavior, my_bins):
		for key, val in my_bins.items():
			distributions = self._distribution(val["usage"])
			for waste_type in self.const.getNames():
				val["distribution"][waste_type] = np.outer(distributions[waste_type], behavior)[0].tolist()
			
		return my_bins


	###### RECOLLECTION ######
	def recollect(self, my_bins, force=False):
		print("Empty the bins!")
		for key, value in my_bins.items():
			for waste_type, level in value['levels'].items():
				if level > self.const.getWasteRec() or force:
					my_bins[key]['levels'][waste_type] = 0
		return my_bins

	def check_recollection(self, my_bins, my_day, my_hour):
		if my_day in self.const.getCollDay() and my_hour == self.const.getCollHour():
			return self.recollect(my_bins)
		else:
			return my_bins 

	def _getCoord(self):
		self.coordinates = []
		for key, val in self.bins.items():
			self.coordinates.append([val["coordinates"]["x"], val["coordinates"]["y"]])

		return self.coordinates

	def calculateNeighbours(self, sigle_bin, deep):
		tree = spatial.KDTree(self._getCoord())
		pts = np.array([sigle_bin["coordinates"]["x"], sigle_bin["coordinates"]["y"]])
		distance, location =  tree.query(pts, k=deep)
		return location[-1:][0]

		