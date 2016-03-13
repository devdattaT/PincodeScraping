from bs4 import BeautifulSoup
f1=open(r"E:\GIS\Pincodes\Goa\403001")
data=f1.read()
soup=BeautifulSoup(data,"html.parser")
tb=soup.find('table')
rows=tb.find_all('tr')
for r in rows:
	po=r.find('td')
	po_name=po.text.strip()
	code=po.attrs['onclick']
	print "For {0} Code is: {1}".format(po_name, code)