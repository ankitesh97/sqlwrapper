
import psycopg2 as pg
from helperfunctions import functions
from Errors import *
from functools import wraps


class psqlwrapper():

	"""class that provides an interface to query the postgres server
	   use:
	   from sqlwrapper import psqlwrapper
	   db = psqlwrapper()
	"""

	def __init__(self):
		self.__databasename = None
		self.__host = None
		self.__port = None
		self.__user = None
		self.__metadata = {}
		self.__conn = None
		self.__cur = None
		self.__helper = functions()

############################################################################################
######################################## wrappers ##########################################
############################################################################################
	
	def __configuration_required(f):
		@wraps(f)
		def isconfigured(self,*args,**kwargs):
			if(self.__cur == None):
				raise NullConnectionError("Not connected to postgres server")
			
			return f(self,*args,**kwargs)
		return isconfigured

############################################################################################
######################################## configuration code  ###############################
############################################################################################

	
	def connect(self, database, user, password, host='127.0.0.1', port=5432):
		self.__metadata["dbname"] = database
		self.__metadata["user"] = user
		self.__metadata["host"] = host
		self.__metadata["port"] = port
		try:
			self.__conn = pg.connect(database=database, user=user, password=password, host=host, port=port)
			self.__cur = self.__conn.cursor()
		except Exception as e:
			raise e

