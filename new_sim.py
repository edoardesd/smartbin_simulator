#!/usr/bin/python3

import paho.mqtt.client as mqtt
import json 
from time import sleep
import datetime
import pprint as pp
import signal
import sys
import ast
#my imports
import constants as c
import functions as f

import mongodb
import Timestamp


config_file = " "
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
    print("on topic", topic)

    if topic == c.TOPIC_EMPTY:
    	if m_decode == 'all':
    		my_func.recollect(bins, True)
    	

    if topic == c.TOPIC_CONFIG:

    	global wait_config
    	wait_config = False
		
    	global config_file
    	config_file = m_decode
    	

    	

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


_starting_time = datetime.datetime.now().timestamp()+3600
my_ts = Timestamp.MyTimestamp(_starting_time)
print(my_ts.getFullTs())

my_db = mongodb.MyDB("bin_simulation", _starting_time)
my_const = c.Constants(my_db)
my_func = f.Functions(my_const, my_db)

###### START PROGRAM ######
bins = {}

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)

	while wait_config:
		pass	
	
	config_file = ast.literal_eval(config_file)
	pp.pprint(config_file)
	bins = my_func.load_configuration(config_file, my_ts)
	
	pp.pprint(bins)


	while True:
		print(my_ts.getHour())
		if my_ts.getHour() == 0:
			my_func.day_distribution(my_func.behavior(my_ts.dayOfWeek()), bins)

			print("Today is ", my_ts.getDay(), my_ts.getMonth(), my_ts.getYear())

		#put trash in the bin
		for key, value in bins.items():
			#pop the first value of the 
			current = {}
			value['timestamp'] = my_ts.getFullTs()
			for waste_type in my_const.getNames():
				current[waste_type] = value["distribution"][waste_type].pop(0)
				
				if((current[waste_type] + value['levels'][waste_type]) <= value['total_height']):
					value['levels'][waste_type] += current[waste_type]
				else:
					print(waste_type, " full")
					#TODO: move current to other bin
			

			#send mqtt
			#convert the dictionary in a json and in a string
			client.publish("{0}/{1}".format(c.TOPIC_STATUS, str(value['bin_id'])), json.dumps(value)) 


		bins = my_func.check_recollection(bins, my_ts.dayOfWeek(), my_ts.getHour())
		my_db.updateFinalDB(bins)
		
		sleep(my_const.getSpeed())
		print("-"*10)
		my_ts.updateTimestamp()




