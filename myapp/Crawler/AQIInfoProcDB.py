#encoding=utf8
####################################
# Author: wangyd
# Date  : 2017/12/11
####################################

from CommonProcDB import CommonProcDB

class CAQIInfoProcDB(CommonProcDB):
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
	#更新一天AQI详细信息
	#---------------------------------
	def updatedayAQIInfo(self, dayAQIInfo):
		self.insertAQIInfo(dayAQIInfo)
	
	#---------------------------------
	#插入一天AQI数据
	#---------------------------------
	def insertAQIInfo(self, dayAQIInfo):
		#转换日期
		srcWDate = dayAQIInfo['weatherDate']
		dstWDate = ('%s-%s-%s'%(srcWDate[0:4], srcWDate[4:6], srcWDate[6:]))
		#转换更新时间
		srcUTime = dayAQIInfo['updateDT']
		dstUTime = ('%s-%s-%s %s:%s:00'%(srcUTime[0:4], srcUTime[4:6], srcUTime[6:8], srcUTime[8:10], srcUTime[10:]))
		
		SQL = ("select count(*) from TAQIInfo where CityID = %d and WeatherDate = '%s'" %(int(dayAQIInfo['cityID']), dstWDate))
		val = self.selectDB(SQL)
		if val[0][0] != 0 :
			#删除老数据
			SQL = ("delete from TAQIInfo where CityID = %d and WeatherDate = '%s'" %(int(dayAQIInfo['cityID']), dstWDate))
			self.updateDB(SQL)
		#插入数据
		SQL = ("insert into TAQIInfo(CityID, WeatherDate, UpdateDT, AQI, PM10, PM25, NO2, SO2, CO, O3) \
				values(%d, '%s', '%s', %d, %d, %d, %d, %d, %f, %d)"%(int(dayAQIInfo['cityID']), dstWDate, 
				dstUTime, int(dayAQIInfo['aqi']), int(dayAQIInfo['pm10']), int(dayAQIInfo['pm25']), int(dayAQIInfo['no2']), 
				int(dayAQIInfo['so2']), float(dayAQIInfo['co']), int(dayAQIInfo['o3'])))
		self.updateDBWithCommit(SQL)
		
		