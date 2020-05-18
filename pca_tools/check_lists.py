import os
from env import *

lists = []
all_missing = []
for file in os.listdir("."):
    if file.endswith(".list"):
	lists.append( file )

lists.sort()

for list in lists:
	missing = []
	with open(list) as f:
    		content = f.readlines()
		content = [x.strip() for x in content]
		max_run = max(content)
		min_run = min(content)

		# check whether the file is stored at feyman
		path = feynman_path

		for run in content:
			file_string = "SNOP_0000%s_000.zdab" % run
			full_string = path + "/" + file_string
			if os.path.exists(full_string):
				print "File " + file_string + " exists."
			else:
				print "File " + file_string + " is missing!!!"
				missing.append ( file_string )
				all_missing.append ( file_string )


	print "List: ", list
	print "Runs: ", len(content)
	print "Range: " +min_run, "-", max_run
	print "Missing runs: ", missing
	print ""

print "All missing runs: ", all_missing
