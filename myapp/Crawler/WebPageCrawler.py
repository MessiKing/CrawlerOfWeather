#encoding=utf-8
####################################
# Author: wangyd
# Date  : 2017/12/06
####################################
import re
import urllib2
import logging
import logging.config

LogWriter = logging.getLogger('main.mod')

#---------------------------------
#获取html
#---------------------------------
class CWebPageCrawler:
	#---------------------------------
	# 构造函数
	#---------------------------------
	def __init__(self):
		self.url=''

	#---------------------------------
	# 根据url获取结果
	#---------------------------------
	def GetWebPageFromServer(self, url, header_args = None, retry_count=2):
		try:
			self.url = url
			if header_args == None:
				LogWriter.debug('request url: %s'%(self.url))
				request = urllib2.Request(self.url)
			else:
				LogWriter.debug('request url: %s, headers: %s'%(self.url, header_args))
				request = urllib2.Request(self.url, headers=header_args)
			response = urllib2.urlopen(request)
			result = response.read()
			#LogWriter.debug("Respose: %s"%(result))

		except urllib2.URLError as e:
			result = None
			if retry_count > 0:
				if hasattr(e, 'code') and 500 <= e.code < 600:
					# retry 5XX HTTP errors
					return self.GetHtmlFromServer(self.url, retry_count - 1)
			else:
				LogWriter.warning('Request url(%s) failure.'%(self.url))
		return result
		
	#---------------------------------
	# 获取json结果
	#---------------------------------	
	def GetJsonDataFromServer(self, url, header_args):
		result = self.GetWebPageFromServer(url, header_args)
		return result
		
	#---------------------------------
	# 获取html页面结果
	#---------------------------------
	def GetHtmlFromServer(self, url):
		html = self.GetWebPageFromServer(url)
		return html



