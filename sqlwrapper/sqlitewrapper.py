import sqlite3 as sql
from helperfunctions import functions
from Errors import *
from functools import wraps
import hashlib




class sqlitewrapper():

	"""class that provides an interface to query the database
	use: 
	from sqlwrapper import sqlitewrapper
	db = sqlitewrapper()
	"""

	def __init__(self):
		self.__databasepath = None
		self.__datatbasename = None
		self.__metadata = {}
		self.__conn = None
		self.__cur = None
		self.__helper = functions()
		self.__isroot = 0
		self.__rootpwd = None

############################################################################################
######################################## wrappers ##########################################
############################################################################################
	
	def __configuration_required(f):
		@wraps(f)
		def isconfigured(self,*args,**kwargs):
			# checks if database path have been set
			
			if(self.__cur == None):
				raise PathNotSetError("please set the database path using db.config() method")
			

			return f(self,*args,**kwargs)
		return isconfigured

	def __login_required(f):
		@wraps(f)
		def isroot(self,*args,**kwargs):
			#checks if the user is logged in
			if(self.__rootpwd == None):
				raise SetPasswordError("please set a session password using db.set_session_password(pwd) method")
			if(self.__isroot == 0):
				raise ValidationError("please call db.login(pwd) to login to a session")
			else:
				return f(self,*args,**kwargs)
		return isroot



############################################################################################
############################## configuration code ##########################################
############################################################################################

	def connect(self,databasepath):
		"""set the database path using this function

		function definition:
		connect(databasepath)

		example: db.connect('/path/to/your/database.sqlite')
		"""
		self.__databasepath = databasepath
		try:
			self.__conn = sql.connect(self.__databasepath)
		except Exception as e:
			raise e
		self.__datatbasename = databasepath.split('/')[-1]
		self.__metadata["dbname"] = self.__datatbasename
		self.__metadata["dbpath"] = self.__databasepath
		self.__conn.row_factory = sql.Row
   		self.__cur = self.__conn.cursor()


   	def set_session_password(self,pwd):
   		"""set a session password to execute sensitive commands

   		function definition:
   		set_session_password(pwd)

   		usage:
   		db.set_session_password("a_password")
   		"""

   		if(self.__rootpwd == None):
   			self.__rootpwd = hashlib.md5(pwd).hexdigest()
   		else:
   			self.__change_password(pwd)

   	def login(self,pwd):
   		"""login to a session to execute sensitive commands

   		function definition:
   		login(pwd)

   		usage:
   		db.login("password_that_was_set")
   		"""
   		if(self.__isroot == 1):
   			return "User is already logged in"
   		if(self.__rootpwd == None):
   			raise SetPasswordError("please set a session password using db.set_session_password(pwd) method")
   		else:
   			if(self.__rootpwd == hashlib.md5(pwd).hexdigest()):
   				self.__isroot = 1
   				return "successfully logged in"
   			else:
   				raise ValidationError("wrong paswword please try again")
		raise ValidationError("wrong paswword please try again")

   	@__login_required
   	def logout(self):
   		""" logsout the session now no more sesitive commands can be used"""
   		self.__isroot = 0


   	@__login_required
   	def __change_password(self,pwd):
   		# this method is called when user tries to change its paswword
   		self.__rootpwd = hashlib.md5(pwd).hexdigest()
   		return "password successfully changed"


