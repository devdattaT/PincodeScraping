import csv
import os
import urllib
import sys
import sqlite3

db=r"db.sqlite"
OutFolder=r"E:\GIS\Pincodes"
url_template=r"http://bhuvan.nrsc.gov.in/governance/tools/postal/get/getpinDetails.php?sno="


def downloadState(state):
	#check if folder exists
	st_folder=os.path.join(OutFolder, state)
	if( not os.path.isdir(st_folder)):
		#make folder
		os.makedirs(st_folder)

	strQuery="Select Distinct(pincode) from pc where statename='{0}'".format(state)
	print strQuery

	#Open DB
	conn=sqlite3.connect(db)
	c=conn.cursor()

	#Get The data
	c.execute(strQuery)
	data=c.fetchall()
	recordCount=len(data)
	print "Found {0} records for {1}".format(recordCount, state)
	conn.close()

	#now let us download them one by one
	index=0

	for d in data:
		pc=str(d[0])
		#print pc
		url=url_template+pc
		out_file=os.path.join(st_folder,pc)
		index=index+1
		#now download
		try:
			urllib.urlretrieve(url,out_file)
			print "Finished downloading {0} {1}/{2}".format(pc, index, recordCount)
		except:
			pass


	#All are done
	print "finished the downloading data for: {0}".format(state)


if(len(sys.argv)>1):
	st=sys.argv[1]
	print st
	downloadState(st)
else:
	print "No state has been provided. Downloading data for all states."
	#we need to download for all states
	query="Select Distinct(statename) from pc"
	conn=sqlite3.connect(db)
	c=conn.cursor()

	#Get The data
	c.execute(query)
	data=c.fetchall()
	recordCount=len(data)
	print "Found {0} records for States".format(recordCount)
	conn.close()

	#now iterate
	for d in data:
		st=str(d[0])
		print "Downloading data for: {0}".format(st)
		downloadState(st)



	





			