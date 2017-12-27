#encoding=utf8
####################################
# Author: wangyd
# Date  : 2017/12/06
# 72小时内数据
####################################
import logging
import logging.config
import datetime
import time

LogWriter = logging.getLogger('main.mod')

class CDayDetailInfoParser():
	#---------------------------------
	#构造函数
	#---------------------------------
	def __init__(self, cityid):
		self.cityID = cityid
		self.dicRecord = {}
		self.listHour72Weather = []
		#字典键值
		'''
		cityID, weatherTime, temp, weather
		'''
		#截取数据标志
		self.start_flag = 'var fc1h_24 ='
		self.end_flag = ';'
	
	#---------------------------------
	#从Json数据中获取数据
	#---------------------------------
	def JsonDataParser(self, source_data):
		#查找对应的数据段
		start_index = source_data.index(self.start_flag) + len(self.start_flag)
		end_index = source_data.find(self.end_flag, start_index)
		if int(end_index) == -1:
			end_index = len(source_data)
		target = source_data[start_index:end_index]
		#LogWriter.debug(target)
		#字符串型数据传容器型数据
		tmp = eval(target)
		#LogWriter.debug(tmp)
		source_list = tmp['jh']
		#取数据
		for record in source_list:
			dicRecord = {}
			dicRecord['cityID'] = self.cityID
			dicRecord['weatherTime'] = record['jf']
			dicRecord['temp'] = record['jb']
			dicRecord['weather'] = self.convertIcon(record['ja'], record['jf'])
			self.listHour72Weather.append(dicRecord)
		return self.listHour72Weather
	
	#---------------------------------
	#得到对应的URL和headers参数
	#---------------------------------
	def GetURL(self):
		t = time.time()
		url='http://d1.weather.com.cn/wap_40d/%d.html?_=%d'%(self.cityID, int(round(t * 1000)))
		headers={
		'Referer': 'http://m.weather.com.cn/mweather/%d.shtml'%(self.cityID),}
		return (url, headers)
		
	#---------------------------------
	#将天气图标转换成对应的图标
	#---------------------------------
	def convertIcon(self, src_code, time):
		#白天/晚上
		hour = int(time[8:10])
		icon_hour = '_0'
		if hour > 19 or hour < 5:
			icon_hour = '_1'
		else:
			icon_hour = '_0'
		
		#天气图标
		return ('%s%s'%(src_code, icon_hour))
		
	
