# import MySQLdb
import sqlite3 as sql

def insert(tablename,columns=None,values=None):#columns is a list
	# conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "",db = "test")
	conn = sql.connect('/home/ankitesh/modules/sqlwrapper/test.sqlite')
	cursor = conn.cursor ()
	for x in 
	if columns:
		query="Insert into "+tablename+" ("+','.join(columns)+") Values ("+','.join(values)+")"
	else:
		query="Insert into "+tablename+" Values ("+','.join(values)+")"
			#print query
	try:
		cursor.execute(query)
		conn.commit()
		return "Successfully executed the query."
	except:
		conn.rollback()
		return "Unsuccessful execution of query."
	conn.close()
insert("k",["id","name"],['21','90','70'])