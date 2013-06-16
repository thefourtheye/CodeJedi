from common import Context, Templates, Object
from dynamic.CSRF import CSRFProtected

class SubmitProblems:
	def GET(self):
		if not Context.User.getAuthenticated(): raise Context.Redirect ("/")
		return Templates.Problems.Submit (None, None)

	@CSRFProtected
	def POST(self):
		Message = ""
		if 'ProblemName' not in Context.Request or Context.Request.ProblemName.strip() == "":
			Message += "<li>Problem Name field cannot be empty.</li>"
		if 'ProblemDescription' not in Context.Request or Context.Request.ProblemDescription.strip() == "":
			Message += "<li>Problem Description field cannot be empty.</li>"
		if 'Editorial' not in Context.Request or Context.Request.Editorial.strip() == "":
			Message += "<li>Editorial field cannot be empty.</li>"
		if 'SmallTestCaseFile' not in Context.Request or Context.Request.SmallTestCaseFile.strip() == "":
			Message += "<li>Preliminary test case file field cannot be empty.</li>"
		if 'BigTestCaseFile' not in Context.Request or Context.Request.BigTestCaseFile.strip() == "":
			Message += "<li>System test case file field cannot be empty.</li>"
		if 'Category' not in Context.Request or Context.Request.Category.strip() == "":
			Message += "<li>Category field cannot be empty.</li>"
		if Message != "":
			return Templates.Problems.Submit (Message, True)
		else:
			ProblemName = Context.Request.ProblemName
			Description = Context.Request.ProblemDescription
			Editorial   = Context.Request.Editorial
			Category    = "" if 'Category' not in Context.Request else Context.Request.Category
			SmallFile   = Context.Request.SmallTestCaseFile
			BigFile     = Context.Request.BigTestCaseFile
			Practice    = False if 'Practice' not in Context.Request else True
			ProblemID   = str(Context.DB.count (dict(), 'Problems') + 10000)
			Problem = Object(dict
									(
											ProblemID   = ProblemID,
											ProblemName = ProblemName,
											Practice    = Practice,
											Category    = Category,
											Deleted     = False
									)
								 )
			Context.DB.insert (Problem, 'Problems')
			open (Context.ProblemDir + ProblemID + "_Description.txt", "w").writelines (Description)
			open (Context.ProblemDir + ProblemID + "_Editorial.txt", "w").writelines (Editorial)
			open (Context.ProblemDir + ProblemID + "_Small.txt", "w").writelines (SmallFile)
			open (Context.ProblemDir + ProblemID + "_Big.txt", "w").writelines (BigFile)
			return Templates.Problems.Submit ("Problem Submitted Successfully", False)

