
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

	
	def connect(self, database, user, password, host, port):
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
		columns = self.__helper._functions__desc_to_columns(self.__cur.description)
		fetcheddata = self.__helper._functions__pgtodict(fetcheddata,columns)
		return fetcheddata
