
import re
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

	def __pgtodict(self, pgdataobject, columns):

		"""function that converts pgdataobject to list of dict"""
		self.__final = []
		self.__temp = {}
		try:
			for data in pgdataobject:
				for i in range(len(columns)):
					self.__temp[columns[i]] = data[i]
				self.__final.append(self.__temp)
				self.__temp = {}
		except Exception as e:
			raise e
		return self.__final

	def __desc_to_columns(self,descobj):
		""" converts pg description object to list of columns"""
		coulmns = []
		for x in descobj:
			coulmns.append(x[0])
		return coulmns






