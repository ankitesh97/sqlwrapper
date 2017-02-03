# sqlwrapper
 This module is a wrapper aroung SQL query language, i.e an interface between the database and python.
 
 version: v0.1

## Installation

```python
pip install sqlwrapper
```

## What is it?

Can be used to develop a database based application quickly in python. It is a method based package, i.e you don't require the knowledge of sql language. Basically one can create a CRUD application quickly.

Currently provides an interface for Mysql, sqlite, postgresql databases. Tested for python 2.7.x

#### Requirements
psycopg2=2.6.1 (and above)(for postgresql)(pip install psycopg2)
mysqlclient=1.3.7 (and above)(for mysql Basically import MYSQLdb)
(pip install MySQL-python)

### Advantages

Quick development of CRUD based database application
No knowledge of SQL required
Very easy to understang and use

### Basic import

### object for sqlite

```python
>> from sqlwrapper import sqlitewrapper
>> db = sqlitewrapper()
```

### object for Mysql

```python
>> from sqlwrapper import mysqlwrapper
>> db = mysqlwrapper()
```
### object for PostgreSql

```python
>> from sqlwrapper import psqlwrapper
>> db = psqlwrapper()
```
Description of all the methods are in the package documentation which can be viewed from the official pypi website

## Cookbook
Examples are in the Examples folder