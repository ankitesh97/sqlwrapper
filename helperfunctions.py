

class functions():

	def __init__(self):
		self.__temp = {}
		self.final = []
		self.__data_types = ['INTEGER', 'TEXT', 'REAL', 'NUMERIC', 'BLOB', 'VARCHAR']

	def __rowtodict(self,listofrows):

		"""function for internal use it converts rows object to list of dictionaries"""

		self.__final = []
		self.__temp = {}
		if not listofrows:
			return self.__final

		keys = listofrows[0].keys()
		
		for row in listofrows:
			for key in keys:
				self.__temp[key] = row[key]
			
			self.__final.append(self.__temp)
			self.__temp = {}
		return self.__final


	def __isvalid_dtype(self,data_type):
		"""function that validates the data type"""
		if data_type.upper() in self.__data_types:
			return True
		return False
