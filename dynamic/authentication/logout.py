from common import Templates, Context
from SessionManager import LogoutSession

class UserLogout:
	def GET(self):
		LogoutSession()
		return Templates.loggedout("You are successfully logged out now.")

class InvalidSession:
	def GET(self):
		LogoutSession()
		return Templates.loggedout("Invalid login session.")

class ExpiredSession:
	def GET(self):
		LogoutSession()
		return Templates.loggedout("Your login session expired.")
