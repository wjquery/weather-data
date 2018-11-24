# coding: utf8
import locale
#/usr/bin/python3

from urllib import request, parse
from datetime import datetime, timedelta
import json
import os


MAIN_URL='http://www.sgqx.gov.cn/monitor/auto-monitor!getGongzhongByElement.action'
MAIN_TIME_RANGE_URL='http://www.sgqx.gov.cn/monitor/auto-monitor!getDateTimeRange.action'
RIGHT_PLOT_URL='http://www.sgqx.gov.cn/monitor/auto-monitor!getZidongChartDatas.action'
DOWNLOAD_DIR='data'

'''
postData={
	'element': 't2mmMax', 
	'dataType': 'country',
	'datetime': '2018-11-24%2013:24:00' #format YYYY-MM-DD HH:mm:ss
}

postDataRightBar = {

siteNo: 59082
dataType: rainShik
siteType: country

siteNo: 59082
dataType: rain24hour
siteType: country


	siteNo: 59082
	dataType: visibility
	siteType: country

	siteNo: 59082
dataType: wind
siteType: country
}
'''

'''
element
气温
- t2mmMax 最高气温, 
t2mmMin: 最低气温， 
t2mm: 实时气温

雨量
- rainShik : 实况雨量
- rain24hour ： 日雨量

能见度
- visibility: 能见度
siteNo: 59082

'''

def readLastJobDone():
	with open('jobs.data','r') as jobfile:
		line = jobfile.readline()
		try:
			lastJobDoneDt = datetime.strptime(line, '%Y-%m-%d %H:%M:%S')
			return lastJobDoneDt
		except:
			print('no ')
		return None

def readLastRadarDt():
	locale.setlocale(locale.LC_ALL,'zh_CN.UTF-8')
	with open('radarTime.dat','r') as jobfile:
		line = jobfile.readline()
		try:
			line = line.replace(u'年','-').replace(u'月','-').replace(u'日','')
			print(line)
			lastJobDoneDt = datetime.strptime(line, '%Y-%m-%d %H:%M')
			return lastJobDoneDt
		except Exception as e:
			print(e)
		return None

def writeLastJobDone(lastJobDoneDt):
	with open('jobs.data','w') as jobfile:
		return jobfile.write(lastJobDoneDt.strftime('%Y-%m-%d %H:%M:%S'))


def fetchData(dataType, reqDtStr, downloadDir=DOWNLOAD_DIR):
	reqDtStr = reqDt.strftime('%Y-%m-%d %H:%M:00')
	reqDtFile = reqDt.strftime('%Y%m%d%H%M00')
	data = {
		'element':ELEMENTS[dataType],
		'dataType':'country',
		'datetime':  reqDtStr
	}

	print(data)
	postData  = bytes( parse.urlencode( data ).encode() )

	req = request.Request(MAIN_URL, data=postData)
	resp = request.urlopen(req)
	content = resp.read().decode('utf-8')
	jsonData = json.loads(content)

	print(jsonData)

	rows=[]
	rowHeader=[]
	rowHeader.extend(BASE_DATA)
	rowHeader.extend(ELEMENTS_DATA[dataType])

	for dataItem in jsonData['datas']:
		row=[]
		row.append(dataItem['time'])
		row.append(dataItem['no'])
		row.append(dataItem['name'])
		row.append(dataItem['lon'])
		row.append(dataItem['lat'])
		row.append(dataItem['humidity'])
		if dataType == 'temp':
			row.append(dataItem['t2mm'])
			row.append(dataItem['t2mmMin'])
			row.append(dataItem['t2mmMax'])
		elif dataType == 'rain':
			row.append(dataItem['rainShik'])
			row.append(dataItem['rain24hour'])
		elif dataType == 'wind':
			row.append(dataItem['windDir'])
			row.append(dataItem['wind1hDir'])
			row.append(dataItem['windSpeed'])
			row.append(dataItem['wind1hSpeed'])
			row.append(dataItem['windSpeedValue'])
			row.append(dataItem['wind1hSpeedValue'])
		elif dataType == 'visibility':
			row.append(dataItem['value'])
		else:
			print('invalid dataType')
			pass
		rows.append(row)

	import csv
	csvFile = os.path.join(downloadDir,dataType+'_'+reqDtFile+'.csv')
	with open(csvFile, 'w', newline='', encoding='utf-8-sig') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(rowHeader)
		for row in rows:
			spamwriter.writerow(row)


def fetchDatum(reqDt):
	fetchData('temp', reqDt)
	fetchData('rain', reqDt)
	fetchData('wind', reqDt)
	#visiblity data update every hour
	if reqDt.minute == 0:
		fetchData('visibility', reqDt)
	writeLastJobDone(reqDt)

ELEMENTS = {
	'temp':'t2mm',
	'rain':'rainShik',
	'wind':'wind',
	'visibility':'visibility'
}

BASE_DATA=['time', 'no','name','lon','lat','humidity']
#温度
TEMP_DATA=['t2mm','t2mmMin','t2mmMax']
#雨量
RAIN_DATA=['rainShik','rain24hour']
#风向分速度
WIND_DATA=['windDir','win1hDir','windSpeed','wind1hSpeed','windSpeedValue','wind1hSpeedValue']
#能见度
VISIBILITY_DATA=['visibility']

ELEMENTS_DATA = {
	'temp':TEMP_DATA,
	'rain':RAIN_DATA,
	'wind':WIND_DATA,
	'visibility':VISIBILITY_DATA
}


now = datetime.now()
#检查网页的radarTime，有可能数据没更新

#数据6分钟更新一次
#导入最后一次数据更新的时间，如果没，则从当前小时00分开始
#
lastJobDoneDt = readLastJobDone()
radarTimeDt = readLastRadarDt()
if radarTimeDt is None:
	print('No radarTime found')
	import sys
	sys.exit(-1)

if lastJobDoneDt is not None :
	reqDt = lastJobDoneDt + timedelta(minutes=6)
	while reqDt <= radarTimeDt:
		#repeat the download process
		fetchDatum(reqDt)
		reqDt = reqDt + timedelta(minutes=6)
else:
	reqDt = datetime(radarTimeDt.year, radarTimeDt.month, radarTimeDt.day, radarTimeDt.hour, radarTimeDt.minute,0,0)
	fetchDatum(reqDt)






