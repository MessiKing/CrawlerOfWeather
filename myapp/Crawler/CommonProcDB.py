#encoding=utf8
####################################
# Author: wangyd
# Date  : 2017/12/06
# 数据库基本操作
####################################
import sqlite3
import logging
import logging.config
import mysql.connector

LogWriter = logging.getLogger('main.mod')

class CommonProcDB():
	#---------------------------------
	#构造函数1(sqlite)
	#---------------------------------
	def __init__(self, dbname):
		self.dbname = dbname
		self.cursor = ''
		self.conn = ''
		self.openDBSQLite()
		
	#---------------------------------
	#构造函数2(mysql)
	#---------------------------------
	def __init__(self, user, passwd, name):
		self.dbname = name
		self.dbuser = user
		self.dbpasswd = passwd
		self.openDBMySQL()

	#---------------------------------
	#打开数据库(mysql)
	#---------------------------------
	def openDBMySQL(self):
		self.conn = mysql.connector.connect(user=self.dbuser, password=self.dbpasswd, database=self.dbname)
		self.cursor = self.conn.cursor()

	#---------------------------------
	#打开数据库(sqlite)
	#---------------------------------
	def openDBSQLite(self):
		self.conn = sqlite3.connect(self.dbname)
		self.cursor = self.conn.cursor()
		
	#---------------------------------
	#关闭数据库
	#---------------------------------
	def closeDB(self):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()
		
	#---------------------------------
	#执行更新操作(不提交)
	#---------------------------------
	def updateDB(self, SQL):
		LogWriter.info(SQL)
		self.cursor.execute(SQL)
		self.conn.commit()
	
	#---------------------------------
	#执行更新操作(提交)
	#---------------------------------
	def updateDBWithCommit(self, SQL):
		LogWriter.debug(SQL)
		self.cursor.execute(SQL)
		self.conn.commit()
	
	#---------------------------------
	#执行查询操作
	#---------------------------------
	def selectDB(self, SQL):
		LogWriter.debug(SQL)
		self.cursor.execute(SQL)
		return self.cursor.fetchall()
		
	
	
