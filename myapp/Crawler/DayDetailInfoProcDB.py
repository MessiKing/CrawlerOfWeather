#encoding=utf8
####################################
# Author: wangyd
# Date  : 2017/12/11
####################################

from CommonProcDB import CommonProcDB

class CDayDetailInfoProcDB(CommonProcDB):
	#---------------------------------
	#构造函数(sqlite)
	#---------------------------------
	def __init__(self, dbname):
		CommonProcDB.__init__(self, dbname)
			
	#---------------------------------
	#构造函数(mysql)
	#---------------------------------
	def __init__(self, dbuser, dbpasswd, dbname):
		CommonProcDB.__init__(self, dbuser, dbpasswd, dbname)
	
	#---------------------------------
	#更新一天天气信息
	#---------------------------------
	def updateHourDetailWeather(self, hourWeather):
		self.insertDetailWeather(hourWeather)
	
	#---------------------------------
	#插入一天的数据
	#---------------------------------
	def insertDetailWeather(self, hourWeather):
		srcDateStr = hourWeather['weatherTime']
		dstDateStr = ('%s-%s-%s %s:%s:00'%(srcDateStr[0:4], srcDateStr[4:6], srcDateStr[6:8], srcDateStr[8:10], srcDateStr[10:]))
		SQL = ("select count(*) from TDetailWeather where CityID = %d and WeatherTime = '%s'" %(int(hourWeather['cityID']), dstDateStr))
		val = self.selectDB(SQL)
		if val[0][0] != 0 :
			#删除老数据
			SQL = ("delete from TDetailWeather where CityID = %d and WeatherTime = '%s'" %(int(hourWeather['cityID']), dstDateStr))
			self.updateDB(SQL)
		#插入数据
		SQL = ("insert into TDetailWeather(CityID, WeatherTime, Temp, Weather) \
				values(%d, '%s', %d, '%s')"%(int(hourWeather['cityID']), dstDateStr, 
				int(hourWeather['temp']), hourWeather['weather'].encode('utf8')))
		self.updateDBWithCommit(SQL)
	
	#---------------------------------
	#批量插入数据
	#---------------------------------
	def updateDayDetailWeather(self, hour72Weather):
		for record in hour72Weather:
			dict = record
			self.updateHourDetailWeather(dict)

	