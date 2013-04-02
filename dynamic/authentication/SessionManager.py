import web
from common import Context, Templates, Object, Logger
from time import time
from hashlib import sha512
from bson import ObjectId

def CreateSession (userID, displayName):
	SessionTimeout = int(Context.Config.getSession().getTimeOut())
	CSRFTimeout    = int(Context.Config.getCSRF().getTimeOut())
	SessionToken = sha512(userID + Context.ip + str(time())).hexdigest()
	CurrentUser = Context.DB.find (dict(userid=userID), 'User')
	if len(CurrentUser) == 0:
		CurrentUser = Object( dict (
										userId = userID,
										displayName=displayName,
										accessLevel='Participant',
										session = dict (
												ip=Context.ip,
												expirytime=time() + SessionTimeout,
												token=SessionToken
										),
										CSRF = dict (
											CSRFToken = sha512(userID + Context.ip + str(time())).hexdigest(),
											ExpiryTime = time() + CSRFTimeout
										)
									)
								)
		Context.DB.insert (CurrentUser, 'User')
	elif len(CurrentUser) == 1:
		CurrentUser = CurrentUser[0]
		CurrentUser.getSession().setIP (Context.ip);
		CurrentUser.getSession().setExpiryTime (time() + SessionTimeout);
		CurrentUser.getSession().setToken (SessionToken)
		CSRFExpiryTime = CurrentUser.getCSRF().getExpiryTime()
		if time() > CSRFExpiryTime:
			CurrentUser.getCSRF().setCSRFToken (sha512(userID + Context.ip + str(time())).hexdigest())
			CurrentUser.getCSRF().setExpiryTime (time() + CSRFTimeout)
		MongoID = CurrentUser.getID()
		CurrentUser.delID()
		Context.DB.save (dict(_id=ObjectId(MongoID)), CurrentUser, 'User')
	else:
		Logger.critical ("More than one User records for User ID : %s" % userID)
		raise web.internalerror()
	Context.User.setAuthenticated(True)
	Context.User.setUserID(CurrentUser.getUserID())
	Context.User.setDisplayName(CurrentUser.getDisplayName())
	Context.User.setAccessLevel(CurrentUser.getAccessLevel())
	Context.User.setSessionID(SessionToken)
	Context.User.setCSRFToken(CurrentUser.getCSRF().getCSRFToken())
	Context.SetCookie ('Session', SessionToken)

def EstablishSession():
	Context['User'] = Object(dict(Authenticated=False, UserId=None, DisplayName=None, AccessLevel=None, SessionID=None, CSRFToken=None))
	if 'Session' in Context.Cookies:
		UserSession = Context.DB.find ({"session.token" : Context.Cookies.Session}, "User")
		if len(UserSession) == 0: return
		elif len(UserSession) > 1: return web.seeother ("/invalidsession")
		UserSession = UserSession[0]
		ExpiryTime = UserSession.getSession().getExpiryTime()
		CSRFExpiryTime = UserSession.getCSRF().getExpiryTime()
		CSRFTimeout    = int(Context.Config.getCSRF().getTimeOut())
		if time() > ExpiryTime: web.seeother ('/expiredsession')
		if Context.ip != UserSession.getSession().getIP(): return web.seeother ('/invalidsession')
		if time() > CSRFExpiryTime:
			UserSession.getCSRF().setCSRFToken (sha512(UserSession.getUserID() + Context.ip + str(time())).hexdigest())
			UserSession.getCSRF().setExpiryTime (time() + CSRFTimeout)
			MongoID = UserSession.getID()
			UserSession.delID()
			Context.DB.save (dict(_id=ObjectId(MongoID)), UserSession, 'User')
		Context.User.setAuthenticated(True)
		Context.User.setUserID (UserSession.getUserID())
		Context.User.setDisplayName (UserSession.getDisplayName())
		Context.User.setAccessLevel (UserSession.getAccessLevel())
		Context.User.setSessionID (Context.Cookies.Session)
		Context.User.setCSRFToken (UserSession.getCSRF().getCSRFToken())

def LogoutSession (SessionID = None):
	Context.User.setAuthenticated(False)
	Context.SetCookie ('Session', '', expires=-1)
	if SessionID == None: SessionID = Context.User.getSessionID()
	if SessionID == None: SessionID = Context.Cookies.Session if 'Session' in Context.Cookies else None
	if SessionID == None: return
	UserSessions = Context.DB.find ({"session.token" : SessionID}, "User")
	if len(UserSessions) == 0: return
	for UserSession in UserSessions:
		MongoID = UserSession.getID()
		UserSession.delID()
		UserSession.getSession().setToken (None)
		UserSession.getSession().setExpiryTime (None)
		UserSession.getSession().setIP(None)
		UserSession.getCSRF().setCSRFToken(None)
		UserSession.getCSRF().setExpiryTime(None)
		Context.DB.save (dict(_id=ObjectId(MongoID)), UserSession, 'User')
