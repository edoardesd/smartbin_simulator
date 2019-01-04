#!/usr/bin/python3
import constants
import random
import numpy as np
import config


const = constants.Constants()

###### CONFIG #####
def load_configuration(my_config_file, ts, db):
	starting_bins = {}
	#already in msg, fix new and old
	my_config = config.MyConfig("new", my_config_file)
	bins_coord = db.get_coordinates()

	for _index, _coord in enumerate(bins_coord):
		last_height, last_weight = db.last_values(_coord["_id"])
		starting_bins[_index] = {
			"bin_id": _coord["_id"],
			"coordinates": {"x": _coord["x"],
							"y": _coord["y"]},
			"timestamp": ts.getFullTs(),
			"usage": db.getUsage(_coord["_id"]),
			"weight": last_weight,
			"height": last_height,
			"total_height": db.get_dimension(_coord["_id"])
		}

	day_distribution(behavior(ts.dayOfWeek(), ts.getHour()), starting_bins)

	return starting_bins

###### BINS FUNCTIONS ######
def behavior(today, starting_hour = 0):
	if today in ["Sunday", "Saturday"]:
		return const.getBinEnd()[starting_hour:]
	else:
		return (const.getBinWeek()[starting_hour:])


def _distribution(use):
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

def day_distribution(behavior, my_bins):
	for key, val in my_bins.items():
		d_height, d_weight = _distribution(val["usage"])
		val['distribution_height'] = np.outer(d_height, behavior)[0]
		val['distribution_weight'] = np.outer(d_weight, behavior)[0]
		val['distribution_height'] = val['distribution_height'].tolist()
		val['distribution_weight'] = val['distribution_weight'].tolist()

	return my_bins


###### RECOLLECTION ######
def _recollect(my_bins):
	for key, value in my_bins.items():
		if value['height'] > const.getWasteRec():
			value['height'] = 0
			value['weight'] = 0
	return my_bins

def check_recollection(my_bins, my_day, my_hour):
	if my_day in const.getCollDay() and my_hour == const.getCollHour():
		return _recollect(my_bins)
	else:
		return my_bins 



