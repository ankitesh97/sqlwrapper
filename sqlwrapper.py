import sqlite3 as sql
from helperfunctions import functions
from functools import wraps

class sqlwrapper():

	"""class that provides an interface to query the database
	use: 
	from sqlwrapper import sqlwrapper
	db = sqlwrapper()
	"""

	def __init__(self):
		self.__databasepath = None
		self.__datatbaseaname = None
		self.__metadata = []
		self.__conn = None
		self.__cur = None
		self.__helper = functions()


	def configure(self,databasepath):
		"""set the database path using this function
		example: db.configure('/path/to/your/database.sqlite')
		"""
		self.__databasepath = databasepath
		try:
			self.__conn = sql.connect(self.__databasepath)
		except Exception as e:
			return "could not connect with the database, some error occured the error was: "+str(e)
		self.__datatbaseaname = databasepath.split('/')[-1]
		self.__conn.row_factory = sql.Row
   		self.__cur = self.__conn.cursor()

	def __configuration_required(f):
		@wraps(f)
		def isconfigured(self,*args,**kwargs):
			# checks if database path have been set
			
			if(self.__cur == None):
				return "please set the database path using configure() method"
			

			return f(self,*args,**kwargs)
		return isconfigured 

	@__configuration_required
	def fetch_all(self,tablename):
		
		"""fetches all the data from a given table 
		example: db.fetch_all('users')
		return_type: returns list of dictionaries (i.e the whole table)
		"""
	   	
		query = 'select * from '+tablename		
		try:
			self.__cur.execute(query)
		except Exception as e:
			return "could not execute query, some error occured please try again, error was: "+str(e)
	   	fetcheddata = self.__cur.fetchall()  #data type of fetchall is list of rows object
		fetcheddata = self.__helper._functions__rowtodict(fetcheddata)
		return fetcheddata


	@__configuration_required
	def fetch_first(self,tablename):
		"""fetches the first data from the table
		example: db.fetch_first('users')
		return_type: single dictionary (i.e row)
		"""
		
		query = 'select * from '+tablename+" ASC LIMIT 1"
		try:
			self.__cur.execute(query)
		except Exception as e:
			return "could not execute query, some error occured please try again, error was: "+str(e)
		fetcheddata = self.__cur.fetchall()
		fetcheddata = self.__helper._functions__rowtodict(fetcheddata)
		return fetcheddata[0]

	def fetch_last(self,tablename):
		"""
		   fetches the last data from the table
        example: db.fetch_last('users')
		return_type: single dictionary (i.e row)
		"""

		temp = self.fetch_all(tablename)
		if(type(temp) == str):
			return temp
		return temp[-1]

	@__configuration_required
	def fetch_where(self,tablename,where=None):
		""" fetches data from a given table with where condition
		example: db.fetch_where('users','id >= 4')
		returns: list of dictionaries that satisfies the where clause
		"""

		if where is None:
			return self.fetch_all(tablename)
		if type(where) != str:
			return "please provide a valid where clause"

		query = 'select * from ' + tablename + ' where ' + where

		try:
			self.__cur.execute(query)
		except Exception as e:
			return "could not execute query, some error occured please try again, error was: "+str(e)

		fetcheddata = self.__cur.fetchall()
		fetcheddata = self.__helper._functions__rowtodict(fetcheddata)
		return fetcheddata

	@__configuration_required
	def delete(self,tablename,where=None):
		"""deletes data from a given table provided a where condition that identifies
	    the row to delete.
	    usage:
	    db.delete('users',"name = 'ankitesh' or id = 4") 
		"""
		if where is None:
			return "please provide a where clause which identifies the row to delete"
		if type(where) != str:
			return "please provide a valid where clause"

		query = 'delete from '+ tablename + ' where ' + where

		try:
			self.__cur.execute(query)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			return "could not delete from the table, some error occured the error was: "+str(e)

	@__configuration_required
	def delete_all_from(self,tablename):

		"""deletes all data from a given table
		usage:
		db.delete('users')
		"""
		query = 'delete from ' + tablename
		try:
			self.__cur.execute(query)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			return "could not delete from the table, some error occured the error was: "+str(e)

