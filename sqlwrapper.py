import sqlite3 as sql


class sqlwrapper():

	def __init__(self):
		self.__databasepath = None
		self.__datatbaseaname = None
		self.__metadata = []
		self.__cur = None


	def configure(self,databasepath):
		self.__databasepath = databasepath
		self.__datatbaseaname = databasepath.split('/')[-1]
		conn = sql.connect(self.__databasepath)		
		conn.row_factory = sql.Row
   		self.__cur = conn.cursor()

	# def __updatemetadata(self):

	def fetch(self,tablename,where=None):
		
		if where is None:
			query = 'Select * from '+tablename		
	   	self.__cur.execute(query)
	   	fetcheddata = self.__cur.fetchall()  #data type of fetchall is list of rows object
		return fetcheddata