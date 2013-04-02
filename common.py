import web, sys, os, logging
templates = os.path.join(os.path.dirname(__file__) + "/templates/")
sys.path.insert(1, templates)
Templates = web.template.render (templates, base='master')
from web import ctx as Context
from dynamic.core.genericmodel  import GenericModel as Object
from dynamic.core.mongodb       import MongoDb      as MongoDB
Logger = logging.getLogger ('')
Context.RootDirectory = os.path.dirname(__file__) + "/"
