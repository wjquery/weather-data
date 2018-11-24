
import urllib2, re
from bs4 import BeautifulSoup 

url='http://apims.doe.gov.my/v2/'
response = urllib2.urlopen(url)
content = response.read().decode("utf-8")
content = content.replace('\r\n','')
content = content.replace('\t','')
content = content.strip()

matches=re.findall(r'\{latLng\:\[(.*?)\]\,data\:\'(.*?)\'\,\s*options\:\{icon\:\s*\'(.*?)png\'\}\,\}', content, re.DOTALL)
for m in matches:
    latLng = m[0].split(',')
    lat=latLng[0]
    lng=latLng[1]
    soup=BeautifulSoup(m[1],'html.parser') ##blah
    tds=soup.find_all('td')
    val = tds[0].find('h2').text[:-1] #remove *
    city = tds[1].find('h2').text
    datets = tds[1].text[len(city):]
    dateStr = datets.split('-')[0].strip()
    timeStr = datets.split('-')[1].strip()
    print(city,lng, lat, dateStr, timeStr, val)
	#process data

#write to output

