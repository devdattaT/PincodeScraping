from bs4 import BeautifulSoup
import os
import sqlite3

dataDir=r"E:\GIS\Pincodes\Data"
db=r"E:\GIS\Pincodes\processed.sqlite"

def parseCode(code):
	#assume that data is something like this:
	#addpostpopup("241132","nm",16.2423266,77.6194372),zoom_to_centre(77.6194372,16.2423266,7)

	#remove addpostpopup
	code=code.replace('addpostpopup(', '')
	#remove zoom_to_centre
	code=code.replace('zoom_to_centre(', '')
	#remove closing brackets
	code=code.replace(')', '')
	#remove "
	code=code.replace('"', '')
	
	data=code.split(',')
	return data

def readFile(path):
	pin_code=os.path.basename(path)
	with open(path, 'rb') as file:
		parsedData=[]
		data=file.read()
		soup=BeautifulSoup(data,"html.parser")
		tb=soup.find('table')
		if tb is not None:
			rows=tb.find_all('tr')

			for r in rows:
				po=r.find('td')
				po_name=po.text.strip()
				code=po.attrs['onclick']
				#The code needs to be parsed
				po_data=parseCode(code)

				#append postoffice name
				po_data.insert(0,po_name)
				#append pincode
				po_data.insert(1, pin_code)
				#add to parsed data
				parsedData.append(tuple(po_data))
	#now retun
	return parsedData


def createTable(db):
	conn=sqlite3.connect(db)
	query='CREATE  TABLE  IF NOT EXISTS "main"."postoffice" ("Name" TEXT, "State" TEXT, "pincode" TEXT NOT NULL , "po_code" TEXT NOT NULL ,"mode" TEXT,  "lat" NUMERIC, "lng" NUMERIC, "bbc_lat" NUMERIC, "bbc_lng" NUMERIC, "zoom" NUMERIC)'
	c=conn.cursor()
	c.execute(query)
	conn.commit()
	conn.close()

def saveData(conn, records):
	c=conn.cursor()
	#the bbc_lat & lng are flipped, because that's how it is in the code
	insertQuery="INSERT INTO postoffice ('Name', 'State', 'pincode', 'po_code','mode', 'lat', 'lng', 'bbc_lng','bbc_lat', 'zoom')    VALUES (?,?,?,?,?,?,?,?,?,?)"
	c.executemany(insertQuery, records)
	conn.commit()

def AddState(records, state):
	modifiedRecords=[]
	for r in records:
		data=list(r)
		data.insert(1, state)
		modifiedRecords.append(data)

	return modifiedRecords



#iterate over the folder and get the directories
dirs=[]
parts=os.listdir(dataDir)
for p in parts:
	full_path=os.path.join(dataDir, p)
	if os.path.isdir(full_path):
		dirs.append(full_path)

if (len(dirs)>0):
	#create table
	createTable(db)
	
	for  d in dirs:
		print "Reading {0}".format(d)
		#Get all the files in this directory
		files=os.listdir(d)
		#open database
		conn=sqlite3.connect(db)

		for f in files:
			file_path=os.path.join(d, f)

			#Get the data in this file
			records=readFile(file_path)

			#add State 
			records=AddState(records, os.path.basename(d))

			#save these records
			saveData(conn, records)
		conn.close()

#finished everything
print "Finished saving all"



