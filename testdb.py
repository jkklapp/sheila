#!/usr/bin/env python
import names,requests,json
from random import randint

while True:
	j = {}
	for i in range(randint(1,10)):
		j[names.get_first_name()]=randint(1,1000)
	print "Trying: "+json.dumps(j)
	try:
		r = requests.post("http://localhost:5000/_insert", data=json.dumps(j))
		print r.text
	except:
		pass
	for i in range(randint(1,10)):
		j[names.get_first_name()]=randint(1,1000)
	print "Trying: "+json.dumps(j)
	try:
		r = requests.post("http://localhost:5000/_query", data=json.dumps(j))
		print r.text
	except:
		pass

