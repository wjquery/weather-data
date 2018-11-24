#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup 

url='http://bmkg.go.id/BMKG_Pusat/Kualitas_Udara/Informasi_Partikulat.bmkg'
response = urllib2.urlopen(url)
content = response.read().decode("utf-8")
soup = BeautifulSoup(content,'html.parser')

doms=['modal-pekanbaru','modal-jambi','modal-palembang','modal-batam','modal-indrapuri','modal-pontianak','modal-banjarbaru'
,'modal-samarinda','modal-palangkaraya','modal-kemayoran','modal-cibeureum']

for city in doms:
    print "city: ",city[6:]
    dc = soup.find('div',class_=city)
    datestr = dc.find('h4').string.split(':')
    city_date = datestr[1].strip()
    print city_date
    datum = dc.find('div',class_='modal-body').get_text(separator="\n").split('\n')
    for dataline in datum:
        data = dataline.split(',')
        if len(data) == 2:
            city_name = data[0]
            city_timeval = data[1]
            city_time = city_timeval.split(':')[0]
            city_val = city_timeval.split(':')[1]
            print (city_name, city_time, city_val)
	
#output to file

