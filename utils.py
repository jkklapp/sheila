import hashlib,pickle,utils
import logging
import logging.handlers
import bz2,os
import MySQLdb


class CodeTable:
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self,conf):
		self.path=conf.cstfile
		try:
			logging.info("Loading existing CST '"+conf.cstfile+"'...")
			self.table = pickle.load(open(conf.cstfile,'r'))
			logging.info("Existing CST loaded.")
		except:
			logging.warning("Loading empty CST!")
			self.table = {}
	def __call__(self):
		return self.table
	def get(self,tag):
		try:
			return self.table[tag]
		except KeyError:
			logging.critical("Accessing non existing element on CST table: "+tag)
			raise
	def getKeysAsSet(self,tag):
		try:
			return set(self.table[tag])
		except KeyError:
			logging.critical("Accessing non existing element on CST table: "+tag)
			raise
	def getName(self,tag):
		try:
			return str(self.table[tag])
		except KeyError:
			logging.critical("Accessing non existing element on CST table: "+tag)
			raise
	def set(self,tag,value):
		self.table[tag]=value
	def remove(self,tag):
		try:
			del self.table[tag]
		except KeyError:
			logging.critical("Removing non existing element on CST table: "+tag)
			raise
	def tables(self):
		return self.table.keys()



def genCode(s): return "table_"+hashlib.md5(s).hexdigest()

def makeTableName(d): 
	s = ""
	for k in sorted(d):
		s+=k
	return genCode(s)

def disjoin(l1,l2): return len(set(l1) & set(l2)) == 0


def subset(l1,l2): return set(l1).issubset(set(l2))

def printCST(cst):
	r="CST state\n"
	for key in cst.tables():
		r += "key: "+key+" content: "+cst.getName(key)+"\n"
	r+= "----------------------------------------"
	return r


#this is for querying
def getCommonSets(s,cst):
	tTags=[]
	for key in cst.tables():
		if set(s).issubset(cst.getKeysAsSet(key)):
			tTags.append(key)
	return tTags

#this one is for the best insertion
def getSetWithMostCommonTags(s,cst):
	logger = logging.getLogger("sheila")
	rset=[]
	rkey = ""
	for key in cst.tables():
		if len(rset) < (len(set(s) & cst.getKeysAsSet(key))):
			rset = list(set(s) & cst.getKeysAsSet(key))
			rkey = key
			logger.debug("For set: "+str(s)+"\nmerging with "+cst.getName(key)+"\nresulting in rkey "+str(rkey)+" and rset "+str(rset))
	return rkey,rset


def queryMatch(f, d1, d2):
	if f == 'equal':
		return d1 == d2

def confLogger(conf):
	logger = logging.getLogger("sheila")
	logger.setLevel(conf.level)
	logging.basicConfig(filename='sheila.log')
	# create console handler and set level to debug
	handler = logging.handlers.RotatingFileHandler(conf.logfile, maxBytes=conf.maxFileSize, backupCount=10)
	logger.addHandler(handler)
	ch = logging.StreamHandler()
	ch.setLevel(conf.level)
	formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s","%Y-%m-%d %H:%M:%S")
	ch.setFormatter(formatter)
	logger.addHandler(ch)

def clearEnvironment(sconf,beconf):
	logger = logging.getLogger("sheila")
	try:
		os.remove(sconf.cstfile)
	except OSError:
		logger.critical("No CST file to erase")
	try:
		conn = MySQLdb.connect(host=beconf.host,user=beconf.user,passwd=beconf.passwd)
		c = conn.cursor()
		c.execute('DROP DATABASE '+beconf.db)
		c.execute('CREATE DATABASE '+beconf.db)
		c.close()
		conn.close()
	except:
		logger.critical("Error clearing environment!")
		raise