import csv
import os
import urllib
import sys
import sqlite3

db=r"db.sqlite"
OutFolder=r"E:\GIS\Pincodes"
url_template=r"http://bhuvan.nrsc.gov.in/governance/tools/postal/get/getpinDetails.php?sno="

if(len(sys.argv)>1):
	State=sys.argv[1]
	print State

	#check if folder exists
	st_folder=os.path.join(OutFolder, State)
	if( not os.path.isdir(st_folder)):
		#make folder
		os.makedirs(st_folder)

	strQuery="Select Distinct(pincode) from pc where statename='{0}'".format(State)
	print strQuery

	#Open DB
	conn=sqlite3.connect(db)
	c=conn.cursor()

	#Get The data
	c.execute(strQuery)
	data=c.fetchall()
	recordCount=len(data)
	print "Found {0} records for {1}".format(recordCount, State)
	conn.close()

	#now let us download them one by one
	done=0

	for d in data:
		pc=str(d[0])
		#print pc
		url=url_template+pc
		out_file=os.path.join(st_folder,pc)
		#now download
		urllib.urlretrieve(url,out_file)
		done=done+1
		print "Finished downloading {0} {1}/{2}".format(pc, done, recordCount)


	#All are done
	print "finished the state"





			