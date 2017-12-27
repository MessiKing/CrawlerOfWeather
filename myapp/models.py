#encoding=utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Taqiinfo(models.Model):
    cityid = models.IntegerField(db_column='CityID', primary_key=True)  # Field name made lowercase.
    weatherdate = models.DateField(db_column='WeatherDate')  # Field name made lowercase.
    updatedt = models.DateTimeField(db_column='UpdateDT', blank=True, null=True)  # Field name made lowercase.
    aqi = models.IntegerField(db_column='AQI', blank=True, null=True)  # Field name made lowercase.
    pm10 = models.IntegerField(db_column='PM10', blank=True, null=True)  # Field name made lowercase.
    pm25 = models.IntegerField(db_column='PM25', blank=True, null=True)  # Field name made lowercase.
    no2 = models.IntegerField(db_column='NO2', blank=True, null=True)  # Field name made lowercase.
    so2 = models.IntegerField(db_column='SO2', blank=True, null=True)  # Field name made lowercase.
    co = models.FloatField(db_column='CO', blank=True, null=True)  # Field name made lowercase.
    o3 = models.IntegerField(db_column='O3', blank=True, null=True)  # Field name made lowercase.
    #id = models.IntegerField(primary_key=True)

    def toDict(self, arg):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)

		d = {}
		for attr in fields:
			#微信端不发送无用信息
			if arg == 'WX':
				if attr == 'cityid' or attr == 'weatherdate' or attr == 'updatedt':
					continue;
			#数据格式转换
			d[attr] = getattr(self, attr)
			if attr == 'weatherdate':
				d[attr] = ("%s"%(d[attr]))
				d[attr] = d[attr].replace('-', '')
			if attr == 'updatedt':
				d[attr] = ("%s"%(d[attr]))
				d[attr] = d[attr].replace('-', '').replace(':', '').replace(' ', '')[0:14]
		
		return d

    def toJSON(self, arg):
		import json
		dictData = self.toDict(arg)
		return json.dumps(dictData)
    
    class Meta:
        managed = False
        db_table = 'TAQIInfo'
        #unique_together = (('cityid', 'weatherdate'),)
	

