url_mappings = (
	'/', 'index.index',
	'/authenticate', 'dynamic.authentication.authentication.Authenticate',
	'/problems/submit', 'dynamic.problems.SubmitProblems.SubmitProblems',
	'/home', 'index.Home',
	'/logout', 'dynamic.authentication.logout.UserLogout',
	'/invalidsession', 'dynamic.authentication.logout.InvalidSession',
	'/expiredsession', 'dynamic.authentication.logout.ExpiredSession',
)
