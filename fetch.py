

""" 
where clause format 

where = {"key":"equal to"} 	        
where = {"key1":{"$gt":"value"}, "key2":"what ever"}   			greater than
where = {"key":{"$lt":"value"}}									less than
where = {"key":{"$gte":"value"}}								greater than equal to
where = {"key":{"$lte":"value"}}								less that equal to
where = {"key":{"$bt":[start,end]}}									between ends excluded
where = {"key":{"$btei":[start,end]}}								between ends included


"""
		self.__wheredict = {"$gt":"> ?", "$gte":">= ?", "$lt":"< ?", "$lte":"<= ?", "$bt":"> ? and < ?",
		"$btei":">= ? and <= ?"}
def __keytoqueryvalue(key = None,keycolumn = None):
	
	""" A function that returns a part of query for a given where clause
		it is for internal use
	"""

	if(key == "$gt"):
		return "> ?"
	elif(key == "$gte"):
		return ">= ?"
	elif(key == "$lt"):
		return "< ?"
	elif(key == "$lte"):
		return "<= ?"
	elif(key == "$bt"):
		if(keycolumn is None):
			return ""
		else:
			return keycolumn += " > ? and " += keycolumn += " < ?"
	else:            #key == '$btei'
		
		if(keycolumn is None):
			return ""
		else:
			return keycolumn += " >= ? and " += keycolumn += " <= ?"

	
	

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
			if(len(dictkeys) > 0):
				query += self.__wheredict[dictkeys[0]]
			else:
				query = ""
		return query
	else:
		for key in keys:
			query += key+ " "
			if(type(where[key) != dict):
				query += "= ?"
			else:
				dictkeys = where[key].keys()
				if(len(dictkeys) > 0):
					query += self.__wheredict[dictkeys[0]]
				else:
					query = ""

			if(query==""):
				continue
			elif(key != keys[-1]):
				query += " and"
			else:
				continue
		return query


	return query




def __processwhereclausetest(tablename,where):
	
	""" processes where clause and returns(string) the query """	
	query = "select * from "+ tablename + " where "
	keys = where.keys()
	for key in keys:
		query += key+ " "
		if(type(where[key]) != dict):
			query += "= ?"
		else:
			dictkeys = where[key].keys()
			if(len(dictkeys) > 0):
				query += self.__keytoqueryvalue[dictkeys[0]]
			else:
				query = ""

		if(query==""):
			continue
		elif(key != keys[-1]):
			query += " and"
		else:
			continue
	return query


def fetch(self,tablename,where=None):
	
	""" fetches data from database also considers where clause """
	
	if where is None:
		query = 'select * from '+tablename		
   	
   	else:
   		self.__processwhereclause(where)

   	self.__cur.execute(query)
   	fetcheddata = self.__cur.fetchall()  #data type of fetchall is list of rows object
	fetcheddata = self.__rowtodict(fetcheddata)
	return fetcheddata