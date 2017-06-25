from __future__ import print_function
from bs4 import BeautifulSoup
import os
import sqlite3
import re


dataDir=r"Data"
db=r"processed.sqlite"

def ExtractPincode(name):
	p=re.compile(r"\d{6}")
	matches=p.findall(name)
	if(len(matches)<1):
		return ""
	else:
		return matches[0]

def parseCode(code):
	#assume that data is something like this:
	#addpostpopup("241132","nm",16.2423266,77.6194372)

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
	with open(path, 'rb') as file:
		parsedData=[]
		data=file.read()
		soup=BeautifulSoup(data,"html.parser")
		tb=soup.find('table')
		if tb is not None:
			rows=tb.find_all('tr')

			for r in rows:
				po=r.find('td')
				
				if(po is not None):
					po_name=po.text.strip()
					code=po.attrs['onclick']
					#The code needs to be parsed
					po_data=parseCode(code)
					#extract Pincode
					pin_code=ExtractPincode(po_name)
					#append postoffice name
					po_data.insert(0,po_name)
					#append pincode
					po_data.insert(1, pin_code)
					#add to parsed data
					parsedData.append(tuple(po_data))
				else:
					print(path)
	#now retun
	return parsedData


def createTable(db):
	conn=sqlite3.connect(db)
	query='CREATE  TABLE  IF NOT EXISTS "main"."postoffice" ("Name" TEXT, "State" TEXT, "pincode" TEXT NOT NULL , "po_code" TEXT NOT NULL ,"mode" TEXT,  "lat" NUMERIC, "lng" NUMERIC, CONSTRAINT name_unique UNIQUE(po_code))'
	c=conn.cursor()
	c.execute(query)
	conn.commit()
	conn.close()

def saveData(conn, records):
	#print records
	c=conn.cursor()
	#the bbc_lat & lng are flipped, because that's how it is in the code
	insertQuery="INSERT OR IGNORE INTO postoffice ('Name', 'State', 'pincode', 'po_code','mode', 'lat', 'lng')    VALUES (?,?,?,?,?,?,?)"
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
	#if os.path.isdir(full_path):
	dirs.append(full_path)
index=0
if (len(dirs)>0):
	#create table
	createTable(db)
	
	for  f in dirs:
		#print f
		print("Processing {0} of {1}".format(index, len(dirs)), end='\r')
		conn=sqlite3.connect(db)
		#file_path=os.path.join(d, f)
		#print file_path
		#Get the data in this file
		records=readFile(f)
		#print records
		#break
		#add State 
		#records=AddState(records, os.path.basename(d))
		records=AddState(records, "")

		#save these records
		saveData(conn, records)
		conn.close()
		index +=1

#finished everything
print ("Finished saving all")



