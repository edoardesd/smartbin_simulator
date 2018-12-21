#!/usr/bin/python3
import random
config = {
			  "n_of_bins": 12,
			  "usage": "mid",
			  "bin_dimension": 100,
			  "collection_day": "Tue",
			  "collection_hour": 10,
			  "speed": 200,
			  "waste_rec_level": 65,
			  "area": {"x": 10,
			  		   "y": 10}
			  }


def position(sizex1, sizex2, sizey1, sizey2):
    posx=random.uniform(sizex1, sizex2)
    posy=random.uniform(sizey1, sizey2)
    return posx, posy


if __name__ == "__main__":
	
	print(random.choices( population=["low", "mid", "high"], weights=[0.2, 0.2, 0.6],k=10))



#generate bins
	#coordinates
	#usage

#speed
#recollection day
#recollection hour