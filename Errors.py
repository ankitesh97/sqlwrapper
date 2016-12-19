

class PathNotSetError(Exception):
	"""database path not set error"""

	def __init__(self,message):
		super(PathNotSetError, self).__init__(message)
		self.message = message

class SetPasswordError(Exception):
	"""session password not set error"""

	def __init__(self, arg):
		super(SetPasswordError, self).__init__(message)
		self.message = message
		
class ValidationError(Exception):
	"""not logged in"""

	def __init__(self, arg):
		super(ValidationError, self).__init__(message)
		self.message = message

class NotAStringError(Exception):
	"""where clause not a string"""
	def __init__(self,arg):
		super(NotAStringError,self).__init__(message)
		self.message = message

####################################
##########postgres##################

class NullConnectionError(Exception):
	"""pg server is not connected"""
	def __init__(self,arg):
		super(NullConnectionError,self).__init__(message)
		self.message = message