#!/usr/bin/env python
import json
from flask import Flask
from flask import request
from utils import *
from backend import *
from config import BEConf,SConf,IConf
import ConfigParser
import logging

sheila = Flask(__name__)


@sheila.route('/_insert', methods=['POST'])
def insert():
	data = request.data
	try:
		data = json.loads(data)
	except ValueError:
		logging.warning("Error inserting data")
	if type(data) is dict:
		data=[data]
	# table candidate code
	for d in data:
		if type(d) is not dict:
			d=dict(d)
		new = d.keys()
		operation = 'Create'
		# look for target table code
		for key in cst.keys():
			if subset(new,cst[key]) and len(new) <= len(cst[key]):
				operation = 'Insert'
				target = cst[key]
				logging.debug("\nAppending new: "+json.dumps(d)+" on existing "+makeTableName(target))
				actual_insert(json.dumps(d), makeTableName(target), be)
				break
			if not disjoin(new,cst[key]):
				tTag,tKeys = getSetWithMostCommonTags(new,cst)
				if len(tTag) == 0 or len(tKeys) == 0:
					continue
				operation = 'Update'
				logging.debug("\nAppending new: "+str(new)+" and existing "+str(tKeys))
				target = list(set(new) | set(tKeys))
				updateTable(tTag, target, cst, be)
				actual_insert(json.dumps(d), makeTableName(target), be)
				break
			#subset(cst[key],new) and len(cst[key]) < len(new):
		if operation == 'Create':
			target = new
			createTable(makeTableName(target), target, cst, be)
			actual_insert(json.dumps(d), makeTableName(target), be)
		
		logging.info("Inserted: "+json.dumps(d)+"\nResulting tables : "+str(cst)+"\nOperation: "+operation+" with target "+str(target))
	return ""

@sheila.route('/_query', methods=['POST'])
def query():
	data = request.data
	try:
		d = json.loads(data)
	except ValueError:
		logging.warning("Error querying data")
	keys = d.keys()
	#tTag,tKeys = getSetWithMostCommonTags(keys,cst)
	tKeys = getCommonSets(keys,cst)
	if tKeys == []:
		logging.debug("\nNo table for data: "+data)
		return "{}\n"
	logging.debug("\nLooking for "+data+" on tables: "+str(tKeys))
	ret = []
	for tTag in tKeys:
		partial=actual_select(d, tTag, be)
		for p in partial:
			ret.append(p)
	return json.dumps(ret)+"\n"

if __name__ == '__main__':
	# Configuration
	config = ConfigParser.RawConfigParser()
	config.read('sheila.cfg')
	BEConf.port = config.getint('BE', 'port')
	BEConf.host = config.get('BE', 'host')
	BEConf.user = config.get('BE', 'user')
	BEConf.passwd = config.get('BE', 'pass')
	BEConf.db = config.get('BE', 'db')
	IConf.host=config.get('Interface', 'host')
	IConf.port=config.getint('Interface', 'port')
	IConf.debug=config.get('Interface', 'debug')
	SConf.cstfile=config.get('Sheila','cstfile')
	LConf.level=config.get('Log','level')
	confLogger()
	logging.info("Reading configuration...")
	# App start
	logging.info("Starting sheila...")
	be = Backend()
	cst = CodeTable().table
	sheila.run(debug=IConf.debug, host=IConf.host,port=IConf.port)

