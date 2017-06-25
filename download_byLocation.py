import csv
import os
import urllib
import sys
import sqlite3

OutFolder=r"data"
url_template=r"https://bhuvan.nrsc.gov.in/governance/tools/postal_rwd/get/getpinsearchDetails.php?sno="

input_file="input.csv"

def download(lat,lng, id):
    out_file=os.path.join(OutFolder, str(id)+".html")
    url=url_template+str(lng)+'_'+str(lat)+'_75'
    try:
        urllib.urlretrieve(url,out_file)  
    except:
        pass
        
        
def DownloadFrom(start):
    index=0
    with open(input_file, 'rb') as f:
        reader = csv.reader(f)
        for r in reader:
            print index,r
            if index>=start:
                #Now we need to read inputs & download data for that lat long
                download(r[1],r[2], index)
            else:
                print "Still less"
            index+=1
            
                
    
if(len(sys.argv)>1):
	startIndex=int(sys.argv[1])
	print startIndex
	DownloadFrom(startIndex)
else:
    DownloadFrom(1)