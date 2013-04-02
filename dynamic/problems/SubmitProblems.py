from common import Context, Templates, Object
from dynamic.CSRF import CSRFProtected

class SubmitProblems:
	def GET(self):
		if not Context.User.getAuthenticated(): raise Context.Redirect ("/")
		return Templates.Problems.Submit (None, None)

	@CSRFProtected
	def POST(self):
		Message = ""
		if 'Description' not in Context.Request or Context.Request.Description.strip() == "":
			Message += "<li>Problem Description cannot be empty.</li>"
		if 'TimeLimit' not in Context.Request or Context.Request.TimeLimit.strip() == "":
			Message += "<li>Time Limit should be a valid number of seconds</li>"
		else:
			try:
				int(Context.Request.TimeLimit)
			except:
				Message += "<li>Time Limit should be a valid number of seconds</li>"
		if 'SmallTestCaseFile' not in Context.Request or Context.Request.SmallTestCaseFile.strip() == "":
			Message += "<li>Preliminary test case file field cannot be empty.</li>"
		if 'BigTestCaseFile' not in Context.Request or Context.Request.BigTestCaseFile.strip() == "":
			Message += "<li>System test case file field cannot be empty.</li>"
		if Message != "":
			return Templates.Problems.Submit (Message, True)
		else:
			Description = Context.Request.Description
			TimeLimit   = Context.Request.TimeLimit
			Category    = "" if 'Category' not in Context.Request else Context.Request.Category
			SmallFile   = Context.Request.SmallTestCaseFile
			BigFile     = Context.Request.BigTestCaseFile
			ProblemID   = str(Context.DB.count (dict(), 'Problems') + 1)
			Dir         = Context.RootDirectory + "Submissions/Problems/" + ProblemID + "/"
			if not os.path.exists(Dir): os.makedirs (Dir)
			open (Dir + "Prelim.txt", "w+").writelines (SmallFile)
			open (Dir + "ST.txt", "w+").writelines (SmallFile)

