from ConfigParser import SafeConfigParser
from genericmodel import GenericModel

def GetConfigurations(CfgFileName):
	Configurations = GenericModel()
	try:
		parser = SafeConfigParser()
		parser.read (CfgFileName)
		for Section in parser.sections():
			getattr (Configurations, 'set' + Section)(GenericModel())
			CurrentSection = getattr (Configurations, 'get' + Section)()
			for ConfigName, ConfigValue in parser.items (Section):
				getattr (CurrentSection, 'set' + ConfigName) (ConfigValue)
	except:
		print sys.exec_info[0]
	return Configurations
