#!/usr/bin/python3
from dateutil.parser import parse




class MyTimestamp():
	def __init__(self, starting_ts):
		self.now = starting_ts
		self.year, self.month, self.day = list(map(int,str(self.now.date()).split("-")))
		self.hour, self.minutes, self.seconds = list(map(int,str(self.now.time())[:-8].split(":")))
		self.day_week = int(self.now.today().weekday())

		#print(self.year, self.month, self.day, self.hour)
		#print("today is", self.dayOfWeek())	

	def updateTimestamp(self):
		self.hour += 1

		self._nextDay()
		self._nextMonth()
		self._nextYear()



	def getYear(self):
		return self.year
	def getMonth(self):
		return self.month
	def getDay(self):
		return self.day
	def getHour(self):
		return self.hour
	#def getDayWeek(self):
	#	return self.day_week

	def getAll():
		return self.year, self.month, self.day, self.hour, self.day_week

	def dayOfWeek(self):
		if self.day_week%7==0:
			return "Monday"
		if self.day_week%7==1:
			return "Tuesday"
		if self.day_week%7==2:
			return "Wednesday"
		if self.day_week%7==3:
			return "Thursday"
		if self.day_week%7==4:
			return "Friday"
		if self.day_week%7==5:
			return "Saturday"
		if self.day_week%7==6:
			return "Sunday"

	def getFullTs(self):
		try:
			ts_string = str(parse("{0}-{1}-{2} {3}:00:00".format(self.year, self.month, self.day, self.hour)))
		except ValueError as e:
			ts_string = "00-00-00_12:12:12"
			print("Error: ", e)

		return ts_string

	def _nextDay(self):
		if self.hour%24 == 0:
			self.day += 1
			self.hour = 0
			self.day_week += 1
			print("It's midnight, a new day has been started.")
			

	def _nextMonth(self):
			#TODO: months with different days
			if self.day==31:
				self.month += 1
				self.day = 1
				print("new month number: ", self.month)


	def _nextYear(self):
		if self.month%13 == 0:
			self.year += 1
			self.month = 1
			print("Happy new year!!!", self.year)
		