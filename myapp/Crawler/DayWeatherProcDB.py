#encoding=utf8
####################################
# Author: wangyd
# Date  : 2017/12/11
####################################

from CommonProcDB import CommonProcDB

class CDayWeatherProcDB(CommonProcDB):
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
	def updateDayWeather(self, dayWeather):
		self.insertCityWeather(dayWeather)
	
	#---------------------------------
	#插入一天的数据
	#---------------------------------
	def insertCityWeather(self, dayWeather):
		#转换日期
		srcWDate = dayWeather['weatherDate']
		dstWDate = ('%s-%s-%s'%(srcWDate[0:4], srcWDate[4:6], srcWDate[6:]))
		#转换更新时间
		srcUTime = dayWeather['updateDT']
		dstUTime = ('%s-%s-%s %s:00'%(srcUTime[0:4], srcUTime[4:6], srcUTime[6:8], srcUTime[9:]))
		#转换湿度值
		strSD = ('0.%s'%(dayWeather['humidity'].replace('%', '')))
	
		SQL = ("select count(*) from TDayWeather where CityID = %d and WeatherDate = '%s'" %(int(dayWeather['cityID']), dstWDate))
		val = self.selectDB(SQL)
		if val[0][0] != 0 :
			#删除老数据
			SQL = ("delete from TDayWeather where CityID = %d and WeatherDate = '%s'" %(int(dayWeather['cityID']), dstWDate))
			self.updateDB(SQL)
		#插入数据
		SQL = ("insert into TDayWeather(CityID, WeatherDate, UpdateDT, NowTemp, MaxTemp, MinTemp, Weather, NowWindDirectionID, StartWindDirectionID, \
				EndWindDirectionID, WindScale, Humidity, AQI) values(%d, '%s', '%s', %d, %d, %d, '%s', '%s', '%s', '%s', '%s', %f, '%s')"%(int(dayWeather['cityID']), 
				dstWDate, dstUTime, int(dayWeather['nowTemp']), int(dayWeather['maxTemp']), int(dayWeather['minTemp']),
				dayWeather['weather'].encode('utf8'), dayWeather['nowWindID'], dayWeather['startWindID'], 
				dayWeather['endWindID'], dayWeather['windScale'].encode('utf8'), float(strSD), 
				dayWeather['aqi'].encode('utf8')))
		self.updateDBWithCommit(SQL)
	
	#---------------------------------
	#批量插入数据
	#---------------------------------
	def updateWeekWeather(self, weekWeather):
		for record in weekWeather:
			dict = record
			self.updateDayWeather(dict)

	