import hashlib,pickle,logging
from config import SConf,LConf

class CodeTable:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		try:
			logging.info("Loading existing CST '"+SConf.cstfile+"'...")
			self.table = pickle.load(open(SConf.cstfile,'r'))
			logging.info("Existing CST loaded.")
		except:
			logging.warning("Loading empty CST!")
			self.table = {}


def genCode(s): return "table_"+hashlib.md5(s).hexdigest()

def makeTableName(d): 
	s = ""
	for k in sorted(d):
		s+=k
	return genCode(s)

def disjoin(l1,l2): return len(set(l1) & set(l2)) == 0


def subset(l1,l2): return set(l1).issubset(set(l2))

def printCST(cst):
	print "CST state"
	for key in cst.keys():
		print "key: "+key+" content: "+str(cst[key])
	print "----------------------------------------"


#this is for querying
def getCommonSets(s,cst):
	sets=[]
	for key in cst.keys():
		print str(cst[key])+" "+str(s)
		if len(set(cst[key]) & set(s)) > 0:
			sets.append(key)
	return sets

#this one is for the best insertion
def getSetWithMostCommonTags(s,cst):
	rset=[]
	rkey = ""
	for key in cst.keys():
		if len(rset) < (len(set(s) & set(cst[key]))):
			rset = list(set(s) & set(cst[key]))
			rkey = key
			logging.debug("For set: "+str(s)+"\nmerging with "+str(cst[key])+"\nresulting in rkey "+str(rkey)+" and rset "+str(rset))
	return rkey,rset


def queryMatch(f, d1, d2):
	if f == 'equal':
		return d1 == d2

def confLogger():
	logger = logging.getLogger("sheila")
	logging.basicConfig(filename='sheila.log', level=logging.INFO)
	logger.setLevel(LConf.level)
	# create console handler and set level to debug
	ch = logging.StreamHandler()
	ch.setLevel(LConf.level)
	formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s","%Y-%m-%d %H:%M:%S")
	ch.setFormatter(formatter)
	logger.addHandler(ch)
