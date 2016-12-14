import sqlite3 as sql
from helperfunctions import functions
from functools import wraps
import hashlib

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
				return "please set the database path using configure('path/to/your/db') method"
			

			return f(self,*args,**kwargs)
		return isconfigured

	def __login_required(f):
		@wraps(f)
		def isroot(self,*args,**kwargs):
			#checks if the user is logged in
			if(self.__rootpwd == None):
				return "please set a session password using db.set_session_password(pwd) method"
			if(self.__isroot == 0):
				return "please call db.login(pwd) to login to a session"
			else:
				return f(self,*args,**kwargs)
		return isroot



############################################################################################
############################## configuration code ##########################################
############################################################################################

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


   	def set_session_password(self,pwd):
   		"""set a session password to execute sensitive commands
   		usage:
   		db.set_session_password("a_password")
   		"""

   		if(self.__rootpwd == None):
   			self.__rootpwd = hashlib.md5(pwd).hexdigest()
   		else:
   			self.__change_password(pwd)

   	def login(self,pwd):
   		"""login to a session to execute sensitive commands
   		usage:
   		db.login("password_that_was_set")
   		"""
   		if(self.__isroot == 1):
   			return "User is already logged in"
   		if(self.__rootpwd == None):
   			return "please set a session password using db.set_session_password(pwd) method"
   		else:
   			if(self.__rootpwd == hashlib.md5(pwd).hexdigest()):
   				self.__isroot = 1
   				return "successfully logged in"
   			else:
   				return "wrong paswword please try again"
		return "wrong paswword please try again"

   	@__login_required
   	def logout(self):
   		""" logsout the session now no more sesitive commands can be used"""
   		self.__rootpwd = None
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
	def insert(self,tablename,columns=None,values=None):
		"""inserts data in the given tale
		usage:
		db.insert('users',['id','name'],[1,'saif'])
		db.insert('users',[],[1,'saif']) if there are only two columns in the table
		"""

		length=len(columns)
		if length!=0:
			placeholder=['?']*length
			query="Insert into " +tablename+ " ("+','.join(columns)+") Values ("+','.join(placeholder)+")"
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


	@__configuration_required
	@__login_required
	def drop_table(self,tablename):
		"""drops the given table from the database
		requires to be authenticated to execute this command
		usage:
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
			return "could not drop the table, some error occured the error was: "+ str(e)

	@__configuration_required
	def create_table(self,columns=None,data_types=None,primary_key=None,foreign_key=None):
		""" creates a table in the database
		arguments:
		coulmns = [] array which contains column names
		data_types = [] valid data_types = [integer,text,real,numeric,blob,varchar
		"""
		if(columns == None):
			return "please give columns"
		if(data_types == None):
			return "please give data_type"