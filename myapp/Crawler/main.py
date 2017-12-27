#encoding=utf8
####################################
# Author: wangyd
# Date  : 2017/12/06
####################################
import urllib2
import logging
import logging.config
from DayDetailInfoParser import CDayDetailInfoParser
from DayWeatherParser import CDayWeatherParser
from WebPageCrawler import CWebPageCrawler
from AQIInfoParser import CAQIInfoParser
from DayDetailInfoProcDB import CDayDetailInfoProcDB
from CityBaseInfoProcDB import CCityBaseInfoProcDB
from DayWeatherProcDB import CDayWeatherProcDB
from AQIInfoProcDB import CAQIInfoProcDB

logging.config.fileConfig('/var/www/Weather/myapp/Crawler/log.conf')
LogWriter = logging.getLogger('main')

#---------------------------------
# main
#---------------------------------
def SyncData(cityID):
	LogWriter.info('Start Data Sync. city id: %d'%(cityID));	

	#初始化
	dbUser = 'weather'
	dbPassword = 'weather'
	dbName = 'weatherDB3'
	items = []
	
	#从网络获取数据
	crawler = CWebPageCrawler()
	
	#(1)解析当天72小时分时数据
	 #---数据爬取
	detailInfoParser = CDayDetailInfoParser(cityID)
	(url, headers) = detailInfoParser.GetURL()
	json_data = crawler.GetJsonDataFromServer(url, headers)
	if json_data != None:
		items = detailInfoParser.JsonDataParser(json_data)
		LogWriter.debug(items)
	 #---数据插入
	detailInfoProcDB = CDayDetailInfoProcDB(dbUser, dbPassword, dbName)
	detailInfoProcDB.updateDayDetailWeather(items)
	detailInfoProcDB.closeDB()

	#(2)解析当天以后10天基本信息
	weekWeatherParser = CDayWeatherParser(cityID)
	 #--40天数据
	weekWeatherParser.JsonData40DayParser(json_data)
	 #--5天内数据
	 
	 #--当天数据
	(url, headers) = weekWeatherParser.GetURL(1)
	json_data = crawler.GetJsonDataFromServer(url, headers)
	if json_data != None:
		items = weekWeatherParser.JsonData1DayParser(json_data)
		LogWriter.debug(items)
	 
	 #--数据插入
	weekWeatherProcDB = CDayWeatherProcDB(dbUser, dbPassword, dbName)
	weekWeatherProcDB.updateWeekWeather(items)
	weekWeatherProcDB.closeDB()
	
	#(3)解析当天AQI详细信息
	 #--数据爬取
	aqiInfoParser = CAQIInfoParser(cityID)
	(url, headers) = aqiInfoParser.GetURL()
	json_data = crawler.GetJsonDataFromServer(url, headers)
	if json_data != None:
		items = aqiInfoParser.JsonDataParser(json_data)
		LogWriter.debug(items)
		
	 #--数据插入
	aqiInfoProcDB = CAQIInfoProcDB(dbUser, dbPassword, dbName)
	aqiInfoProcDB.updatedayAQIInfo(items)
	aqiInfoProcDB.closeDB()

#---------------------------------
# 启动
#---------------------------------
#if __name__ == "__main__":
#	LogWriter.info('==========Start Application==========')
#	
#	cityName = '郑州'
#
#	#查询城市ID
#	cityBaseInfo = CCityBaseInfoProcDB('weather', 'weather', 'weatherDB')
#	cityID = cityBaseInfo.SelectCityID(cityName)
#	LogWriter.debug(cityID)
#	
#
#	SyncData(cityID)


