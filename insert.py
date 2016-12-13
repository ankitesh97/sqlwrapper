import MySQLdb

def insert(tablename,columns=None,values=None):#columns is a list
	conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "",db = "test")
	cursor = conn.cursor ()
	if columns:
		query="Insert into "+tablename+" ("+','.join(columns)+") Values ("+','.join(values)+")"
	else:
		query="Insert into "+tablename+" Values ("+','.join(values)+")"
			#print query
	try:
		cursor.execute(query)
		conn.commit()
		print "Successfully executed the query."
	except:
		conn.rollback()
		print "Unsuccessful execution of query."
	conn.close()
insert("k",[],['21','90','70'])