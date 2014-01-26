SHEILA DB
==============
ScHema-less rEst Interface for reLAtional DB
--------------

*Sheila enables REST NoSQL database operation on top of a relational database.*

*Version: Alpha 0.1*

Requirements
--------------
1. Python: flask, MySQLdb, pickle, json
2. MySQL: Running server with a database named 'sheila' created.

Getting started
--------------
Edit sheila.cfg
Run ./server.py
Now you can do POST requests to '/_query' and '/_insert' with JSON data.

server.py
--------------
Main code. Initializes connections to relational backend and starts the REST service.

sheila.cfg
--------------

Configuration file. You have to provide values for at least all empty fields.

backend.py
-------------
Primitives to work with the SQL end.

utils.py
------------
Utility functions to make everything work.

TODO
--------------
	* Extend query capabilities to support wild cards (only equivalence
		testing is supported so far).
	* Allow remove and update of data.
	* Explain how Sheila works under the hood.

Author & License
--------------
Author: Jaakko Lappalainen, 2014. email: jkk.lapp@gmail.com

This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>. 

