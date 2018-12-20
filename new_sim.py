#!/usr/bin/python3
import random
import numpy as np
import paho.mqtt.client as mqtt
import json 
from time import sleep
import datetime
from dateutil.parser import parse
import pprint as pp
import mongodb
import signal
import sys
#my imports
import constants as c

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
    		recolect(bins)
    		print("EMPTY ALL THE BINS!!!")



###### TS FUNCTIONS ######
#next day

class MyTimestamp():
		def __init__(self, starting_ts):
			self.now = starting_ts
		
	def update_timestamp(_hour, _day, _month, _year):
		if _hour%24 == 0:
			_day += 1
			_hour = 0
			print("It's midnight, a new day has been started.")
			print("Today is ", day_of_week(_day))
			day_distribution(behavior(day_of_week(_day)), bins)

		#next month
		if _day==31:
			_month += 1
			_day = 1
			print("new month number: ", _month)

		#next year
		if _month%13 == 0:
			_year += 1
			_month = 1
			print("Happy new year!!!", _year)

		return _hour, _day, _month, _year

	def create_first_ts(present=1):
		if present:
			#split date time
			_now = datetime.datetime.now()
			_year, _month, _day = list(map(int,str(_now.date()).split("-")))
			_hour, _minutes, _seconds = list(map(int,str(_now.time())[:-8].split(":")))
			_day_week = int(_now.today().weekday())

		else:
			pass
			#TODO

		return _year, _month, _day, _hour, _minutes, _seconds, _day_week

	def day_of_week(day):
		if day%7==0:
			weekday="Monday"
		if day%7==1:
			weekday="Tuesday"
		if day%7==2:
			weekday="Wednesday"
		if day%7==3:
			weekday="Thursday"
		if day%7==4:
			weekday="Friday"
		if day%7==5:
			weekday="Saturday"
		if day%7==6:
			weekday="Sunday"
		return weekday

	def full_fake_ts(_year, _month, _day, _hour):
		return str(parse("{0}-{1}-{2} {3}:00:00".format(_year, _month, _day, _hour)))


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
	print("BEHA", behavior)
	for key, val in my_bins.items():
		d_height, d_weight = distribution(val["usage"])
		val['distribution_height'] = np.outer(d_height, behavior)[0]
		val['distribution_weight'] = np.outer(d_weight, behavior)[0]
		val['distribution_height'] = val['distribution_height'].tolist()
		val['distribution_weight'] = val['distribution_weight'].tolist()

	return my_bins

def prepare_update(my_bins):
	update = []
	query = []
	for key, value in my_bins.items():
		query.append({"_id": value["bin_id"]})
		update.append({"weight": value["weight"], "height": value["height"]})
	
	my_db.store_final_values(query, update)

###### RECOLECTION ######
def recolect(my_bins):
	for key, value in my_bins.items():
		if value['height'] > c.WASTE_LEVEL_RECOLECTION:
			value['height'] = 0
			value['weight'] = 0
	return my_bins

def check_recolection(my_bins, my_day, my_hour):
	if day_of_week(my_day) in c.RECOLECTION_DAYS and my_hour == c.RECOLECTION_HOUR:
		return recolect(my_bins)
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
my_db = mongodb.MyDB() 
bins_coord = my_db.get_coordinates()

###### START PROGRAM ######

_year, _month, _day, _hour, _minutes, _seconds, _day_week = create_first_ts()

bins = {}


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)

	for _index, _coord in enumerate(bins_coord):
		last_height, last_weight = my_db.last_values(_coord["_id"])
		bins[_index] = {
			"bin_id": _coord["_id"].encode("utf-8"),
			"coordinates": {"x": _coord["x"],
							"y": _coord["y"]},
			"timestamp": full_fake_ts(year, month, day, hour),
			"usage": "low",
			"weight": last_weight,
			"height": last_height,
			"total_height": my_db.get_dimension(_coord["_id"])
		}

	day_distribution(behavior(day_of_week(day_week), hour), bins)

	pp.pprint(bins)
	while True:

		hour, day, month, year = update_timestamp(hour, day, month, year)

		#put trash in the bin
		for key, value in bins.items():
			#pop the first value of the 
			current_height = value['distribution_height'].pop(0)
			current_weight = value['distribution_weight'].pop(0)
			value['timestamp'] = full_fake_ts(year, month, day, hour)
			if((current_height + value['height']) <= value['total_height']):
				value['height'] += current_height
				value['weight'] += current_weight
			else:
				print("Bin full")
				#TODO: move current to other bin

			#send mqtt
			#convert the dictionary in a json and in a string
			client.publish("{0}/{1}".format(c.TOPIC_STATUS, str(value['bin_id'])), str(json.dumps(value))) 


		bins = check_recolection(bins, day, hour)
		prepare_update(bins)
		#print(bins)
		print("hour: ", hour)
		hour += 1
		sleep(2)



