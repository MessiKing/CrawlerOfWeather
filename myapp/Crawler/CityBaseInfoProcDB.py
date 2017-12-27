#encoding=utf8
####################################
# Author: wangyd
# Date  : 2017/12/11
####################################

from CommonProcDB import CommonProcDB

class CCityBaseInfoProcDB(CommonProcDB):
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
	#查询城市ID
	#---------------------------------
	def SelectCityID(self, name):
		SQL = ("select CityID from TCityBaseInfo where name = '%s' "%(name))
		val = self.selectDB(SQL)
		return val[0][0]
	
	
