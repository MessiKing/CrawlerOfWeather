#encoding=utf8
####################################
# Author: wangyd
# Date  : 2017/12/06
# 一周内的数据
####################################
import logging
import logging.config
import time

LogWriter = logging.getLogger('main.mod')

class CDayWeatherParser():
	#---------------------------------
	#构造函数
	#---------------------------------
	def __init__(self, cityid):
		self.cityID = cityid
		self.dicRecord = {}
		self.listWeakWeather = []
		self.initData()
		#字典键值
		'''
		cityID, weatherDate, updateDT, nowTemp, maxTemp, minTemp
		weather, nowWindID, startWindID, endWindID, windScale, 
		humidity, aqi
		'''
	
	#---------------------------------
	#从Json数据中获取数据(40天内数据)
	#---------------------------------
	def JsonData40DayParser(self, source_data):
		start_flag = 'var fc40='
		end_flag = ';'
		#查找对应的数据段
		start_index = source_data.index(start_flag) + len(start_flag)
		end_index = source_data.find(end_flag, start_index)
		if int(end_index) == -1:
			end_index = len(source_data)
		target = source_data[start_index:end_index]
		#LogWriter.debug(target)
		#字符串型数据传容器型数据
		tmp = eval(target)
		#LogWriter.debug(tmp)
		source_list = tmp
		#取数据
		count = 0
		for record in source_list:
			self.listWeakWeather[count]['cityID'] = self.cityID
			self.listWeakWeather[count]['weatherDate'] = record['009']
			self.listWeakWeather[count]['maxTemp'] = record['003']
			self.listWeakWeather[count]['minTemp'] = record['004']
			self.listWeakWeather[count]['weather'] = ('%s_0'%(record['002']))
			self.listWeakWeather[count]['aqi'] = record['011']
			count += 1
			if count == 10:
				break
		return self.listWeakWeather
	
	#---------------------------------
	#从Json数据中获取数据(5天内数据)
	#---------------------------------
	def JsonData5DayParser(self, source_data):
		start_flag = 'var json='
		end_flag = ';'
		#查找对应的数据段
		start_index = source_data.index(start_flag) + len(start_flag)
		end_index = source_data.find(end_flag, start_index)
		if int(end_index) == -1:
			end_index = len(source_data)
		target = source_data[start_index:end_index]
		#LogWriter.debug(target)
		#字符串型数据传容器型数据
		tmp = eval(target)
		#LogWriter.debug(tmp)
		source_list = tmp['2001007']
		#取数据
		count = 0
		#暂时不取
		
	#---------------------------------
	#从Json数据中获取数据(当天详细数据)
	#---------------------------------
	def JsonData1DayParser(self, source_data):
		start_flag = 'var dataSK ='
		end_flag = '----'
		#查找对应的数据段
		start_index = source_data.index(start_flag) + len(start_flag)
		end_index = source_data.find(end_flag, start_index)
		if int(end_index) == -1:
			end_index = len(source_data)
		target = source_data[start_index:end_index]
		#LogWriter.debug(target)
		#字符串型数据传容器型数据
		tmp = eval(target)
		#LogWriter.debug(tmp)
		source_dict = tmp
		self.listWeakWeather[0]['cityID'] = self.cityID
		self.listWeakWeather[0]['updateDT'] = ('%s %s'%(self.listWeakWeather[0]['weatherDate'], source_dict['time']))
		self.listWeakWeather[0]['nowTemp'] = source_dict['temp']
		self.listWeakWeather[0]['weather'] = self.convertIcon(source_dict['weathercode'], source_dict['time'])
		self.listWeakWeather[0]['nowWindID'] = source_dict['wde'].rstrip()
		self.listWeakWeather[0]['windScale'] = source_dict['WS'][0:1]
		self.listWeakWeather[0]['humidity'] = source_dict['sd']
		self.listWeakWeather[0]['aqi'] = source_dict['aqi']
		return self.listWeakWeather
		
	#---------------------------------
	#初始化数据结构（最多存储10天的数据）
	#---------------------------------
	def initData(self):
		for index in range(0, 10):
			dicRecord = {}
			dicRecord['cityID'] = self.cityID 
			dicRecord['weatherDate'] = '' 
			dicRecord['updateDT'] = '' 
			dicRecord['nowTemp'] = '0' 
			dicRecord['maxTemp'] = '0' 
			dicRecord['minTemp'] = '0'
			dicRecord['weather'] = '' 
			dicRecord['nowWindID'] = '' 
			dicRecord['startWindID'] = '' 
			dicRecord['endWindID'] = '' 
			dicRecord['windScale'] = '' 
			dicRecord['humidity'] = '0%' 
			dicRecord['aqi'] = '0'
			self.listWeakWeather.append(dicRecord)
	
	#---------------------------------
	#得到对应的URL和headers参数
	#---------------------------------
	def GetURL(self, day):
		t = time.time()
		timestamp = int(round(t * 1000))
		if day == 40:
			url='http://d1.weather.com.cn/wap_40d/%d.html?_=%d'%(self.cityID, timestamp)
		elif day == 5:
			url='http://d1.weather.com.cn/aqi_7d/XiangJiAqiFc5d/%d.html?_=%d'%(self.cityID, timestamp)
		else:
			url='http://d1.weather.com.cn/sk_2d/%d.html?_=%d'%(self.cityID, timestamp)
		headers={
		'Referer': 'http://m.weather.com.cn/mweather/%d.shtml'%(self.cityID),}
		return (url, headers)
		
	#---------------------------------
	#将天气图标转换成对应的图标
	#---------------------------------
	def convertIcon(self, src_code, time):
		#白天/晚上
		hour = int(time[0:2])
		icon_hour = '_0'
		if hour > 19 or hour < 5:
			icon_hour = '_1'
		else:
			icon_hour = '_0'
		
		#天气图标
		return ('%s%s'%(src_code[1:], icon_hour))
		
	
