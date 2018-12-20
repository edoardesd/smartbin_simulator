BINS_NUMBER = 2
DELAY = 1 #delay between two simulations
TOTAL_HEIGHT = 100 #cm of the bin  
RECOLLECTION_DAYS = "Tuesday", "Thursday"
RECOLLECTION_HOUR = 20 #bins are recollected at RECOLKECTION_HOUR
WASTE_LEVEL_RECOLLECTION = 65 #level wether or not recollect
BIN_BEHAVIOR_WEEK = [0, 0, 0, 0, 0, 0, 0, 0.02, 0.02, 0.1, 0.1, 0.02, 0.2, 0.2, 0.02, 0.02, 0.1, 0.1, 0.02, 0.02, 0.02, 0.02, 0, 0]
BIN_BEHAVIOR_END=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


TOPIC_BIN = "smartbin"
TOPIC_CTRL = TOPIC_BIN+"/ctrl"
TOPIC_STATUS = TOPIC_BIN+"/status"
TOPIC_EMPTY = TOPIC_CTRL+"/emptybin"
TOPIC_CONFIG = TOPIC_CTRL+"/config"