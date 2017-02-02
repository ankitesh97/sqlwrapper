
#import the module, mysqlwrapper is a class defined inside the module
from mysqlwrapper import mysqlwrapper

#create a db object
db=mysqlwrapper()

#let's connect to our mysql database
db.mysqlconnect("localhost","root","","test")	

#For example: host="localhost",user="root",password="1234",dbname="test"
#if everything goes correct you have successfully connected to your database


#we have just started the shop thus we only keep one type of pet i.e dogs let's create dog table
# dogs will have following characteristics id, breed, color, weight(in kg)
# it takes tablename, columns, data types and primary key as the input
db.create_table('dogs', ['id','breed','color','weight'],['integer','text','text','real'],'id')
#now your table has been created
# you can check all the tables in the database by using db.show_tables()
#now we have creted dogs table
#You can check the description of the columns in the table by using db.describe_table('dogs')

#let's insert some values
#it takes columns and values
db.insert('dogs', ['id','breed','color','weight'],[1,'Labrador','yellow',29.4])
#the above query can also be written as
db.insert('dogs',[],[2,'German Shepherd','black',30.6])
#let's say i got a new dog but its weight is unknown
db.insert('dogs',['id','breed','color'],[3, 'German Shepherd', 'Brown'])
#this will make an entry of (3,German Shepherd, brown,None) in the table

#now let's fetch the values that was inserted
print db.fetch_all('dogs') #this will return all values in the dogs table in the form of list of dictionaries
print db.fetch_first('dogs') #this will return the first entry of the table
print db.fetch_last('dogs') #this will return thr last entry of the table

# now let's fetch the dogs whose breed is German Shepherd
print db.fetch_by('dogs',where= 'breed = "German Shepherd"')

#fetch all the dogs whose breed is German Shepherd or it has yellow color skin
print db.fetch_by('dogs',where= 'breed = "German Shepherd" or color = "yellow"')

# fetch all the dogs whose breed is German Shepherd and color is black
print db.fetch_by('dogs',where= 'breed = "German Shepherd" and color = "black"')

#remember we had bought a dog whose weight was not known, well now the weight is known so let's update the entry
db.update_by('dogs',['weight'],[34.5],where= ' id = 3')

#let's say he was bought by some buyer, thus now we will have to delete his entry
db.delete_by('dogs', "id=3")

#you can also count entries in the table by using 
db.count_entries('dogs')

#also there is a method to delete all data from a specific table
db.delete_all_from('dogs')
#let's say you have decided to stop selling dogs and you want to delete all the data i.e dogs table
# now you can use drop table method
db.drop_table('dogs')


#you're done all basic functions at your finger tips, don't need to write queries, now to develop a basic
#app it is fast and easy !!!