############################################################################################
################################# functional code ##########################################
############################################################################################


	@__configuration_required
	def fetch_all(self,tablename):
		
		"""fetches all the data from a given table

		function definition:
		fetch_all(tablename)

		example: db.fetch_all('users')
		return_type: returns list of dictionaries (i.e the whole table)
		"""
	   	
		query = 'select * from '+tablename		
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
	   	fetcheddata = self.__cur.fetchall()  #data type of fetchall is list of rows object
		if fetcheddata:
			fetcheddata = self.__helper._functions__rowtodict(fetcheddata)
			return fetcheddata
		return None


	@__configuration_required
	def fetch_first(self,tablename):
		"""fetches the first data from the table

		function definition:
		fetch_first(tablename)

		example: db.fetch_first('users')
		return_type: single dictionary (i.e row)
		"""
		
		query = 'select * from '+tablename+" ASC LIMIT 1"
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
		fetcheddata = self.__cur.fetchall()
		if fetcheddata:
			fetcheddata = fetcheddata[0]
			fetcheddata = self.__helper._functions__rowtodict([fetcheddata])
			return fetcheddata[0]
		return None

	def fetch_last(self,tablename):
		"""fetches the last data from the table

		function definition:
		fetch_last(tablename)

        example: db.fetch_last('users')
		return_type: single dictionary (i.e row)
		"""
		query = 'select * from ' + tablename
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
		fetcheddata = self.__cur.fetchall()
		if fetcheddata:
			fetcheddata = fetcheddata[-1]
			fetcheddata = self.__helper._functions.__rowtodict([fetcheddata])
			return fetcheddata[-1]
		return None

	@__configuration_required
	def fetch_where(self,tablename,where):
		""" fetches data from a given table with where condition

		function definition:
		fetch_where(tablename,where)
		type of where clause should be string

		example: db.fetch_where('users','id >= 4')
		returns: list of dictionaries that satisfies the where clause
		"""

		if type(where) != str:
			raise NotAStringError("please provide a valid where clause")

		query = 'select * from ' + tablename + ' where ' + where

		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e

		fetcheddata = self.__cur.fetchall()
		fetcheddata = self.__helper._functions__rowtodict(fetcheddata)
		return fetcheddata

	
	@__configuration_required
	def insert(self,tablename,columns,values):
		"""inserts data in the given tale

		function definition:
		insert(tablename,columns,values)
		columns should be a list containing column names(string)
		values should be a list containing column values

		usage:
		db.insert('users',['id','name'],[1,'saif'])
		db.insert('users',[],[1,'saif']) if there are only two columns in the table
		"""

		length=len(columns)
		if length!=0:
			placeholder=['?']*length
			query="Insert into " +tablename+ " ("+','.join(columns)+") Values ("+','.join(placeholder)+")"
		else:
			l=len(values)
			placeholder=['?']*l
			query="Insert into "+tablename+" Values ("+','.join(placeholder)+")"
		try:
			self.__cur.execute(query,values)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e



	@__configuration_required
	def delete(self,tablename,where):
		"""deletes data from a given table provided a where condition that identifies
	    the row to delete.

	    function definition:
	    delete(tablename,where)
		type of where clause should be string

	    usage:
	    db.delete('users',"name = 'ankitesh' or id = 4") 
		"""
		
		if type(where) != str:
			raise NotAStringError("please provide a valid where clause")

		query = 'delete from '+ tablename + ' where ' + where

		try:
			self.__cur.execute(query)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def delete_all_from(self,tablename):

		"""deletes all data from a given table

		function definition:
		delete_all_from(tablename)

		usage:
		db.delete('users')
		"""
		query = 'delete from ' + tablename
		try:
			self.__cur.execute(query)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e


	@__configuration_required
	@__login_required
	def drop_table(self,tablename):
		"""drops the given table from the database
		requires to be authenticated to execute this command
		function definition:
		drop_table(tablename)

		usage:
		before executing this set the password using set_session_password() method and then login
		drop_table('users')
		"""
		# print "table dropped"
		# return
		query = 'drop table '+tablename
		try:
			self.__cur.execute(query)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e


	@__configuration_required
	def create_table(self,tablename,columns,data_types,primary_key):
		""" creates a table in the database

		function definition:
		create_table(tablename,columns,data_types,primary_key)

		arguments:
		tablename: appropriate tablename (string)
		coulmns = [] array which contains column names (string)
		data_types = [] valid data_types = ['integer','text','real','numeric','blob']
		primary_key: a key that uniquely identifies the row (string)
		"""
		if(len(columns) == 0):
			raise NoColumnsGivenError("Columns list is empty")

		if(len(data_types) == 0):
			raise NoDataTypesGivenError("Data Types list is empty")

		if(len(columns) != len(data_types)):
			CountDontMatchError("Column count and data types count don't match")

		if primary_key not in columns:
			NoPrimaryKeyError("Primary key not in the column list")

		for x in data_types:
			if(self.__helper._functions__isvalid_dtype(x) == False):
				DataTypeError("Please give a valid data type")

		data_types = [x.upper() for x in data_types]
		temp =''''''
		temp_list = []
		for i in range(len(columns)):
			if(columns[i] is primary_key):
				temp_list.append(columns[i]+''' '''+data_types[i]+''' PRIMARY KEY''')
			else:
				temp_list.append(columns[i]+''' '''+data_types[i])

		temp = ''', '''.join(temp_list)
		query = '''create table ''' +tablename+ ''' ( ''' +temp+ ''' )'''

		try:
			self.__cur.execute(query)
			self.__conn.commit()
			
		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def show_tables(self):
		""" returns a list of table which contains all the table name in the database"""
		query = "SELECT name FROM sqlite_master WHERE type = 'table'"
		try:
			temp = self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e

		tables = []
		for x in temp:
			tables.append(x["name"])
		del temp
		return tables


	@__configuration_required
	def update(self,tablename,columns,values,where):
		""" updates data to a given table with where condition

		function definition:
		update(tablename,columns,where,values)
		type of where clause should be string

		example: db.update('users',['name'],'id >= 4',['saif'])
		"""
		if type(where) != str:
			raise NotAStringError("please provide a valid where clause")

		length=len(columns)
		if length==0:
			raise NoColumnsGivenError("Columns list is empty")

		placeholder=[s+'=?' for s in columns]
		query='Update '+tablename+' Set '+','.join(placeholder)+' Where '+where
		try:
			self.__cur.execute(query,values)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def count_entries(self,tablename):
		""" returns number of entries in a table

		function definition:
		count_entries(tablename)

		example: db.count_entries('users')
		"""
		query="Select count(*) from "+tablename
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
		fetcheddata = self.__cur.fetchone()
		return fetcheddata[0]

	@__configuration_required
	def describe_table(self,tablename):
		"""describes the columns of the given table
		describe_table(tablename)
		"""
		query = "select * from "+tablename
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
		return self.__cur.description
