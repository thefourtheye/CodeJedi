import web, sys, os
from common import Templates, Context

class index:
	def GET(self):
		templates = os.path.join(os.path.dirname(__file__) + "/templates/")
		sys.path.insert(1, templates)
		return web.template.render (templates).index()

class Home:
	def GET(self):
		if not Context.User.getAuthenticated(): raise Context.Redirect('/expiredsession')
		return Templates.home()

