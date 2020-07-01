import os
import couchdb
import getpass
from env import *

# connect to couch
pw = getpass.getpass("CouchDB password: ")
couchserver = couchdb.Server("http://" + db_username + ":" + pw + "@" + db_address)

# select db
db = couchserver[db_name]

lists = []
wrong = []
for file in os.listdir("."):
    if file.endswith(".list"):
	lists.append( file )

lists.sort()

for list in lists:
	missing = []
	with open(list) as f:
    		content = f.readlines()
		content = [x.strip() for x in content]

	print "List: ", list
	print "Runs: ", len(content)

	# load run, connect to db
	for run in content:
		print run

		for item in db.view('_design/runs/_view/run_by_number', startkey=int(run), endkey=int(run)):
    			id = item.id
			subruns = len(db[id]['sub_run_info'])
			print "Subruns in couchdb: ", subruns
			if (subruns != n_subruns):
				print " !!! WRONG NUMBER OF SUBRUNS !!! "
				wrong.append ( run )

	print "List DONE, wrong runs: ", wrong

print "All DONE, wrong runs: ", wrong
