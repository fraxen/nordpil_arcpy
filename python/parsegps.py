# coding=utf-8
import EXIF
import sys,os
import time
import codecs
import Image

# {{{ FUNCTIONS

def DmsToDecimal(degree_num, degree_den, minute_num, minute_den,
                 second_num, second_den):
  """Converts the Degree/Minute/Second formatted GPS data to decimal degrees.

  Args:
    degree_num: The numerator of the degree object.
    degree_den: The denominator of the degree object.
    minute_num: The numerator of the minute object.
    minute_den: The denominator of the minute object.
    second_num: The numerator of the second object.
    second_den: The denominator of the second object.

  Returns:
    A deciminal degree.
  """

  degree = float(degree_num)/float(degree_den)
  minute = float(minute_num)/float(minute_den)/60
  second = float(second_num)/float(second_den)/3600
  return degree + minute + second


def GetGps(data):
  """Parses out the GPS coordinates from the file.

  Args:
    data: A dict object representing the EXIF headers of the photo.

  Returns:
    A tuple representing the latitude, longitude, and altitude of the photo.
  """

  lat_dms = data['GPS GPSLatitude'].values
  long_dms = data['GPS GPSLongitude'].values
  latitude = DmsToDecimal(lat_dms[0].num, lat_dms[0].den,
                          lat_dms[1].num, lat_dms[1].den,
                          lat_dms[2].num, lat_dms[2].den)
  longitude = DmsToDecimal(long_dms[0].num, long_dms[0].den,
                           long_dms[1].num, long_dms[1].den,
                           long_dms[2].num, long_dms[2].den)
  if data['GPS GPSLatitudeRef'].printable == 'S': latitude *= -1
  if data['GPS GPSLongitudeRef'].printable == 'W': longitude *= -1
  altitude = None

  try:
    alt = data['GPS GPSAltitude'].values[0]
    altitude = alt.num/alt.den
    if data['GPS GPSAltitudeRef'] == 1: altitude *= -1

  except KeyError:
    altitude = 0
  
  return latitude, longitude, altitude
# }}}

outFile = codecs.open ('out.kml',encoding='utf-8', mode='w')

