import web, types, os
from urls import url_mappings
from common import Templates, MongoDB, Object, Context
from dynamic.authentication.SessionManager import EstablishSession
from dynamic.core.Config import GetConfigurations

def page_not_found():
	return web.notfound (Templates.errors.page_not_found())

def internal_error():
	return web.internalerror (Templates.errors.internal_error())

def initialize_environment():
	Context.Config      = GetConfigurations ('CodeJedi.cfg')
	Context['DB']       = MongoDB ()
	Context['Cookies']  = web.cookies()
	Context.Request     = web.input()
	Context.SetCookie   = web.setcookie
	Context.Redirect    = web.seeother
	Context.ProblemDir  = "Submissions/Problems/"
	Context.SolutionDir = "Submissions/Solutions/"
	EstablishSession()
	web.template.Template.globals['Session'] = Context.User

if __name__ == '__main__' :
	app = web.application (url_mappings, globals())
	app.notfound = page_not_found
	app.internalerror = internal_error
	app.add_processor(web.loadhook(initialize_environment))
	app.run()

