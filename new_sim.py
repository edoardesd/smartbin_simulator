#!/usr/bin/python3
import random
import numpy as np
import paho.mqtt.client as mqtt 
from time import sleep

#my imports
import constants as c

###### MQTT FUNCTIONS ######
def on_connect(client, userdata, flags, rc):
	if rc==0:
		print("connected OK")
	else:
		print("Bad connection Returned code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
	print("Disconnect result code "+str(rc))

def on_message(client, userdata,msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8"))
    print("message received", m_decode)

###### BINS FUNCTIONS ######
def behavior(today):
	if today in ["Sunday", "Saturday"]:
		return c.BIN_BEHAVIOR_END
	else:
		return c.BIN_BEHAVIOR_WEEK

def day_of_week(day):
	if day%7==0:
		weekday="Sunday"
	if day%7==1:
		weekday="Monday"
	if day%7==2:
		weekday="Tuesday"
	if day%7==3:
		weekday="Wednesday"
	if day%7==4:
		weekday="Thursday"
	if day%7==5:
		weekday="Friday"
	if day%7==6:
		weekday="Saturday"
	return weekday

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
		val['distribution_height'][0] += val['height']
		val['distribution_weight'][0] += val['weight']
		val['distribution_height'] = np.cumsum(val['distribution_height'])
		val['distribution_weight'] = np.cumsum(val['distribution_weight'])
		val['distribution_height'] = np.clip(val['distribution_height'], 0, val['total_height'])
		val['distribution_weight'] = np.clip(val['distribution_weight'], 0, val['total_height'])

	return my_bins


###### START MQTT ######
broker = "localhost"
client = mqtt.Client("python1") 

client.on_connect = on_connect 
client.on_disconnect = on_disconnect
client.on_message = on_message
print("Connecting to broker ", broker)

client.connect(broker) #connect to broker
client.loop_start() #start loop
###### END MQTT ######

###### START PROGRAM ######
hour = 1  
day = 1   
week = 0  
#today = "Monday"

bins = {}

for i in range(c.BINS_NUMBER):
	bins[i] = {
		"bin_id": "bin"+str(i),
		"posX": 9,
		"posY": 9,
		"weight": 0,
		"height": 19,
		"total_height": 100,
		"timestamp": "2018-12-10 10:10:10",
		"usage": "low"
	}

day_distribution(behavior(day_of_week(day)), bins)

print(bins)

while True:

	#next day
	if hour%24 == 0:
		day = day+1
		hour = 0
		print("It's midnight, a new day has been started.")
		print("Today is ", day_of_week(day))
		
		day_distribution(behavior(day_of_week(day)), bins)
		print(bins)

	#put trash in the bin
	for key, value in bins.items():
		#pop the first value of the array
		#sum the previous value of trash with the value popped
		#check if its above size, 
			#if yes TODO: move to other bin
		pass
		#send mqtt
		client.publish("%s/%s" %(c.TOPIC_BIN) %value['bin_id'], value)

	hour += 1
	sleep(2)



