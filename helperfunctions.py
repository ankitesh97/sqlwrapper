

class functions():

	def __init__(self):
		self.__temp = {}
		self.final = []

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
