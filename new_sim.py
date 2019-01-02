#!/usr/bin/python3
import random
import numpy as np
import paho.mqtt.client as mqtt
import json 
from time import sleep
import datetime
import pprint as pp
import signal
import sys
#my imports
import constants as c
import mongodb
import Timestamp
import config

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

wait_config = True
###### MQTT FUNCTIONS ######
def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("connected OK")
		client.subscribe(c.TOPIC_CONFIG)
		print(c.TOPIC_EMPTY)
		client.subscribe(c.TOPIC_EMPTY)
	else:
		print("Bad connection Returned code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
	print("Disconnect result code "+str(rc))

def on_message(client, userdata,msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8"))
    print("message received", m_decode)

    print(topic)
    if topic == c.TOPIC_EMPTY:
    	if m_decode == "all":
    		recollect(bins)
    		print("EMPTY ALL THE BINS!!!")

    if topic == c.TOPIC_CONFIG:
    	global wait_config
    	wait_config = False


###### BINS FUNCTIONS ######
def behavior(today, starting_hour = 0):
	if today in ["Sunday", "Saturday"]:
		return c.BIN_BEHAVIOR_END[starting_hour:]
	else:
		return (c.BIN_BEHAVIOR_WEEK[starting_hour:])


def distribution(use):
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
		d_height, d_weight = distribution(val["usage"])
		val['distribution_height'] = np.outer(d_height, behavior)[0]
		val['distribution_weight'] = np.outer(d_weight, behavior)[0]
		val['distribution_height'] = val['distribution_height'].tolist()
		val['distribution_weight'] = val['distribution_weight'].tolist()

	return my_bins

###### RECOLLECTION ######
def recollect(my_bins):
	for key, value in my_bins.items():
		if value['height'] > WASTE_LEVEL_RECOLLECTION:
			value['height'] = 0
			value['weight'] = 0
	return my_bins

def check_recollection(my_bins, my_day, my_hour):
	if my_day in RECOLLECTION_DAYS and my_hour == RECOLLECTION_HOUR:
		return recollect(my_bins)
	else:
		return my_bins 

#close everything in the proper way and store values in database (start when cltr-c is clicked)
def signal_handler(signal, frame):
	print("Exit!")

	#DO SOMETHING?

	sys.exit(0)


###### START MQTT ######
broker = "localhost"
client = mqtt.Client("simulator1") 

client.on_connect = on_connect 
client.on_disconnect = on_disconnect
client.on_message = on_message
print("Connecting to broker ", broker)

client.connect(broker) #connect to broker
client.loop_start() #start loop
###### END MQTT ######

###### MONGODB ######
starting_time = datetime.datetime.now()
my_ts = Timestamp.MyTimestamp(starting_time)

###### START PROGRAM ######
bins = {}

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)

	wait_config = False
	
	my_config = config.MyConfig("old", config_file)
	my_db = mongodb.MyDB("bin_simulation", starting_time) 
	bins_coord = my_db.get_coordinates()
	GLOBAL = my_db.getConstants()

	RECOLLECTION_DAYS = GLOBAL["collection_day"]
	RECOLLECTION_HOUR = GLOBAL["collection_hour"]
	DELAY = GLOBAL["speed"]
	WASTE_LEVEL_RECOLLECTION = GLOBAL["waste_rec_level"] 

	for _index, _coord in enumerate(bins_coord):
		last_height, last_weight = my_db.last_values(_coord["_id"])
		bins[_index] = {
			"bin_id": _coord["_id"],
			"coordinates": {"x": _coord["x"],
							"y": _coord["y"]},
			"timestamp": my_ts.getFullTs(),
			"usage": my_db.getUsage(_coord["_id"]),
			"weight": last_weight,
			"height": last_height,
			"total_height": my_db.get_dimension(_coord["_id"])
		}

	day_distribution(behavior(my_ts.dayOfWeek(), my_ts.getHour()), bins)

	pp.pprint(bins)
	sleep(3)

	while True:
		
		if my_ts.getHour() == 0:
			day_distribution(behavior(my_ts.dayOfWeek()), bins)

			print("Today is ", my_ts.getDay(), my_ts.getMonth(), my_ts.getYear())

		#put trash in the bin
		for key, value in bins.items():
			#pop the first value of the 
			current_height = value['distribution_height'].pop(0)
			current_weight = value['distribution_weight'].pop(0)
			value['timestamp'] = my_ts.getFullTs()
			if((current_height + value['height']) <= value['total_height']):
				value['height'] += current_height
				value['weight'] += current_weight
			else:
				print("Bin full")
				#TODO: move current to other bin

			#send mqtt
			#convert the dictionary in a json and in a string
			client.publish("{0}/{1}".format(c.TOPIC_STATUS, str(value['bin_id'])), json.dumps(value)) 


		bins = check_recollection(bins, my_ts.dayOfWeek(), my_ts.getHour())
		my_db.updateFinalDB(bins)
		
		sleep(DELAY)
		print("-"*10)
		my_ts.updateTimestamp()




