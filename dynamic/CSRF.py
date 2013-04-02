import web
from common import Context, Object
from dynamic.authentication.SessionManager import LogoutSession
def CSRFProtected (function_to_be_called):
	def decorated (*args, **kwargs):
		if ('CSRFToken' not in Context.Request or Context.Request.CSRFToken != Context.User.getCSRFToken()):
			LogoutSession()
			raise web.internalerror()
		return function_to_be_called (*args, **kwargs)
	return decorated
