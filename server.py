#!/usr/bin/env python
import json
from flask import Flask
from flask import request
from utils import *
from backend import *
from config import SConf,BEConf,LConf,IConf
import logging

sheila = Flask(__name__)

@sheila.route('/_insert', methods=['POST'])
def insert():
	logger = logging.getLogger("sheila")
	data = request.data
	try:
		data = json.loads(data)
	except ValueError:
		logger.warning("Error inserting data")
	if type(data) is dict:
		data=[data]
	# table candidate code
	for d in data:
		if type(d) is not dict:
			d=dict(d)
		new = d.keys()
		operation = 'Create'
		# look for target table code
		for key in cst.tables():
			if subset(new,cst.get(key)) and len(new) <= len(cst.get(key)):
				operation = 'Insert'
				#target = cst.get(key)
				tTag,tKeys = getSetWithMostCommonTags(new,cst)
				target=tTag
				actual_insert(json.dumps(d), target, be)
				break
			if not disjoin(new,cst.get(key)):
				tTag,tKeys = getSetWithMostCommonTags(new,cst)
				if len(tTag) == 0 or len(tKeys) == 0:
					continue
				operation = 'Update'
				new = list(set(new) | set(tKeys))
				#target=makeTableName(new)
				target=tTag
				updateTable(target, new, cst, be)
				actual_insert(json.dumps(d), tTag, be)
				break
			#subset(cst.get(key),new) and len(cst.get(key)) < len(new):
		if operation == 'Create':
			target = makeTableName(new)
			createTable(target, new, cst, be)
			actual_insert(json.dumps(d), target, be)
		
		logger.debug("Inserted: "+json.dumps(d)+"\nResulting tables : "+printCST(cst)+"\nOperation: "+operation+" "+target)
	return ""

@sheila.route('/_query', methods=['POST'])
def query():
	logger = logging.getLogger("sheila")
	data = request.data
	try:
		d = json.loads(data)
	except ValueError:
		logger.warning("Error querying data")
	keys = d.keys()
	#tTag,tKeys = getKeysAsSetetWithMostCommonTags(keys,cst)
	tKeys = getCommonSets(keys,cst)
	if tKeys == []:
		logger.debug("\nNo table for data: "+data)
		return "[]\n"
	ret = []
	for tTag in tKeys:
		partial=actual_select(d, tTag, be)
		for p in partial:
			ret.append(p)
	return json.dumps(ret)+"\n"

if __name__ == '__main__':
	beconf = BEConf()
	iconf = IConf()
	sconf = SConf()
	lconf = LConf()
	confLogger(lconf)
	logger = logging.getLogger("sheila")
	if sconf.clear:
		clearEnvironment(sconf,beconf)
	logger.info("Reading configuration...")
	# App start
	logger.info("Starting sheila...")
	be = Backend(beconf)
	cst = CodeTable(sconf)
	sheila.run(debug=iconf.debug, host=iconf.host,port=iconf.port)

