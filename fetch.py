

""" 
where clause format 

where = {"key":"equal to"}         
where = {"key1":{"$gt":"value"}, "key2":"what ever"}   			greater than
where = {"key":{"$lt":"value"}}									less than
where = {"key":{"$gte":"value"}}								greater than equal to
where = {"key":{"$lte":"value"}}								less that equal to
where = {"key":{"$bt":"value"}}									between ends excluded
where = {"key":{"$btei":"value"}}								between ends included


"""


def __rowtodict(listofrows):

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

	return final

def __processwhereclause(tablename,where):
	
	""" processes where clause and returns(string) the query """	
	query = "select * from "+ tablename + " where "
	keys = where.keys()
	if(len(keys)==1):
		query += keys[0]+" "
		if(type(where[keys[0]]) != dict):
			query += "= ?"
		else:
			dictkeys = where[keys[0]].keys()
			

	return query

def fetch(self,tablename,where=None):
	
	""" fetches data from database also considers where clause """
	
	if where is None:
		query = 'select * from '+tablename		
   	
   	else:
   		self.__processwhereclause(where)

   	self.__cur.execute(query)
   	fetcheddata = self.__cur.fetchall()  #data type of fetchall is list of rows object
	
	return fetcheddata