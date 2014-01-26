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
	# table candidate code
	for d in data:
		new = d.keys()
		operation = 'Create'
		# look for target table code
		for key in cst.keys():
			if subset(new,cst[key]) and len(new) <= len(cst[key]):
				operation = 'Insert'
				target = cst[key]
				actual_insert(json.dumps(d), makeTableName(target), be)
				break
			if not disjoin(new,cst[key]):
				tTag,tKeys = getSetWithMostCommonTags(new,cst)
				if len(tTag) == 0 or len(tKeys) == 0:
					continue
				operation = 'Update'
				logging.debug("\nAppending new: "+str(new)+" and existing "+str(tKeys))
				target = list(set(new) | set(tKeys))
				updateTable(tTag, makeTableName(target), cst, be)
				actual_insert(json.dumps(d), makeTableName(target), be)
				break
			#subset(cst[key],new) and len(cst[key]) < len(new):
		if operation == 'Create':
			target = new
			createTable(makeTableName(target), target, cst, be)
			actual_insert(d, makeTableName(target), be)
		
		logging.info("Inserted: "+json.dumps(d)+"\nResulting tables : "+str(cst)+"\nOperation: "+operation+" with target "+str(target))
	return ""

@sheila.route('/_query', methods=['POST'])
def query():
	data = request.data
	try:
		d = json.loads(data)
	except ValueError:
		logging.warning("Error inserting data")
	keys = d.keys()
	tTag,tKeys = getSetWithMostCommonTags(keys,cst)
	if tTag is None or tKeys == []:
		logging.debug("\nNo table for data: "+data)
		return "{}\n"
	logging.debug("\nLooking for "+data+" on "+tTag)
	r=actual_select(d, tTag, be)
	if len(r) > 1:
		ret='{ "results": ['+json.dumps(r[0])
		del r[0]
		for j in r:
			ret+=", "+json.dumps(j)
		return ret+"]}\n"
	else:
		return '{ "results": '+r[0]+'}\n'

if __name__ == '__main__':
	confLogger()
	logging.info("Reading configuration...")
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
	# App start
	logging.info("Starting sheila...")
	be = Backend()
	cst = CodeTable().table
	sheila.run(debug=IConf.debug, host=IConf.host,port=IConf.port)

