#encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import json
from myapp.models import Tdayweather, Taqiinfo, Tdetailweather, Tcitybaseinfo, Tupdaterecord
import time
import sys
sys.path.append('/var/www/Weather/myapp/Crawler')
from main import SyncData
from datetime import datetime
import pytz

# Create your views here.
#-------------------------------------
# 获取AQI信息（对外接口）
#-------------------------------------
def GetTodayAqi(request):
	(id, mark) = GetCityID(request)
	if id == 'NA':
		return ResponseError()

	if len(id) != 9:
		return ResponseError()
	
	number = int(id)

	#更新数据
	UpdateDate(number)
	
	#结果集
	try:
		record = Taqiinfo.objects.get(cityid = number, weatherdate = GetCurrentDateStr())
		listResult = [{'result': 1}]
		listResult.append(record.toDict(mark))
		return HttpResponse(json.dumps(listResult))
	except Taqiinfo.DoesNotExist as e:
		return ResponseError()

#-------------------------------------
# 获取一周天气信息（对外接口）
#-------------------------------------
def GetWeekWeatherInfo(request, retry=2):
	(id, mark) = GetCityID(request)
	if id == 'NA':
		return ResponseError()
	
	if len(id) != 9:
		return ResponseError()
	
	number = int(id)
	
	#更新数据
	UpdateDate(number)
	
	#结果集
	try:
		listRecord = Tdayweather.objects.filter(cityid = number, weatherdate__gte = GetCurrentDateStr()).order_by('weatherdate')[:7]
		listResult = [{'result': len(listRecord)}]
		for record in listRecord:
			dictRecord = record.toDict(mark)
			listResult.append(dictRecord)
		if len(listResult) == 0:
			return ResponseError()
		else:
			return HttpResponse(json.dumps(listResult))
	except Tdayweather.DoesNotExist as e:
		return ResponseError()

#-------------------------------------
# 获取当天详细信息（对外接口）
#-------------------------------------
def GetDetailInfo(request, retry=2):
	(id, mark) = GetCityID(request)
	if id == 'NA':
		return ResponseError()
	
	if len(id) != 9:
		return ResponseError()
	
	number = int(id)
	
	#更新数据
	UpdateDate(number)
	
	#结果集
	try:
        	tz = pytz.timezone('Asia/Shanghai')
        	nowTime = datetime.now(tz)
        	nowTimeStr = nowTime.strftime("%Y-%m-%d %H:%M:%S")
		listRecord = Tdetailweather.objects.filter(cityid = number, weathertime__gte = nowTimeStr).order_by('weathertime')
		listResult = [{'result': len(listRecord)}]
		for record in listRecord:
			dictRecord = record.toDict(mark)
			listResult.append(dictRecord)
		if len(listResult) == 0:
			return ResponseError()
		else:
			return HttpResponse(json.dumps(listResult))
	except Tdetailweather.DoesNotExist as e:
		return ResponseError()
	
#-------------------------------------
# 异常应答
#-------------------------------------
def ResponseError():
	record = [{'result': '0'}]
	return HttpResponse(json.dumps(record))


#-------------------------------------
# 获取ID
#-------------------------------------
def GetCityID(request):
	cityID = request.GET.get('cityid', 'NA')
	cityname = request.GET.get('cityname', 'NA')
	code = request.GET.get('code', 'NA')
	mark = request.GET.get('mark', 'NA')

	result = 'NA'

	#优先使用ID
	if cityID != 'NA':
		try:
			record = Tcitybaseinfo.objects.filter(cityid = int(cityID))[:1]
			result = '%d'%(record[0].cityid)
		except Tcitybaseinfo.DoesNotExist as e:
			result = 'NA'
		except IndexError as e:
			result = 'NA'
		except ValueError as e:
			result = 'NA'
	
	#使用城市名查询城市ID
	elif cityname != 'NA':
		try:
			record = Tcitybaseinfo.objects.filter(name = cityname)[:1]
			result = '%d'%(record[0].cityid)
		except Tcitybaseinfo.DoesNotExist as e:
			result = 'NA'
		except IndexError as e:
			result = 'NA'
	
	#使用拼音查询城市ID
	elif code != 'NA':
		try:
			record = Tcitybaseinfo.objects.filter(alphacode = code)[:1]
			result = '%d'%(record[0].cityid)
		except Tcitybaseinfo.DoesNotExist as e:
			result = 'NA'
		except IndexError as e:
			result = 'NA'
	else:
		result ='NA'

	return (result, mark)


#-------------------------------------
# 更新数据库数据
#-------------------------------------
def UpdateDate(cid):
	try:
		record = Tupdaterecord.objects.get(cityid = cid)
		#检查数据的有效性
		if True == IsUpdate(record.lastupdatedt):
			#print('Update. cityid: %d, updatedt: %s'%(cid, record.lastupdatedt))
				
			#更新最后更新日期
        		tz = pytz.timezone('Asia/Shanghai')
        		nowTime = datetime.now(tz)
        		nowTimeStr = nowTime.strftime("%Y-%m-%d %H:%M:%S")
			record.lastupdatedt = nowTimeStr
			record.save()
				
			#请求更新数据库
			SyncData(cid)
			return 
		else:
			return
	except Tupdaterecord.DoesNotExist as e:
		#print('DoesNotExist. cityid: %d'%(cid))
		#更新最后更新日期
        	tz = pytz.timezone('Asia/Shanghai')
        	nowTime = datetime.now(tz)
        	nowTimeStr = nowTime.strftime("%Y-%m-%d %H:%M:%S")
		obj = Tupdaterecord(cityid = cid, lastupdatedt = nowTimeStr)
		obj.save()
			
		#请求更新数据库
		SyncData(cid)
		return 

#-------------------------------------
# 获取当前时间
#-------------------------------------
def GetCurrentTimeStr():
        tz = pytz.timezone('Asia/Shanghai')
        nowTime = datetime.now(tz)
        nowTimeStr = nowTime.strftime("%Y%m%d%H%M%S")
	#print(nowTimeStr)
        return nowTimeStr

#-------------------------------------
# 获取当前日期
#-------------------------------------
def GetCurrentDateStr():
        tz = pytz.timezone('Asia/Shanghai')
        nowDate = datetime.now(tz)
        nowDateStr = nowDate.strftime("%Y-%m-%d")
        return nowDateStr

#-------------------------------------
# 判断是否更新
#-------------------------------------
def IsUpdate(updatedt):
	#datetime类型转字符串
	strUpdate = ("%s"%(updatedt))
	strUpdate = strUpdate.replace('-', '').replace(':', '').replace(' ', '')[0:14]
	
	#转long型进行数据比较
	oldDate = long(strUpdate)
	if oldDate == 0L:
		return True
	
	nowDate = long(GetCurrentTimeStr())
	#print('nowDate: %d, oldDate: %d'%(nowDate, oldDate))
	#半个小时允许更新一次
	if nowDate - oldDate > 3000L:
		return True
	else:
		return False

