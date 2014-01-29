import ConfigParser,os

class Conf:
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Conf, cls).__new__(cls, *args, **kwargs)
		return cls._instance
	def __repr__(self):
		return '%r' % (self.__class__)
	def __init__(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read('sheila.cfg')

class BEConf(Conf):
	def __init__(self):
		Conf.__init__(self)
		self.port = self.config.getint('BE', 'port')
		self.host = self.config.get('BE', 'host')
		self.user = self.config.get('BE', 'user')
		self.passwd = self.config.get('BE', 'pass')
		self.db = self.config.get('BE', 'db')

class IConf(Conf):
	def __init__(self):
		Conf.__init__(self)
		self.host=self.config.get('Interface', 'host')
		self.port=self.config.getint('Interface', 'port')
		self.debug=self.config.get('Interface', 'debug')

class SConf(Conf):
	def __init__(self):
		Conf.__init__(self)
		self.cstfile=self.config.get('Sheila','cstfile')
		self.clear=self.config.getboolean('Sheila','clearOnStart')

class LConf(Conf):
	def __init__(self):
		Conf.__init__(self)
		self.level=self.config.get('Log','level')
		self.maxFileSize=self.config.getint('Log','maxFileSize')
		self.logfile=self.config.get('Log','logfile')
