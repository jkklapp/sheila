import MySQLdb,pickle,json
from config import BEConf, SConf
import logging
from utils import *

class Backend:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		logging.info("Connecting to DB...")
		self.conn = MySQLdb.connect(host=BEConf.host, port=BEConf.port, user=BEConf.user, passwd=BEConf.passwd, db=BEConf.db)
		logging.info("DB Online.")

def createTable(name, keys, cst, be):
	c = be.conn.cursor()
	try:
		c.execute("CREATE TABLE "+name+" ( id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, data TEXT NOT NULL )")
		be.conn.commit()
	except Exception as e:
		logging.critical(e)
		be.conn.rollback()
	cst[name]=keys
	pickle.dump(cst,open(SConf.cstfile,'w'))


def updateTable(old, new, cst, be):
	'''Change table name '''
	c = be.conn.cursor()
	try:
		c.execute("ALTER TABLE "+old+" RENAME TO "+new)
		be.conn.commit()
	except Exception as e:
		logging.critical(e)
		be.conn.rollback()
	cst[new]=cst[old]
	del cst[old]
	pickle.dump(cst,open(SConf.cstfile,'w'))

def actual_insert(data, table, be):
	# Actual data insertion
	c = be.conn.cursor()
	try:
		c.execute("INSERT INTO "+table+"(data) VALUES (%s)",(str(data)))
		be.conn.commit()
	except Exception as e:
		logging.critical(e)
		be.conn.rollback()


def actual_select(data, table, be):
	f = 'equal'
 	c = be.conn.cursor()
 	# current duplicate-free policy on queries
	c.execute("SELECT DISTINCT data FROM "+table)
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
  	return r