ep={
	"vardshus": {'startTime': time.strptime('2010-09-20 01:00',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-25 08:00',"%Y-%m-%d %H:%M"), 'text': u'Blidö Värdshus (inkl. foton från bilresan'},
	"innan": {'startTime': time.strptime('2010-09-25 01:00',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-25 10:47',"%Y-%m-%d %H:%M"), 'text': u'Förbedelser inför avfärd'},
	"etappl1": {'startTime': time.strptime('2010-09-25 10:47',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-25 12:55',"%Y-%m-%d %H:%M"), 'text': u'Stämmarsund - Brännäsören (Etapp 1, lördag)'},
	"lunchl": {'startTime': time.strptime('2010-09-25 12:55',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-25 13:38',"%Y-%m-%d %H:%M"), 'text': u'Lördag lunch (Brännäsören)'},
	"etappl2": {'startTime': time.strptime('2010-09-25 13:38',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-25 16:23',"%Y-%m-%d %H:%M"), 'text': u'Brännäsören - Vidinge (Etapp 2, lördag)'},
	"talt": {'startTime': time.strptime('2010-09-25 16:23',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-26 10:37',"%Y-%m-%d %H:%M"), 'text': u'Tältplats, Vidinge'},
	"etapps1": {'startTime': time.strptime('2010-09-26 10:37',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-26 13:38',"%Y-%m-%d %H:%M"), 'text': u'Vidinge - Marö (Etapp 1, söndag)'},
	"lunchs": {'startTime': time.strptime('2010-09-26 13:38',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-26 14:48',"%Y-%m-%d %H:%M"), 'text': u'Söndag lunch (Marö)'},
	"etapps2": {'startTime': time.strptime('2010-09-26 14:48',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-26 17:19',"%Y-%m-%d %H:%M"), 'text': u'Marö - Stämmarsund (Etapp 2, söndag)'},
	"efter": {'startTime': time.strptime('2010-09-26 17:19',"%Y-%m-%d %H:%M"), 'endTime': time.strptime('2010-09-26 23:00',"%Y-%m-%d %H:%M"), 'text': u'Urpackning och hemfärd'}
}


folder = u"."
allFiles = os.listdir(folder)

allImages = {}
for i in allFiles:
	if (os.path.isfile("./" + i) and i.split(".")[-1].lower() == 'jpg'):
		print '...examining file: ' + i
		thisFile = open("./" + i,"rb")
		headers = EXIF.process_file(thisFile, 'UNDEF', False, False, False)
		thisStamp = time.strptime(headers['EXIF DateTimeOriginal'].__str__(),"%Y:%m:%d %H:%M:%S")
		coords = GetGps(headers)
		thisImage = {}
		thisImage['id'] = ''.join(i.lower().split('.jpg')[0].split(' ')).encode('ascii','ignore')
		thisImage['lat'] = coords[0]
		thisImage['long'] = coords[1]
		thisImage['file'] = i
		thisImage['by'] = i.split('_')[0]
		thisImage['origfile'] = '_'.join(i.split('_')[1:])
		imgSize = Image.open(i).size
		thisImage['xSize'] = imgSize[0]
		thisImage['ySize'] = imgSize[1]
		for j in ep:
			if thisStamp > ep[j]['startTime'] and thisStamp < ep[j]['endTime']: thisImage['ep'] = j
		allImages[thisStamp] = thisImage

thisStamp = time.strptime('2010:09:26 15:12:34','%Y:%m:%d %H:%M:%S')
thisImage = {}
thisImage['id'] = u'håkan_DSCN4232'.encode('ascii','ignore')
thisImage['lat'] = 59.69118575
thisImage['long'] = 19.0335529
thisImage['file'] = u'håkan_DSCN4232.MOV'
thisImage['by'] = u'Håkan'
thisImage['origfile'] = 'DSCN4232.MOV'
thisImage['xSize'] = 0
thisImage['ySize'] = 0
thisImage['ep'] = 'etapps2'
allImages[thisStamp] = thisImage

thisStamp = time.strptime('2010:09:26 15:12:58','%Y:%m:%d %H:%M:%S')
thisImage = {}
thisImage['id'] = u'håkan_DSCN4233'.encode('ascii','ignore')
thisImage['lat'] = 59.69118575
thisImage['long'] = 19.0335529
thisImage['file'] = u'håkan_DSCN4233.MOV'
thisImage['by'] = u'Håkan'
thisImage['origfile'] = 'DSCN4233.MOV'
thisImage['xSize'] = 0
thisImage['ySize'] = 0
thisImage['ep'] = 'etapps2'
allImages[thisStamp] = thisImage

thisStamp = time.strptime('2010:09:26 14:50:58','%Y:%m:%d %H:%M:%S')
thisImage = {}
thisImage['id'] = u'dan_IMGP0117'.encode('ascii','ignore')
thisImage['lat'] = 59.700245
thisImage['long'] = 19.061261
thisImage['file'] = u'dan_IMGP0117.AVI'
thisImage['by'] = u'Dan'
thisImage['origfile'] = 'dan_IMGP0117.AVI'
thisImage['xSize'] = 0
thisImage['ySize'] = 0
thisImage['ep'] = 'etapps2'
allImages[thisStamp] = thisImage

thisStamp = time.strptime('2010:09:25 17:25:00','%Y:%m:%d %H:%M:%S')
thisImage = {}
thisImage['id'] = u'photosynth1'
thisImage['lat'] = 59.659636
thisImage['long'] = 19.1764769999
thisImage['file'] = u'photosynth1'
thisImage['by'] = 'Hugo'
thisImage['origfile'] = 'http://photosynth.net/view.aspx?cid=266fcc25-3d6d-4f81-bbee-fab0b18b5c20'
thisImage['xSize'] = 0
thisImage['ySize'] = 0
thisImage['ep'] = 'talt'
allImages[thisStamp] = thisImage

allKeys = allImages.keys()
allKeys.sort()

for i in range(0, len(allKeys)):
	thisImage = allImages[allKeys[i]]
	outFile.write(u'<Placemark id="' + thisImage['id'] + u'">\n')
	outFile.write('<name>' + time.strftime('%H:%M',allKeys[i]) + '</name>\n')
	outFile.write('<snippet>' + thisImage['origfile'] + '</snippet>\n')
	outFile.write('<gx:TimeStamp id="camera-timestamp"><when>' + time.strftime('%Y-%m-%dT%H:%M:%S+02:00',allKeys[i]) + '</when></gx:TimeStamp>\n')
	outFile.write('<description><![CDATA[\n')
	outFile.write('<style type="text/css">a:link,a:visited {color:navy;text-decoration:none;} a:hover {color:blue; text-decoration:underline;} a img {border: 2px solid #aaa} a:hover img {border: 2px solid blue;} .klick {text-align: center; font-weight: bold; margin: 2em 0 2em 0; display: block; font-size: 20px;}</style>\n')
	outFile.write('<h1>' + thisImage['origfile'] + '</h1>\n')
	if thisImage['xSize'] == 0 and thisImage['ySize'] == 0:
		if thisImage['file'].split('.')[-1].lower() in ['mov','avi']:
			outFile.write(u'<a href="http://oxel.net/abpaddling/' + thisImage['file'] + u'" class="klick">Klicka här</a><br/>\n')
		else:
			outFile.write(u'<a href="' + thisImage['origfile'] + u'" class="klick">Klicka här</a><br/>\n')
	else:
		if thisImage['xSize'] > thisImage['ySize']:
			xSize = 500
			ySize = 500 * thisImage['ySize'] / thisImage['xSize']
		else:
			ySize = 500
			xSize = 500 * thisImage['xSize'] / thisImage['ySize']
		outFile.write('<center><a href="http://oxel.net/abpaddling/' + thisImage['file'] +'"><img src="http://oxel.net/abpaddling/thumbs/web_' + thisImage['file'].lower() + '" alt="' + thisImage['origfile'] + ', foto av ' + thisImage['by'] + '" width="' + str(xSize) + '" height="' + str(ySize) + '"/></a></center><br/>\n')
	outFile.write('<div style="float:right;"><em>Foto av ' + thisImage['by'][0].upper() + thisImage['by'][1:] + '</em></div>\n')
	outFile.write('<h2><a href="#' + thisImage['ep'] + ';balloonFlyto">' + ep[thisImage['ep']]['text'] + '<br/>' + time.strftime('%Y-%m-%d %H:%M',allKeys[i]) + '</a></h2>\n')
	
	prevFile = {False: allImages[allKeys[len(allKeys)-1]]['id'], True: allImages[allKeys[i-1]]['id']}[i>0]
	outFile.write(u'<div style="float:left;"><a href="#' + prevFile.encode('utf-8') + u';balloonFlyto">Föregående</a></div>&nbsp;')
	if i==len(allKeys)-1:
		nextFile = allImages[allKeys[0]]['id']
	else:
		nextFile = allImages[allKeys[i+1]]['id']
	outFile.write(u'<div style="float:right;"><a href="#' + nextFile.encode('utf-8') + u';balloonFlyto">Nästa</a></div><br />')

	outFile.write(']]></description>\n')
	outFile.write('<styleUrl>#photo' + thisImage['by'].lower().encode('ascii','ignore') + '</styleUrl>\n')
	outFile.write('<Point><coordinates>' + str(thisImage['long']) + ',' + str(thisImage['lat']) + ',0</coordinates></Point>\n')
	outFile.write('</Placemark>\n\n')
	print thisImage['file'] + ' - ' + thisImage['ep']

if 1 == 2:
	currEp = ''
	for i in range(0, len(allKeys)):
		thisImage = allImages[allKeys[i]]
		if thisImage['ep'] <> currEp:
			if currEp <> '': outFile.write(']]></description>\n\n\n')
			outFile.write('\n\n<description><![CDATA[\n')
			outFile.write('<name>' + ep[thisImage['ep']]['text'] + '</name>\n')
			outFile.write('<style type="text/css">.thumb {float:left;width:90px;height:90px;font-size: 10px; text-align:center;vertical-align:bottom;text-decoration:italic;} a:link,a:visited {color:navy;text-decoration:none;} a:hover {color:blue; text-decoration:underline;} a img {border: 2px solid #aaa} a:hover img {border: 2px solid blue;}</style>\n')
			currEp = allImages[allKeys[i]]['ep']
		
		outFile.write('<div class="thumb">')
		outFile.write('<a href="#' + thisImage['id'] + ';balloonFlyto">\n')
		outFile.write('<img src="../thumbs/web_' + thisImage['file'].lower() + '" alt="' + thisImage['origfile'] + ', foto av ' + thisImage['by'] + '" width="65" height="65"/><br/>\n')
		outFile.write(time.strftime('%H:%M',allKeys[i]) + '\n')
		outFile.write('</a></div>\n')
	outFile.write(']]></description>\n\n\n')

outFile.close()
