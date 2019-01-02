#!/usr/bin/python3
import random
import pprint as pp

import DBStore

bins = {}

config = {
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

usage_type = ["very_low", "low", "mid", "high", "very_high"]

def position(sizex1, sizex2, sizey1, sizey2):
    posx = random.uniform(sizex1, sizex2)
    posy = random.uniform(sizey1, sizey2)
    return posx, posy


def create_weight(my_usage):
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

if __name__ == "__main__":
	
	if not config["prev_config"]:
		print("Create a new configuration")
		usage = random.choices(population=usage_type, weights=create_weight(config["usage"]), k=config["n_of_bins"])

		for i in range(config["n_of_bins"]):
			_x, _y = position(config["area"]["x1"], config["area"]["x2"], config["area"]["y1"], config["area"]["y2"])
			bins[i] = {
					"bin_id": str("bin"+str(i)),
					"coordinates": {"x": _x,
									"y": _y},
					"timestamp": "NULL",
					"usage": usage[i],
					"weight": 0,
					"height": 0,
					"total_height": config["bin_dimension"],
					"building": "NULL",
					"floor": "NULL",
					"description": "NULL"

			}

		my_db = DBStore.MyDB("bin_simulation") 
		my_db.storeUpdate(bins)
		my_db.storeConstants(config)
		print("DONE\n")

	else:
		print("Load old configuration")


#generate bins
	#coordinates
	#usage

#speed
#recollection day
#recollection hour