############################################################################################
################################# functional code ##########################################
############################################################################################

	@__configuration_required
	def fetch_all(self, tablename):
		"""fetches all the data from a given table

		function definition:
		fetch_all(tablename)

		example: db.fetch_all('users')
		return_type: returns list of dictionaries (i.e the whole table)
		"""

		query = 'select * from "'+tablename+'"'
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
		fetcheddata = self.__cur.fetchall()
		if fetcheddata:
			columns = self.__helper._functions__desc_to_columns(self.__cur.description)
			fetcheddata = self.__helper._functions__pgtodict(fetcheddata,columns)
			return fetcheddata
		return None

	@__configuration_required
	def fetch_first(self, tablename):
		"""fetches first data point from a given table

		function definition:
		fetch_first(tablename)

		example: db.fetch_first('users')
		return_type: returns the first data in the given table
		"""
		query = 'select * from "'+tablename+'" LIMIT 1'
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
		fetcheddata = self.__cur.fetchall()
		if fetcheddata:
			fetcheddata = fetcheddata[0]
			columns = self.__helper._functions__desc_to_columns(self.__cur.description)
			fetcheddata = self.__helper._functions__pgtodict([fetcheddata],columns)
			return fetcheddata[0]
		return None

	@__configuration_required
	def fetch_last(self, tablename):
		"""fetches the last data from the table

		function definition:
		fetch_last(tablename)

		example: db.fetch_last('users')
		return_type: single dictionary (i.e row)
		"""
		query = 'select * from "' + tablename + '"'
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
		fetcheddata = self.__cur.fetchall()
		if fetcheddata:
			fetcheddata = fetcheddata[-1]
			columns = self.__helper._functions__desc_to_columns(self.__cur.description)
			fetcheddata = self.__helper._functions__pgtodict([fetcheddata],columns)
			return fetcheddata[-1]
		return None

	@__configuration_required
	def fetch_by(self, tablename, **kwargs):
		""" fetches data from a given table with where condition

		function definition:
		fetch_by(tablename,**kwargs)
		kwargs should be a column name = its value(it is where clause which will identify the row
		note: for where clause if multiple keyword arguments are supplied it will be joined using and

		example: db.fetch_by('users',id = 4)
		returns: list of dictionaries that satisfies the where clause
		"""

		columns = kwargs.keys()
		values = kwargs.values()
		query = 'Select * from "'+tablename+'" Where'
		for column in columns:
			query+= ' "'+column+'" = %s '
			if column != columns[-1]:
				query+= 'and'
		try:
			self.__cur.execute(query,values)
		except Exception as e:
			self.__conn.rollback()
			raise e
		fetcheddata = self.__cur.fetchall()
		if fetcheddata:
			columns = self.__helper._functions__desc_to_columns(self.__cur.description)
			fetcheddata = self.__helper._functions__pgtodict(fetcheddata,columns)
			return fetcheddata
		return []

	@__configuration_required
	def insert(self, tablename, columns, values):

		"""inserts data in the given tale

		function definition:
		insert(tablename,columns,values)
		columns should be a list containing column names(string)
		values should be a list containing column values

		usage:
		db.insert('users',['id','name'],[1,'saif'])
		db.insert('users',[],[1,'saif']) if there are only two columns in the table
		"""
		if not values:
			raise NoValuesGivenError("No values given to insert")
		length=len(columns)
		if length!=0:
			placeholder=['%s']*length
			query='Insert into "' +tablename+ '" ('+','.join(['"'+column+'"' for column in columns])+') Values ('+','.join(placeholder)+')'
		else:
			l = len(values)
			placeholder=['%s']*l
			query='Insert into "'+tablename+'" Values ('+','.join(placeholder)+')'
		try:
			self.__cur.execute(query,values)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def delete_by(self, tablename, **kwargs):
		""" deletes the entry from the table using the where clause to identify the row
		function definition:
		delete_by(tablename. **kwargs)
		kwargs should be a column name = its value(it is where clause which will identify the row
		note: for where clause if multiple keyword arguments are supplied it will be joined using and
		example:
		delete_by('users',id=4)
		"""
		columns = kwargs.keys()
		values = kwargs.values()
		query = 'delete from "'+tablename+'" where '+ "and".join(['"'+column+'" = %s' for column in columns])
		try:
			self.__cur.execute(query,values)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def delete_all_from(self,tablename):
		"""deletes all the entry from the given table
		prototype: delete_all_from(tablename)
		"""
		query = 'delete from "'+tablename+'"'
		try:
			self.__cur.execute(query)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def drop_table(self,tablename):
		"""drops the table from the database
		function definition:
		drop_table(tablename)
		tablename is the name of the table that is to be dropped
		"""
		query = 'drop table "'+tablename+'"'
		try:
			self.__cur.execute(query)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def create_table(self,tablename, columns, data_types, primary_key):
		""" creates a table in the database

		function definition:
		create_table(tablename,columns,data_types,primary_key)

		arguments:
		tablename: appropriate tablename (string)
		coulmns = [] array which contains column names (string)
		data_types = [] valid data_types = ['integer','text','real','numeric','blob']
		primary_key: a key that uniquely identifies the row (string)

		"""
		if (len(columns) == 0):
			raise NoColumnsGivenError("Columns list is empty")

		if (len(data_types) == 0):
			raise NoDataTypesGivenError("Data Types list is empty")

		if (len(columns) != len(data_types)):
			raise CountDontMatchError("Column count and data types count don't match")

		if primary_key not in columns:
			raise NoPrimaryKeyError("Primary key not in the column list")

		for x in data_types:
			if (self.__helper._functions__isvalid_dtype(x) == False):
				DataTypeError("Please give a valid data type")

		data_types = [x.upper() for x in data_types]
		temp_list = []
		for i in range(len(columns)):
			if (columns[i] is primary_key):
				temp_list.append(columns[i] + ' ' + data_types[i] + ' PRIMARY KEY')
			else:
				temp_list.append(columns[i] + ' ' + data_types[i])

		temp = ', '.join(temp_list)
		query = 'create table "' + tablename + '"' + '( '+temp+' )'

		try:
			self.__cur.execute(query)
			self.__conn.commit()

		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def show_tables(self):
		""" returns a list of table which contains all the table name in the database"""
		query = 'SELECT table_name FROM information_schema.tables where table_schema = %s'
		try:
			self.__cur.execute(query, ['public'])
			temp = self.__cur.fetchall()
		except Exception as e:
			raise e
		tables = []
		for x in temp:
			tables.append(x[0])
		del temp
		return tables

	@__configuration_required
	def update_by(self,tablename,columns,values, **kwargs):
		""" updates data to a given table with where condition

		function definition:
		update(tablename,columns,values,**kwargs)
		tablename is the name of the table
		columns = [] should be a list of columns that is to be updated
		values = [] should be a list of vlaues corresponding to the columns
		kwargs should be a column name = its value(it is where clause which will identify the row
		note: for where clause if multiple keyword arguments are supplied it will be joined using and
		also you can't update the whole row at once without giving the column names

		example: db.update('users',['name'],['saif'], id=4)
		db.update('Books', ['title', 'cover'], ['new_title','new_cover'], pages>100, pages<200)
		in this case it will be equivalent to pages between 100 and 200
		"""
		if len(columns) == 0:
			raise NoColumnsGivenError("Columns list is empty")

		placeholder = ['"'+x+'" = %s' for x in columns]
		keys = kwargs.keys()
		val = kwargs.values()
	 	if not keys:
			query = 'Update "'+tablename+'" Set '+ ", ".join(placeholder)
		else:
			query = 'Update "'+tablename+'" Set '+", ".join(placeholder) + ' Where '+"and".join(['"'+x+'" = %s' for x in keys])
		try:
			self.__cur.execute(query,values+val)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			raise e

	@__configuration_required
	def count_entries(self,tablename):
		""" returns number of entries in a table

		function definition:
		count_entries(tablename)
		returns in terms of long i.e 6L that means 6 long
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
		query = 'select * from "'+tablename+'"'
		try:
			self.__cur.execute(query)
		except Exception as e:
			self.__conn.rollback()
			raise e
		return self.__cur.description






