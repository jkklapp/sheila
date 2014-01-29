import MySQLdb,pickle,json
import logging
from utils import *

class Backend:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Backend, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self,config):
		logger = logging.getLogger("sheila")
		logger.info("Connecting to DB...")
		self.conn = MySQLdb.connect(host=config.host, port=config.port, user=config.user, passwd=config.passwd, db=config.db)
		logger.info("DB Online.")

def createTable(name, keys, cst, be):
	logger = logging.getLogger("sheila")
	c = be.conn.cursor()
	try:
		logger.debug("Creating new "+name)
		c.execute("CREATE TABLE "+name+" ( id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, data TEXT NOT NULL )")
		be.conn.commit()
	except Exception as e:
		logger.critical(e)
		be.conn.rollback()
	cst.set(name,keys)
	pickle.dump(cst,open(cst.path,'w'))


def updateTable(old, new, cst, be):
	'''Change table name '''
	logger = logging.getLogger("sheila")
	#c = be.conn.cursor()
	#try:
	#	logger.debug("Updating table "+old+ " to "+makeTableName(new))
	#	c.execute("ALTER TABLE "+old+" RENAME TO "+makeTableName(new))
	#	be.conn.commit()
	#except Exception as e:
	#	logger.critical(e)
	#	be.conn.rollback()
	#cst.set(makeTableName(new),new)
	cst.set(old,new)
	pickle.dump(cst,open(cst.path,'w'))


def actual_insert(data, table, be):
	# Actual data insertion
	logger = logging.getLogger("sheila")
	c = be.conn.cursor()
	try:
		logger.debug("Inserting into "+table)
		c.execute("INSERT INTO "+table+"(data) VALUES (%s)",(str(data)))
		be.conn.commit()
	except Exception as e:
		logger.critical(e)
		be.conn.rollback()


def actual_select(data, table, be):
	f = 'equal'
 	c = be.conn.cursor()
 	# current duplicate-free policy on queries
 	logger = logging.getLogger("sheila")
 	logger.debug("MySQL select on "+table)
 	try:
		c.execute("SELECT DISTINCT data FROM "+table)
	except:
		logger.critical("Select on "+table)
	numrows = c.rowcount
	r = []
	for x in xrange(0,numrows):
  		row = c.fetchone()
  		j = json.loads(row[0])
  		if len(j) < len(data):
  			continue
  		add = False
  		for d in data.keys():
  			try:
  				if queryMatch(f,data[d],j[d]):
  					add = True
  			except KeyError:
  				continue
  		if add:
  			r.append(j)
  	logger.debug("Returned "+str(len(r))+" results from "+table)
  	return r
