import sqlite3 as sql


class sqlwrapper():

	def __init__(self):
		self.__databasepath = None
		self.__datatbaseaname = None
		self.__metadata = []
		self.__conn = None
		self.__cur = None
		self.__wheredict = {"$gt":"> ?", "$gte":">= ?", "$lt":"< ?", "$lte":"<= ?", "$bt":"> ? and < ?",
		"$btei":">= ? and <= ?"}


	def configure(self,databasepath):
		self.__databasepath = databasepath
		self.__datatbaseaname = databasepath.split('/')[-1]
		self.__conn = sql.connect(self.__databasepath)		
		self.__conn.row_factory = sql.Row
   		self.__cur = self.__conn.cursor()

	# def __updatemetadata(self):
	def __rowtodict(self,listofrows):

		"""function for internal use it converts rows object to list of dictionaries"""

		final = []
		temp = {}
		if not listofrows:
			return final

		keys = listofrows[0].keys()
		
		for row in listofrows:
			for key in keys:
				temp[key] = row[key]
			
			final.append(temp)
			temp = {}
		
		return final

	def fetch_all(self,tablename):
		
		""" fetches all the data from a given table """
		
	   	
		query = 'select * from '+tablename		
		try:
			self.__cur.execute(query)
		except Exception as e:
			return "could not execute query some error occured please try again, error was "+str(e)
	   	fetcheddata = self.__cur.fetchall()  #data type of fetchall is list of rows object
		fetcheddata = self.__rowtodict(fetcheddata)
		return fetcheddata


	def fetch_first(self,tablename):
		"""fetches the first data from the table"""

		query = 'select * from '+tablename+" ASC LIMIT 1"
		try:
			self.__cur.execute(query)
		except Exception as e:
			return "could not execute query some error occured please try again, error was "+str(e)
		fetcheddata = self.__cur.fetchall()
		fetcheddata = self.__rowtodict(fetcheddata)
		return fetcheddata[0]

	def fetch_last(self,tablename):
		"""fetches the last data from the table"""

		temp = self.fetch_all(tablename)
		if(type(temp) == str):
			return temp
		return temp[-1]