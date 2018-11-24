#!/usr/bin/python2.6
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

'''
==== TMP DATA API ======
URL: http://www.weather.gov.sg/weather-currentobservations-temperature

    
==== TMP IMAGE API ======
URL: 
- http://www.weather.gov.sg/files/isotherm/isotherm.png?time=2015-07-10 16:54:59

var map_latitude_top = 1.516;		 
		  var map_longitude_left = 103.572;
		  var map_latitude_bottom = 1.11;		 
		  var map_longitude_right = 104.253;

'''


stations = {};
stations["S06"] = "Paya Lebar";stations["S07"] = "Macritchie Reservoir";stations["S08"] = "Lower Peirce Reservoir";stations["S101"] = "Jurong (North)";
stations["S102"] = "Semakau Island";stations["S104"] = "Admiralty";stations["S105"] = "Admiralty West";stations["S106"] = "Pulau Ubin";
stations["S107"] = "East Coast Parkway";stations["S108"] = "Marina Barrage";stations["S109"] = "Ang Mo Kio";stations["S11"] = "Choa Chu Kang (West)";stations["S110"] = "Serangoon North";
stations["S111"] = "Newton";stations["S112"] = "Lim Chu Kang";stations["S113"] = "Marine Parade";stations["S114"] = "Choa Chu Kang (Central)";stations["S115"] = "Tuas South";
stations["S116"] = "Pasir Panjang";stations["S117"] = "Jurong Island";stations["S118"] = "Dhoby Ghaut";stations["S119"] = "Nicoll Highway";stations["S120"] = "Botanic Garden";
stations["S121"] = "Choa Chu Kang (South)";stations["S122"] = "Khatib";stations["S123"] = "Whampoa";stations["S23"] = "Tengah";stations["S24"] = "Changi";stations["S25"] = "Seletar";
stations["S29"] = "Pasir Ris (West)";stations["S31"] = "Kampong Bahru";stations["S33"] = "Jurong Pier";stations["S35"] = "Ulu Pandan";stations["S36"] = "Serangoon";
stations["S39"] = "Jurong (East)";stations["S40"] = "Mandai";stations["S43"] = "Tai Seng";stations["S44"] = "Jurong (West)";stations["S46"] = "Upper Thomson";stations["S50"] = "Clementi";
stations["S55"] = "Buangkok";stations["S60"] = "Sentosa Island";stations["S61"] = "Chai Chee";stations["S63"] = "Boon Lay (West)";stations["S64"] = "Bukit Panjang";
stations["S66"] = "Kranji Reservoir";stations["S69"] = "Upper Peirce Reservoir";stations["S71"] = "Kent Ridge";stations["S72"] = "Tanjong Pagar";stations["S77"] = "Queenstown";
stations["S78"] = "Tanjong Katong";stations["S79"] = "Somerset (Road)";stations["S80"] = "Sembawang";stations["S81"] = "Punggol";stations["S82"] = "Tuas West";stations["S84"] = "Simei";
stations["S86"] = "Boon Lay (East)";stations["S88"] = "Toa Payoh";stations["S89"] = "Tuas";stations["S90"] = "Bukit Timah";stations["S91"] = "Yishun";stations["S92"] = "Buona Vista";
stations["S94"] = "Pasir Ris (Central)";
stations_geo=[]
stations_geo.append( {'station_code':"S07",'latitude':"1.34180000",'longitude':"103.83390000"});
stations_geo.append( {'station_code':"S08",'latitude':"1.37003333",'longitude':"103.82706667"});
'''//TODO
stations_geo[2] = {'station_code':"S104",
'latitude':"1.44386667",
'longitude':"103.78538333"};stations_geo[3] = {'station_code':"S105",
'latitude':"1.45816667",
'longitude':"103.79525000"};stations_geo[4] = {'station_code':"S106",
'latitude':"1.41680000",
'longitude':"103.96730000"};stations_geo[5] = {'station_code':"S108",
'latitude':"1.27991667",
'longitude':"103.87030000"};stations_geo[6] = {'station_code':"S109",
'latitude':"1.37926667",
'longitude':"103.85001667"};stations_geo[7] = {'station_code':"S11",
'latitude':"1.37425000",
'longitude':"103.69373333"};stations_geo[8] = {'station_code':"S110",
'latitude':"1.36531667",
'longitude':"103.87076667"};stations_geo[9] = {'station_code':"S111",
'latitude':"1.31055000",
'longitude':"103.83650000"};stations_geo[10] = {'station_code':"S112",
'latitude':"1.43880000",
'longitude':"103.70173333"};stations_geo[11] = {'station_code':"S113",
'latitude':"1.30501667",
'longitude':"103.91121667"};stations_geo[12] = {'station_code':"S114",
'latitude':"1.38208333",
'longitude':"103.73810000"};stations_geo[13] = {'station_code':"S115",
'latitude':"1.28840000",
'longitude':"103.63790000"};stations_geo[14] = {'station_code':"S116",
'latitude':"1.28235000",
'longitude':"103.75450000"};stations_geo[15] = {'station_code':"S117",
'latitude':"1.25600000",
'longitude':"103.67900000"};stations_geo[16] = {'station_code':"S118",
'latitude':"1.29940000",
'longitude':"103.84606667"};stations_geo[17] = {'station_code':"S119",
'latitude':"1.29503333",
'longitude':"103.86218333"};stations_geo[18] = {'station_code':"S120",
'latitude':"1.30871667",
'longitude':"103.81801667"};stations_geo[19] = {'station_code':"S122",
'latitude':"1.41725000",
'longitude':"103.82513333"};stations_geo[20] = {'station_code':"S123",
'latitude':"1.32141667",
'longitude':"103.85765000"};stations_geo[21] = {'station_code':"S24",
'latitude':"1.36776667",
'longitude':"103.98226667"};stations_geo[22] = {'station_code':"S29",
'latitude':"1.38650000",
'longitude':"103.94133333"};stations_geo[23] = {'station_code':"S31",
'latitude':"1.27431667",
'longitude':"103.82816667"};stations_geo[24] = {'station_code':"S33",
'latitude':"1.30818333",
'longitude':"103.70986667"};stations_geo[25] = {'station_code':"S35",
'latitude':"1.33246667",
'longitude':"103.75498333"};stations_geo[26] = {'station_code':"S36",
'latitude':"1.33765000",
'longitude':"103.86615000"};stations_geo[27] = {'station_code':"S40",
'latitude':"1.40665000",
'longitude':"103.78320000"};stations_geo[28] = {'station_code':"S43",
'latitude':"1.34061667",
'longitude':"103.88816667"};stations_geo[29] = {'station_code':"S44",
'latitude':"1.34523333",
'longitude':"103.68333333"};stations_geo[30] = {'station_code':"S46",
'latitude':"1.34155000",
'longitude':"103.81078333"};stations_geo[31] = {'station_code':"S50",
'latitude':"1.33178333",
'longitude':"103.77611667"};stations_geo[32] = {'station_code':"S55",
'latitude':"1.38358333",
'longitude':"103.88603333"};stations_geo[33] = {'station_code':"S60",
'latitude':"1.25040000",
'longitude':"103.82753333"};stations_geo[34] = {'station_code':"S61",
'latitude':"1.32710000",
'longitude':"103.92065000"};stations_geo[35] = {'station_code':"S63",
'latitude':"1.32746667",
'longitude':"103.70416667"};stations_geo[36] = {'station_code':"S64",
'latitude':"1.38228333",
'longitude':"103.76066667"};stations_geo[37] = {'station_code':"S66",
'latitude':"1.43866667",
'longitude':"103.73601667"};stations_geo[38] = {'station_code':"S69",
'latitude':"1.37035000",
'longitude':"103.80463333"};stations_geo[39] = {'station_code':"S71",
'latitude':"1.29230000",
'longitude':"103.78150000"};stations_geo[40] = {'station_code':"S72",
'latitude':"1.27388333",
'longitude':"103.84823333"};stations_geo[41] = {'station_code':"S77",
'latitude':"1.29360000",
'longitude':"103.81268333"};stations_geo[42] = {'station_code':"S78",
'latitude':"1.30703333",
'longitude':"103.89066667"};stations_geo[43] = {'station_code':"S79",
'latitude':"1.30040000",
'longitude':"103.83720000"};stations_geo[44] = {'station_code':"S81",
'latitude':"1.40285000",
'longitude':"103.90948333"};stations_geo[45] = {'station_code':"S82",
'latitude':"1.32480000",
'longitude':"103.63520000"};stations_geo[46] = {'station_code':"S84",
'latitude':"1.34428333",
'longitude':"103.94405000"};stations_geo[47] = {'station_code':"S86",
'latitude':"1.32686667",
'longitude':"103.72046667"};stations_geo[48] = {'station_code':"S88",
'latitude':"1.34171667",
'longitude':"103.85150000"};stations_geo[49] = {'station_code':"S89",
'latitude':"1.31985000",
'longitude':"103.66131667"};stations_geo[50] = {'station_code':"S90",
'latitude':"1.31910000",
'longitude':"103.81928333"};stations_geo[51] = {'station_code':"S91",
'latitude':"1.42993333",
'longitude':"103.83061667"};stations_geo[52] = {'station_code':"S92",
'latitude':"1.28408333",
'longitude':"103.78875000"};stations_geo[53] = {'station_code':"S94",
'latitude':"1.36793333",
'longitude':"103.94898333"};   
'''

'''
basic flow
1. Get url and do regex to retrieve the observation time

2. Get the basemap for 30min, 60min, 120mins, midnight according to IMAGE API, save as png

3. Get the station data according to DATA API, save as csv (named obstime) with following format
StationID, Time, Value

4.
'''


import sys
url='http://www.weather.gov.sg/weather-currentobservations-temperature'
req = urllib2.Request(url)
response = urllib2.urlopen(req)

html_doc = response.read()
response.close()
m=re.search(r"http://www.weather.gov.sg/files/isotherm/isotherm.png\?time=(.*)\'",html_doc,flags=re.M)
if m is not None:
    obv_time = m.group(1)
    from bs4 import BeautifulSoup
    file="%s-temp.csv" %(obv_time.replace(':','').replace(' ','_'),)
    soup=BeautifulSoup(html_doc,'html.parser')
    fcsv=open(file,'w')
    fcsv.write("Station, Value \n")
    spans=soup.find_all('span',class_="sgr")
    for span in spans:
        stdid = span['id']
        stdval = span.string
        fcsv.write("%s, %s\n" %(stdid, stdval))
    fcsv.close()
else:
    print "Error"
    sys.exit(-1)
print obv_time

    
    


