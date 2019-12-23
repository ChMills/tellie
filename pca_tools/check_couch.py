import os
import couchdb
import getpass

# connect to couch
pw = getpass.getpass("CouchDB password: ")
couchserver = couchdb.Server("http://snoplus:%s@couch.snopl.us" % pw)

# select db
dbname = "telliedb"
db = couchserver[dbname]

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
			if (subruns != 40): 
				print " !!! WRONG NUMBER OF SUBRUNS !!! "
				wrong.append ( run )

	print "List DONE, wrong runs: ", wrong

print "All DONE, wrong runs: ", wrong

