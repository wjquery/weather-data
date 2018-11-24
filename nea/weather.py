#
# Web crawler for NEA Weather Stations
#
# Note -- requires python-requests package to be installed
#
import re
import urllib
import urllib2
import datetime
import time
from lxml import etree

WeatherParameter={'T':'temperature','H':'heat index','RH':'Relative Humidity','W':'Wind','R':'Rain'}
# Sample URL
# http://www.weather.gov.sg/online/data/hourlyMapData.jsp?timing=30a08a2013%2011b00&paraId=T
#
# the timing is updated hourly
ts=datetime.datetime.now()
#format to the specific format
tstr=ts.strftime('%da%m%Y%Hb00')
tsf=ts.strftime('%Y-%m-%d-%H')
filename = tsf+ WeatherParameter['T']

url='http://www.weather.gov.sg/online/data/hourlyMapData.jsp?timing=%s&paraId=T' % (urllib.quote(tstr),)
#values={'timing':tstr,'paraId':'T'}
#data = urllib.urlencode(values)
#req = urllib2.Request(url, data)
response = urllib2.urlopen(url)
content = response.read().decode("utf-8")
f.close()

#fix the xml bug found, add space 
xml=content.replace('legendPosition',' legendPosition')
xml.strip()

tree = etree.HTML(xml)
nodes = tree.xpath('//markers/defination/marker')
#save to csv/text file
f=open(filename,'w')
for i in range(len(nodes)):
	#write header
	f.write('StationID,X,Y,%s'%WeatherParameter['T'])
	f.write('%s,%s,%s,%s' %(nodes[i].attrib['id'],nodes[i].attrib['x'],nodes[i].attrib['y'],nodes[i].attrib['label'])
f.close()