class Tcitybaseinfo(models.Model):
    cityid = models.IntegerField(db_column='CityID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)  # Field name made lowercase.
    alphacode = models.CharField(db_column='AlphaCode', max_length=80, blank=True, null=True)  # Field name made lowercase.
    provincecode = models.CharField(db_column='ProvinceCode', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toDict(self):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)

		d = {}
		for attr in fields:
			d[attr] = getattr(self, attr)

		return d

    def toJSON(self):
		import json
		dictData = self.toDict()
		return json.dumps(dictData)

    class Meta:
        managed = False
        db_table = 'TCityBaseInfo'


class Tdayweather(models.Model):
    cityid = models.IntegerField(db_column='CityID', primary_key=True)  # Field name made lowercase.
    weatherdate = models.DateField(db_column='WeatherDate')  # Field name made lowercase.
    updatedt = models.DateTimeField(db_column='UpdateDT', blank=True, null=True)  # Field name made lowercase.
    nowtemp = models.IntegerField(db_column='NowTemp', blank=True, null=True)  # Field name made lowercase.
    maxtemp = models.IntegerField(db_column='MaxTemp', blank=True, null=True)  # Field name made lowercase.
    mintemp = models.IntegerField(db_column='MinTemp', blank=True, null=True)  # Field name made lowercase.
    weather = models.CharField(db_column='Weather', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nowwinddirectionid = models.CharField(db_column='NowWindDirectionID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    startwinddirectionid = models.CharField(db_column='StartWindDirectionID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    endwinddirectionid = models.CharField(db_column='EndWindDirectionID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    windscale = models.CharField(db_column='WindScale', max_length=10, blank=True, null=True)  # Field name made lowercase.
    humidity = models.FloatField(db_column='Humidity', blank=True, null=True)  # Field name made lowercase.
    aqi = models.CharField(db_column='AQI', max_length=20, blank=True, null=True)  # Field name made lowercase.
    #id = models.IntegerField(primary_key=True)
    
    def toDict(self, arg):
		import time
		fields = []
		weekNo = ''
		windName = ''
		for field in self._meta.fields:
			fields.append(field.name)

		d = {}
		for attr in fields:
			#微信端不发送无用信息
			if arg == 'WX':
				if attr == 'cityid' or attr == 'startwinddirectionid' or attr == 'endwinddirectionid':
					continue;
			d[attr] = getattr(self, attr)
			if attr == 'nowwinddirectionid':
				if d[attr] != '':
					length = len(d[attr])
					for no in range(length):
						if d[attr][length - 1 - no] == 'E':
							windName += '东'		
						elif d[attr][length - 1 - no] == 'W':
							windName += '西'		
						elif d[attr][length - 1 - no] == 'S':
							windName += '南'		
						elif d[attr][length - 1 - no] == 'N':
							windName += '北'		
						else:
							windName += d[attr][length - 1 - no]					
					d[attr] = windName + '风'

			elif attr == 'weatherdate':
				d[attr] = ("%s"%(d[attr]))
				#d[attr] = d[attr].replace('-', '')
				convTime = time.strptime(d[attr], '%Y-%m-%d')
				weekNo = int(time.strftime("%w", convTime))
				if weekNo == 0:
        				d[attr] = '周日'
				elif weekNo == 1:
        				d[attr] = '周一'
				elif weekNo == 2:
        				d[attr] = '周三'
				elif weekNo == 3:
        				d[attr] = '周三'
				elif weekNo == 4:
        				d[attr] = '周四'
				elif weekNo == 5:
        				d[attr] = '周五'
				elif weekNo == 6:
        				d[attr] = '周六'
				else:
					d[attr] = d[attr].replace('-', '')
			elif attr == 'updatedt':
				d[attr] = ("%s"%(d[attr]))
				d[attr] = d[attr].replace('-', '').replace(':', '').replace(' ', '')[0:14]
			elif attr == 'humidity':
				d[attr] = ('%f'%(d[attr] * 100))
				d[attr] = d[attr][0:2] + '%'
			

		return d

    def toJSON(self, arg):
		import json
		dictData = self.toDict(arg)
		return json.dumps(dictData)
		

    class Meta:
        managed = False
        db_table = 'TDayWeather'
        #unique_together = (('cityid', 'weatherdate'),)


class Tdetailweather(models.Model):
    cityid = models.IntegerField(db_column='CityID', primary_key=True)  # Field name made lowercase.
    weathertime = models.DateTimeField(db_column='WeatherTime')  # Field name made lowercase.
    temp = models.IntegerField(db_column='Temp', blank=True, null=True)  # Field name made lowercase.
    weather = models.CharField(db_column='Weather', max_length=10, blank=True, null=True)  # Field name made lowercase.
    #id = models.IntegerField(primary_key=True)
    
    def toDict(self, arg):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)

		d = {}
		for attr in fields:
			#微信端不发送无用信息
			if arg == 'WX' and attr == 'cityid':
				continue;
			d[attr] = getattr(self, attr)
			if attr == 'weathertime':
				d[attr] = ("%s"%(d[attr]))
				#d[attr] = d[attr].replace('-', '').replace(':', '').replace(' ', '')[0:14]
				d[attr] = d[attr].replace('-', '').replace(':', '').replace(' ', '')[8:10] + '时'

		return d 
    
    def toJSON(self, arg):
		import json
		dictData = self.toDict(arg)
		return json.dumps(dictData)

    class Meta:
        managed = False
        db_table = 'TDetailWeather'
        #unique_together = (('cityid', 'weathertime'),)


class Tprovincebaseinfo(models.Model):
    name = models.CharField(db_column='Name', max_length=80, blank=True, null=True)  # Field name made lowercase.
    alphacode = models.CharField(db_column='AlphaCode', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TProvinceBaseInfo'


class Twinddirectionbaseinfo(models.Model):
    windid = models.IntegerField(db_column='WindID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=10, blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(db_column='Icon', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TWindDirectionBaseInfo'


class Tupdaterecord(models.Model):
    cityid = models.IntegerField(db_column='CityID', primary_key=True)  # Field name made lowercase.
    lastupdatedt = models.DateTimeField(db_column='LastUpdateDT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TUpdateRecord'

