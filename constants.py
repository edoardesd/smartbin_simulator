#!/usr/bin/python3

import mongodb

class Constants():
	def __init__(self, db):
		self.db = db
		self.waste_name = ["unsorted", "plastic", "paper", "glass"]
		self.usage_type = ["very_low", "low", "mid", "high", "very_high"]

	def loadConstants(self):
		self.col_day, self.col_hour, self.speed, self.waste_rec = self.db.getConstants()

	def getCollDay(self):
		return self.col_day

	def getCollHour(self):
		return self.col_hour

	def getSpeed(self):
		return self.speed

	def getWasteRec(self):
		return self.waste_rec

	def getBinWeek(self):
		return [0, 0, 0, 0, 0, 0, 0, 0.02, 0.02, 0.1, 0.1, 0.02, 0.2, 0.2, 0.02, 0.02, 0.1, 0.1, 0.02, 0.02, 0.02, 0.02, 0, 0]

	def getBinEnd(self):
		return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def getNames(self):
		return self.waste_name

	def getUsage(self):
		return self.usage_type


TOPIC_BIN = "smartbin"
## CTRL
TOPIC_CTRL = TOPIC_BIN+"/ctrl"
TOPIC_EMPTY = TOPIC_CTRL+"/emptybin"
TOPIC_CONFIG = TOPIC_CTRL+"/config"
## STATUS
TOPIC_STATUS = TOPIC_BIN+"/status"



config_file = {
			  "prev_config": False,
			  "n_of_bins": 12,
			  "usage": "mid",
			  "bin_dimension": 100,
			  "collection_day": ["Tuesady", "Thursday"],
			  "collection_hour": 18,
			  "speed": 2,
			  "waste_rec_level": 65,
			  "area": {"x1": 10,
			  		   "y1": 10,
			  		   "x2": 11,
			  		   "y2": 11}
			  }	