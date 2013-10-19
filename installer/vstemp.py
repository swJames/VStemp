#!/usr/bin/python
# -*- coding: utf-8 -*-
import commands, re
from commands import getstatusoutput
from time import sleep
from subprocess import call
from os import devnull
from datetime import datetime

class getTemperature:

	def __init__(self):
		self.fanperiod = 0
		self.fanspeed = 0
		self.config = {}
		self.debugmode = False
		execfile("/opt/vstemp/config", self.config)

	def getTemp(self):
		temp = getstatusoutput('sensors')
		temp = temp[1].split("\n");
		temperature = []
		for i in temp:
			result = self.findTemp(i)
			if result != False:
				temperature.extend([result])
		try:
			self.switchTemp(max(temperature))
		except:
			self.writeToLog(temperature, 'ERROR!!!!!!!!!')
			self.switchTemp(60)

	def findTemp(self, temp):
		regexp = '((\d*[.])?\d+)(°C  \()'
		rg = re.compile(regexp)
		m = rg.search(temp)
		if m:
			result = m.group(1)
			return float(str(result))
		else:
			return False;

	def switchTemp(self, temp):
		if self.debugmode == True:
			self.writeToLog(str(temp), "CURRENTTEMP")
			self.writeToLog(str(self.fanperiod), "LASTHIPERIOD")
		if self.fanperiod > 0:
			self.fanperiod = self.fanperiod - 1
			return True
		if temp >= self.config['HIGH']:
			self.fanspeed = 2
			self.fanperiod = 7
		elif temp >= self.config['MED']:
			self.fanspeed = 1
		elif temp <= self.config['LOW']:
			lowtemp = self.config['LOW'] - 15.0
			if temp < lowtemp:
				self.fanspeed = 0
			else:
				self.fanspeed = 1
		else:
			self.fanspeed = 1
		self.changeFanSpeed(self.fanspeed)
		return True
		

	def changeFanSpeed(self, speed):
		if self.debugmode == True:
			self.writeToLog(str(speed), "SETFANSPEED")
		call(["i8kfan", "-v", "-r", str(int(speed))], stdout=open(devnull, 'wb'))

	def writeToLog(self, data, level):
		try:
			log = open('/var/log/vstemplog/vstemp', 'a')
			data = "[" + level + "]\t\t" + datetime.now().strftime("%Y-%m-%d %H:%I:%S") + " - " + str(data) + "\n"
			log.write(data)
			del data
			log.close()
			return True
		except:
			return False
		


