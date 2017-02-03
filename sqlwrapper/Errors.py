

class PathNotSetError(Exception):
	"""database path not set error"""

	def __init__(self,message):
		super(PathNotSetError, self).__init__(message)
		self.message = message

class SetPasswordError(Exception):
	"""session password not set error"""

	def __init__(self, message):
		super(SetPasswordError, self).__init__(message)
		self.message = message
		
class ValidationError(Exception):
	"""not logged in"""

	def __init__(self, message):
		super(ValidationError, self).__init__(message)
		self.message = message

class NotAStringError(Exception):
	"""where clause not a string"""
	def __init__(self,message):
		super(NotAStringError,self).__init__(message)
		self.message = message

####################################
##########postgres##################

class NullConnectionError(Exception):
	"""db server is not connected"""
	def __init__(self,message):
		super(NullConnectionError,self).__init__(message)
		self.message = message


class NoColumnsGivenError(Exception):
	
	def __init__(self, message):
		super(NoColumnsGivenError, self).__init__(message)
		self.message = message

class NoDataTypesGivenError(Exception):

	def __init__(self,message):
		super(NoDataTypesGivenError, self).__init__(message)
		self.message = message

class CountDontMatchError(Exception):

	def __init__(self,message):
		super(CountDontMatchError, self).__init__(message)
		self.message = message

class NoPrimaryKeyError(Exception):

	def __init__(self,message):
		super(NoPrimaryKeyError, self).__init__(message)
		self.message = message

class DataTypeError(Exception):

	def __init__(self,message):
		super(DataTypeError, self).__init__(message)
		self.message = message


class NoValuesGivenError(Exception):
	def __init__(self, message):
		super(NoValuesGivenError, self).__init__(message)
		self.message = message
