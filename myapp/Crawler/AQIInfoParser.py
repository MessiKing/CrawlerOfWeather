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

class CAQIInfoParser():
	#---------------------------------
	#构造函数
	#---------------------------------
	def __init__(self, cityid):
		self.cityID = cityid
		self.dicRecord = {}
		#字典键值
		'''
		cityID, weatherDate, updateDT, aqi, pm10, pm25, no2, so2, co, o3
		'''
		#截取数据标志
		self.start_flag = 'var aqi='
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
		LogWriter.debug(target)
		#字符串型数据传容器型数据
		tmp = eval(target)
		LogWriter.debug(tmp)
		source_dict = tmp['p']
		#取数据
		self.dicRecord['cityID'] = self.cityID
		self.dicRecord['weatherDate'] = source_dict['p9'][0:8]
		self.dicRecord['updateDT'] = source_dict['p9']
		self.dicRecord['aqi'] = source_dict['p2']
		self.dicRecord['pm10'] = source_dict['p5']
		self.dicRecord['pm25'] = source_dict['p1']
		self.dicRecord['no2'] = source_dict['p3']
		self.dicRecord['so2'] = source_dict['p6']
		self.dicRecord['co'] = source_dict['p7']
		self.dicRecord['o3'] = source_dict['p4']
		return self.dicRecord
	
	#---------------------------------
	#得到对应的URL和headers参数
	#---------------------------------
	def GetURL(self):
		t = time.time()
		url='http://d1.weather.com.cn/aqi_mobile/%d.html?_=%d'%(self.cityID, int(round(t * 1000)))
		headers={
		'Referer': 'http://m.weather.com.cn/maqi/%d.shtml'%(self.cityID),}
		return (url, headers)
		
	
