import sqlite3 as sql
from helperfunctions import functions

class sqlwrapper():

	"""
	class that provides an interface to query the database
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
		"""
		set the database path using this function
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

	# def __updatemetadata(self):
	def __configuration_required(f):
		def isconfigured(self,*args,**kwargs):
			"""
			checks if database path have been set
			"""
			if(self.__cur == None):
				return "please set the databasepath using configure() method"
			

			return f(self,*args,**kwargs)
		return isconfigured 

	@__configuration_required
	def fetch_all(self,tablename):
		
		""" 
		fetches all the data from a given table 
		example: db.fetch_all('users')
		return_type: returns list of dictionaries (i.e the whole table)
		"""
		# if(self.__isconfigured()):
			# return "please set a database path using configure() method"
	   	
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
		"""
		fetches the first data from the table
		example: db.fetch_first('users')
		return_type: single dictionary (i.e row)
		"""
		# if(!self.__isconfigured()):
			# return "please set a database path using configure() method"
		
		query = 'select * from '+tablename+" ASC LIMIT 1"
		try:
			self.__cur.execute(query)
		except Exception as e:
			return "could not execute query, some error occured please try again, error was: "+str(e)
		fetcheddata = self.__cur.fetchall()
		fetcheddata = self.__helper.rowtodict(fetcheddata)
		return fetcheddata[0]

	@__configuration_required
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
		""" fetches data from the database with where condition
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
	def insert(self,tablename,columns=None,values=None):
		#inserts data into a table
		#val=','.join(values)
		length=len(columns)
		if length!=0:
			placeholder=['?']*length
			query="Insert into "+tablename+" ("+','.join(columns)+") Values ("+','.join(placeholder)+")"
		else:
			self.__cur=self.__conn.execute('select * from '+tablename)
			names = list(map(lambda x: x[0], self.__cur.description))
			l=len(names)
			placeholder=['?']*l
			query="Insert into "+tablename+" Values ("+','.join(placeholder)+")"
		try:
			self.__cur.execute(query,values)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			return "could not execute query, some error occured please try again, error was: "+str(e)

