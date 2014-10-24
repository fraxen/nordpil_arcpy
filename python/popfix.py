import pyodbc
import math

cnxn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=C:\\mnt\\project\\3004 Azote\\graphics\\cities\\ws\\city.mdb')
cursor = cnxn.cursor()

heightFactor = 100
widthFactor = 0.2
xWidth = widthFactor * 60 * 1852 # number of meters in widthFactor
outputFile = open("popfix.kml", "w")
m1 = 111132.92		# latitude calculation term 1
m2 = -559.82		# latitude calculation term 2
m3 = 1.175			# latitude calculation term 3
m4 = -0.0023		# latitude calculation term 4
p1 = 111412.84		# longitude calculation term 1
p2 = -93.5			# longitude calculation term 2
p3 = 0.118			# longitude calculation term 3

# {{{ HEADER STUFF
outputFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
outputFile.write('<kml xmlns="http://earth.google.com/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
outputFile.write('<Document>\n')
outputFile.write('<name>Cities</name>\n')
outputFile.write('<Style>\n')
outputFile.write('<ListStyle>\n')
outputFile.write('<listItemType>checkHideChildren</listItemType>\n')
outputFile.write('<ItemIcon>\n')
outputFile.write('<state>open closed error fetching0 fetching1 fetching2</state>\n')
outputFile.write('<href>http://nordpil.com/default/css/themes/nordpil/images/favicon.ico</href>\n')
outputFile.write('</ItemIcon>\n')
outputFile.write('</ListStyle>\n')
outputFile.write('</Style>\n')
outputFile.write('<open>1</open>\n')
outputFile.write('<description></description>\n')
outputFile.write('<styleUrl>#nordpil_logo</styleUrl>\n')
outputFile.write('<snippet></snippet>\n')
outputFile.write('<LookAt>\n')
outputFile.write('<gx:TimeStamp><when>2005-01-01T00:00:00Z</when></gx:TimeStamp>\n')
outputFile.write('<longitude>16.72528620935799</longitude>\n')
outputFile.write('<latitude>20.33905232696153</latitude>\n')
outputFile.write('<altitude>0</altitude>\n')
outputFile.write('<range>14028660.68715566</range>\n')
outputFile.write('<tilt>0</tilt>\n')
outputFile.write('<heading>-1.744396647795077</heading>\n')
outputFile.write('<altitudeMode>relativeToGround</altitudeMode>\n')
outputFile.write('</LookAt>\n')
# }}}

# {{{ STYLES

# {{{ BALLOON STYLE
balStyle = ""
balStyle = balStyle + '<BalloonStyle><text><![CDATA[\n'
balStyle = balStyle + '<script type="text/javascript" src="http://www.google.com/jsapi"></script>\n'
balStyle = balStyle + '<script type="text/javascript">\n'
balStyle = balStyle + 'google.load("visualization", "1", {packages:["columnchart"]});\n'
balStyle = balStyle + 'google.setOnLoadCallback(drawChart);\n'
balStyle = balStyle + 'function drawChart() {\n'
balStyle = balStyle + 'var data = new google.visualization.DataTable();\n'
balStyle = balStyle + 'data.addColumn("string", "Year");\n'
balStyle = balStyle + 'data.addColumn("number", "Population (historical)");\n'
balStyle = balStyle + 'data.addColumn("number", "Population (projected)");\n'
balStyle = balStyle + 'data.addRows(21);\n'

for i in range (1,17):
	balStyle = balStyle + 'data.setValue(' + str(i-1) + ', 0, "' + str(i * 5 + 1945) + '");\n'
	if (i*5+1945) < 2010:
		balStyle = balStyle + 'data.setValue(' + str(i-1) + ', 1, $[pop' + str(i * 5 + 1945) +']/1000);\n'
	else:
		balStyle = balStyle + 'data.setValue(' + str(i-1) + ', 2, $[pop' + str(i * 5 + 1945) +']/1000);\n'
for i in range (1,5):
	balStyle = balStyle + 'data.setValue(' + str(i + 15) + ', 0, "' + str(i * 5 + 2025) + '");\n'
	balStyle = balStyle + 'data.setValue(' + str(i + 15) + ', 2, 0);\n'
balStyle = balStyle + 'data.setValue(20, 0, "2050");\n'
balStyle = balStyle + 'data.setValue(20, 2, $[pop2050]/1000);\n'
balStyle = balStyle + 'var chart = new google.visualization.ColumnChart(document.getElementById("chart_div"));\n'
balStyle = balStyle + 'chart.draw(data, {colors: ["#60b0e0","#80FFFF"], isStacked: true, width: 450, height: 300, is3D: false, legend: "none", min: 0});\n'
balStyle = balStyle + '}\n'
balStyle = balStyle + '</script>\n'
balStyle = balStyle + '<h1>$[name]</h1>Population statistics, historical and projected, for the city of <a href="http://www.google.com/search?q=$[name]+$[country]+site:wikipedia.org"><em>$[name]</em></a> in <em>$[country]</em> (millions of inhabitants):\n'
balStyle = balStyle + '<center><div id="chart_div"></div>\n'
balStyle = balStyle + '<em>Data retrieved from <a href="http://esa.un.org/unup/index.asp?panel=2">World Urbanization Prospects: The 2007 Revisition Population Database http://esa.un.org/unup/index.asp?panel=2</a> (online database), accessed June 8 2009. The data has been collected and adapted for this format by <a href="http://nordpil.com">Nordpil</a>.</em> The data collection represents urban agglomerations with a population for of more than 750 000 inhabitants in 2007.</center>'
balStyle = balStyle + ']]></text></BalloonStyle>\n'
# }}}

# {{{ BALLOON STYLE Description
balDescStyle = ""
balDescStyle = balDescStyle + '<BalloonStyle><text><![CDATA[\n'
balDescStyle = balDescStyle + '<script type="text/javascript" src="http://www.google.com/jsapi"></script>\n'
balDescStyle = balDescStyle + '<script type="text/javascript">\n'
balDescStyle = balDescStyle + 'google.load("visualization", "1", {packages:["columnchart"]});\n'
balDescStyle = balDescStyle + 'google.setOnLoadCallback(drawChart);\n'
balDescStyle = balDescStyle + 'function drawChart() {\n'
balDescStyle = balDescStyle + 'var data = new google.visualization.DataTable();\n'
balDescStyle = balDescStyle + 'data.addColumn("string", "Year");\n'
balDescStyle = balDescStyle + 'data.addColumn("number", "Population (historical)");\n'
balDescStyle = balDescStyle + 'data.addColumn("number", "Population (projected)");\n'
balDescStyle = balDescStyle + 'data.addRows(21);\n'
balDescStyle = balDescStyle + 'data.setValue(0, 0, "1950");\n'
balDescStyle = balDescStyle + 'data.setValue(0, 1, 338.4);\n'
balDescStyle = balDescStyle + 'data.setValue(1, 0, "1955");\n'
balDescStyle = balDescStyle + 'data.setValue(1, 1, 390.8);\n'
balDescStyle = balDescStyle + 'data.setValue(2, 0, "1960");\n'
balDescStyle = balDescStyle + 'data.setValue(2, 1, 455.5);\n'
balDescStyle = balDescStyle + 'data.setValue(3, 0, "1965");\n'
balDescStyle = balDescStyle + 'data.setValue(3, 1, 528.7);\n'
balDescStyle = balDescStyle + 'data.setValue(4, 0, "1970");\n'
balDescStyle = balDescStyle + 'data.setValue(4, 1, 612.2);\n'
balDescStyle = balDescStyle + 'data.setValue(5, 0, "1975");\n'
balDescStyle = balDescStyle + 'data.setValue(5, 1, 696.0);\n'
balDescStyle = balDescStyle + 'data.setValue(6, 0, "1980");\n'
balDescStyle = balDescStyle + 'data.setValue(6, 1, 789.0);\n'
balDescStyle = balDescStyle + 'data.setValue(7, 0, "1985");\n'
balDescStyle = balDescStyle + 'data.setValue(7, 1, 881.9);\n'
balDescStyle = balDescStyle + 'data.setValue(8, 0, "1990");\n'
balDescStyle = balDescStyle + 'data.setValue(8, 1, 990.9);\n'
balDescStyle = balDescStyle + 'data.setValue(9, 0, "1995");\n'
balDescStyle = balDescStyle + 'data.setValue(9, 1, 1100.8);\n'
balDescStyle = balDescStyle + 'data.setValue(10, 0, "2000");\n'
balDescStyle = balDescStyle + 'data.setValue(10, 1, 1228.0);\n'
balDescStyle = balDescStyle + 'data.setValue(11, 0, "2005");\n'
balDescStyle = balDescStyle + 'data.setValue(11, 1, 1349.5);\n'
balDescStyle = balDescStyle + 'data.setValue(12, 0, "2010");\n'
balDescStyle = balDescStyle + 'data.setValue(12, 2, 1398.2);\n'
balDescStyle = balDescStyle + 'data.setValue(13, 0, "2015");\n'
balDescStyle = balDescStyle + 'data.setValue(13, 2, 1473.4);\n'
balDescStyle = balDescStyle + 'data.setValue(14, 0, "2020");\n'
balDescStyle = balDescStyle + 'data.setValue(14, 2, 1595.1);\n'
balDescStyle = balDescStyle + 'data.setValue(15, 0, "2025");\n'
balDescStyle = balDescStyle + 'data.setValue(15, 2, 1711.5);\n'
balDescStyle = balDescStyle + 'data.setValue(16, 0, "2030");\n'
balDescStyle = balDescStyle + 'data.setValue(16, 2, 0.0);\n'
balDescStyle = balDescStyle + 'data.setValue(17, 0, "2035");\n'
balDescStyle = balDescStyle + 'data.setValue(17, 2, 0.0);\n'
balDescStyle = balDescStyle + 'data.setValue(18, 0, "2040");\n'
balDescStyle = balDescStyle + 'data.setValue(18, 2, 0.0);\n'
balDescStyle = balDescStyle + 'data.setValue(19, 0, "2045");\n'
balDescStyle = balDescStyle + 'data.setValue(19, 2, 0.0);\n'
balDescStyle = balDescStyle + 'data.setValue(20, 0, "2050");\n'
balDescStyle = balDescStyle + 'data.setValue(20, 2, 1822.3);\n'
balDescStyle = balDescStyle + 'var chart = new google.visualization.ColumnChart(document.getElementById("chart_div"));\n'
balDescStyle = balDescStyle + 'chart.draw(data, {colors: ["#60b0e0","#80FFFF"], isStacked: true, width: 450, height: 300, is3D: false, legend: "none", min: 0});\n'
balDescStyle = balDescStyle + '}\n'
balDescStyle = balDescStyle + '</script>\n'
balDescStyle = balDescStyle + '<img src="http://nordpil.com/static/images/logos/nordpil_tile_128px.png" width="128" height="128" alt="Nordpil - custom cartography, map design, GIS and interactive maps" title="Nordpil - custom cartography, map design, GIS and interactive maps" align="right"/><h1>Large Cities and Mega-Cities</h1><p>This dataset, extracted from UN population Division data, represents urban agglomerations of more than 750000 inhabitants in 2007. The data covers observations and modelled historical data 1950-2005, as well as projections for urban development up to 2050.</p><p>The data preparation and this presentation was prepared by Nordpil in 2007. For more information, please refer to <a href="http://nordpil.com/cities">http://nordpil.com/cities</a>.</p><p><a href="http://nordpil.com/">Nordpil offers consultancy services in map design, map production, GIS and interactive cartography.</a></p><p> The chart below displays the total amount of inhabitants in the cities covered by this data collection, in millions of inhabitants.</p>\n'
balDescStyle = balDescStyle + '<center><div id="chart_div"></div>\n'
balDescStyle = balDescStyle + '<em>Data retrieved from <a href="http://esa.un.org/unup/index.asp?panel=2">World Urbanization Prospects: The 2007 Revisition Population Database http://esa.un.org/unup/index.asp?panel=2</a> (online database), accessed June 8 2009. The data has been collected and adapted for this format by <a href="http://nordpil.com">Nordpil</a>.</em> The data collection represents urban agglomerations with a population for of more than 750 000 inhabitants in 2007.</center>'
balDescStyle = balDescStyle + ']]></text></BalloonStyle>\n'
# }}}

# {{{ LOGO STYLE
outputFile.write('<StyleMap id="nordpil_logo">\n')
outputFile.write('<Pair>\n')
outputFile.write('<key>normal</key>\n')
outputFile.write('<styleUrl>#sn_nordpil_logo</styleUrl>\n')
outputFile.write('</Pair>\n')
outputFile.write('<Pair>\n')
outputFile.write('<key>highlight</key>\n')
outputFile.write('<styleUrl>#sh_nordpil_logo</styleUrl>\n')
outputFile.write('</Pair>\n')
outputFile.write('</StyleMap>\n')
outputFile.write('<Style id="sn_nordpil_logo">\n')
outputFile.write('<IconStyle>\n')
outputFile.write('<scale>3</scale>\n')
outputFile.write('<Icon>\n')
outputFile.write('<href>icon.png</href>\n')
outputFile.write('</Icon>\n')
outputFile.write('</IconStyle>\n')
outputFile.write('<LabelStyle><scale>1.5</scale></LabelStyle>\n')
outputFile.write(balDescStyle)
outputFile.write('</Style>\n')
outputFile.write('<Style id="sh_nordpil_logo">\n')
outputFile.write('<IconStyle>\n')
outputFile.write('<scale>5</scale>\n')
outputFile.write('<Icon>\n')
outputFile.write('<href>icon.png</href>\n')
outputFile.write('</Icon>\n')
outputFile.write('</IconStyle>\n')
outputFile.write('<LabelStyle><scale>2</scale></LabelStyle>\n')
outputFile.write(balDescStyle)
outputFile.write('</Style>\n')
# }}}

outputFile.write('<Style id="hData_n">\n')
outputFile.write(balStyle)
outputFile.write('<LineStyle><color>FF0000FF</color></LineStyle>\n')
outputFile.write('<PolyStyle><color>FF0000FF</color><fill>1</fill><outline>1</outline></PolyStyle>\n')
outputFile.write('</Style>\n')
outputFile.write('<Style id="hData_h">\n')
outputFile.write(balStyle)
outputFile.write('<LineStyle><color>FFFFFFFF</color></LineStyle>\n')
outputFile.write('<PolyStyle><color>FF0000FF</color><fill>1</fill><outline>1</outline></PolyStyle>\n')
outputFile.write('</Style>\n')
outputFile.write('<StyleMap id="hData">\n')
outputFile.write('<Pair>\n')
outputFile.write('<key>normal</key>\n')
outputFile.write('<styleUrl>#hData_n</styleUrl>\n')
outputFile.write('</Pair>\n')
outputFile.write('<Pair>\n')
outputFile.write('<key>highlight</key>\n')
outputFile.write('<styleUrl>#hData_h</styleUrl>\n')
outputFile.write('</Pair>\n')
outputFile.write('</StyleMap>\n')

outputFile.write('<Style id="pData_n">\n')
outputFile.write(balStyle)
outputFile.write('<LineStyle><color>FF6666FF</color></LineStyle>\n')
outputFile.write('<PolyStyle><color>FF6666FF</color><fill>1</fill><outline>1</outline></PolyStyle>\n')
outputFile.write('</Style>\n')
outputFile.write('<Style id="pData_h">\n')
outputFile.write(balStyle)
outputFile.write('<LineStyle><color>FFFFFFFF</color></LineStyle>\n')
outputFile.write('<PolyStyle><color>FF6666FF</color><fill>1</fill><outline>1</outline></PolyStyle>\n')
outputFile.write('</Style>\n')
outputFile.write('<StyleMap id="pData">\n')
outputFile.write('<Pair>\n')
outputFile.write('<key>normal</key>\n')
outputFile.write('<styleUrl>#pData_n</styleUrl>\n')
outputFile.write('</Pair>\n')
outputFile.write('<Pair>\n')
outputFile.write('<key>highlight</key>\n')
outputFile.write('<styleUrl>#pData_h</styleUrl>\n')
outputFile.write('</Pair>\n')
outputFile.write('</StyleMap>\n')

outputFile.write('<Style id="cLabel">\n')
outputFile.write('<IconStyle>\n')
outputFile.write('<color>0</color>\n')
outputFile.write('</IconStyle>\n')
outputFile.write('<LabelStyle><scale>0.7</scale><color>FF0000FF</color></LabelStyle>\n')
outputFile.write('</Style>\n')
# }}}

# {{{ YEAR DATA
outputFile.write('<Folder>\n')
outputFile.write('<name>Years</name>\n')
outputFile.write('<open>1</open>\n')

# {{{ YEARS 1950-2025
for popYear in ['1950','1955','1960','1965','1970','1975','1980','1985','1990','1995','2000','2005','2010','2015','2020','2025']:
	cursor.execute("SELECT City, Country, Latitude, Longitude, pop" + popYear + " AS pop, pop1950,pop1955,pop1960,pop1965,pop1970,pop1975,pop1980,pop1985,pop1990,pop1995,pop2000,pop2005,pop2010,pop2015,pop2020,pop2025,pop2050 FROM popstat3 ORDER BY City")
	outputFile.write('<Folder>\n')
	outputFile.write('<name>' + popYear + '</name>\n')
	outputFile.write('<TimeSpan>\n')
	outputFile.write('<begin>' + str(int(popYear) - 3) + '-07-01</begin>\n')
	outputFile.write('<end>' + str(int(popYear) + 2 ) + '-06-30</end>\n')
	outputFile.write('</TimeSpan>\n')
	outputFile.write('<ScreenOverlay>\n')
	outputFile.write('<name>' + popYear + '</name><snippet></snippet>\n')
	outputFile.write('<Icon><href>' + popYear + '.png</href></Icon>\n')
	outputFile.write('<overlayXY x="1" y="0" xunits="fraction" yunits="fraction"/>\n')
	outputFile.write('<screenXY x="1" y="0.15" xunits="fraction" yunits="fraction"/>\n')
	outputFile.write('<size x="-1" y="-1" xunits="pixels" yunits="pixels" />\n')
	outputFile.write('</ScreenOverlay>\n')

	for row in cursor:
		outputFile.write('<Placemark>\n')
		outputFile.write('<name>' + row.City.encode("utf-8") + '</name>\n')
		if int(popYear) < 2006:
			outputFile.write('<styleUrl>#hData</styleUrl>\n')
		else:
			outputFile.write('<styleUrl>#pData</styleUrl>\n')

		outputFile.write('<ExtendedData>\n')
		outputFile.write('<Data name="country"><value>' + row.Country.encode("utf-8") + '</value></Data>\n')
		outputFile.write('<Data name="thisYear"><value>' + popYear + '</value></Data>\n')
		for popYearData in ['1950','1955','1960','1965','1970','1975','1980','1985','1990','1995','2000','2005','2010','2015','2020','2025','2050']:
			outputFile.write('<Data name="pop' + popYearData + '"><value>' + str(eval("row.pop" + popYearData)) + '</value></Data>\n')
		outputFile.write('</ExtendedData>\n')

		outputFile.write('<Polygon>\n')
		outputFile.write('<extrude>1</extrude>\n')
		outputFile.write('<altitudeMode>absolute</altitudeMode>\n')
		outputFile.write('<outerBoundaryIs>\n')
		outputFile.write('<LinearRing>\n')
		outputFile.write('<coordinates>\n')

		# deg 2 rads
		lat = abs(row.Latitude * (2 * math.pi)/360)
		longlen = (p1 * math.cos(lat)) + (p2 * math.cos(3 * lat)) + (p3 * math.cos(5 * lat))
		xWidth = widthFactor * (111319.458 / longlen)

		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude - widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude + xWidth,2)) + ',' + str(round(row.Latitude - widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude + xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')

		outputFile.write('</coordinates>\n')
		outputFile.write('</LinearRing>\n')
		outputFile.write('</outerBoundaryIs>\n')
		outputFile.write('</Polygon>\n')
		outputFile.write('</Placemark>\n')
	outputFile.write('</Folder>\n')
# }}}

# {{{ YEARS 2030-2045 (approximations)
for popYear in ['2030','2035','2040','2045']:
	cursor.execute("SELECT City, Country, Latitude, Longitude, pop1950,pop1955,pop1960,pop1965,pop1970,pop1975,pop1980,pop1985,pop1990,pop1995,pop2000,pop2005,pop2010,pop2015,pop2020,pop2025,pop2050 FROM popstat3 ORDER BY City")
	outputFile.write('<Folder>\n')
	outputFile.write('<name>' + popYear + '</name>\n')
	outputFile.write('<TimeSpan>\n')
	outputFile.write('<begin>' + str(int(popYear) - 3) + '-07-01</begin>\n')
	outputFile.write('<end>' + str(int(popYear) + 2 ) + '-06-30</end>\n')
	outputFile.write('</TimeSpan>\n')
	outputFile.write('<ScreenOverlay>\n')
	outputFile.write('<name>' + popYear + '</name><snippet></snippet>\n')
	outputFile.write('<Icon><href>' + popYear + '.png</href></Icon>\n')
	outputFile.write('<overlayXY x="1" y="0" xunits="fraction" yunits="fraction"/>\n')
	outputFile.write('<screenXY x="1" y="0.15" xunits="fraction" yunits="fraction"/>\n')
	outputFile.write('<size x="-1" y="-1" xunits="pixels" yunits="pixels" />\n')
	outputFile.write('</ScreenOverlay>\n')

	for row in cursor:
		outputFile.write('<Placemark>\n')
		outputFile.write('<name>' + row.City.encode("utf-8") + '</name>\n')
		outputFile.write('<styleUrl>#pData</styleUrl>\n')

		outputFile.write('<ExtendedData>\n')
		outputFile.write('<Data name="country"><value>' + row.Country.encode("utf-8") + '</value></Data>\n')
		outputFile.write('<Data name="thisYear"><value>' + popYear + '</value></Data>\n')
		for popYearData in ['1950','1955','1960','1965','1970','1975','1980','1985','1990','1995','2000','2005','2010','2015','2020','2025','2050']:
			outputFile.write('<Data name="pop' + popYearData + '"><value>' + str(eval("row.pop" + popYearData)) + '</value></Data>\n')
		outputFile.write('</ExtendedData>\n')

		outputFile.write('<Polygon>\n')
		outputFile.write('<extrude>1</extrude>\n')
		outputFile.write('<altitudeMode>absolute</altitudeMode>\n')
		outputFile.write('<outerBoundaryIs>\n')
		outputFile.write('<LinearRing>\n')
		outputFile.write('<coordinates>\n')

		# deg 2 rads
		lat = abs(row.Latitude * (2 * math.pi)/360)
		longlen = (p1 * math.cos(lat)) + (p2 * math.cos(3 * lat)) + (p3 * math.cos(5 * lat))
		xWidth = widthFactor * (111319.458 / longlen)

		# interpolate year value
		popThisYear = row.pop2025 + ((row.pop2050 - row.pop2025) / 25) * (int(popYear) - 2025)

		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(popThisYear * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude - widthFactor,2)) + ',' + str(round(popThisYear * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude + xWidth,2)) + ',' + str(round(row.Latitude - widthFactor,2)) + ',' + str(round(popThisYear * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude + xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(popThisYear * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(popThisYear * heightFactor,0)) + ' ')

		outputFile.write('</coordinates>\n')
		outputFile.write('</LinearRing>\n')
		outputFile.write('</outerBoundaryIs>\n')
		outputFile.write('</Polygon>\n')
		outputFile.write('</Placemark>\n')
	outputFile.write('</Folder>\n')
# }}}

# {{{ YEAR 2050
for popYear in ['2050']:
	cursor.execute("SELECT City, Country, Latitude, Longitude, pop" + popYear + " AS pop, pop1950,pop1955,pop1960,pop1965,pop1970,pop1975,pop1980,pop1985,pop1990,pop1995,pop2000,pop2005,pop2010,pop2015,pop2020,pop2025,pop2050 FROM popstat3 ORDER BY City")
	outputFile.write('<Folder>\n')
	outputFile.write('<name>' + popYear + '</name>\n')
	outputFile.write('<TimeSpan>\n')
	outputFile.write('<begin>' + str(int(popYear) - 3) + '-07-01</begin>\n')
	outputFile.write('<end>' + str(int(popYear) + 2 ) + '-06-30</end>\n')
	outputFile.write('</TimeSpan>\n')
	outputFile.write('<ScreenOverlay>\n')
	outputFile.write('<name>' + popYear + '</name><snippet></snippet>\n')
	outputFile.write('<Icon><href>' + popYear + '.png</href></Icon>\n')
	outputFile.write('<overlayXY x="1" y="0" xunits="fraction" yunits="fraction"/>\n')
	outputFile.write('<screenXY x="1" y="0.15" xunits="fraction" yunits="fraction"/>\n')
	outputFile.write('<size x="-1" y="-1" xunits="pixels" yunits="pixels" />\n')
	outputFile.write('</ScreenOverlay>\n')

	for row in cursor:
		outputFile.write('<Placemark>\n')
		outputFile.write('<name>' + row.City.encode("utf-8") + '</name>\n')
		outputFile.write('<styleUrl>#pData</styleUrl>\n')

		outputFile.write('<ExtendedData>\n')
		outputFile.write('<Data name="country"><value>' + row.Country.encode("utf-8") + '</value></Data>\n')
		outputFile.write('<Data name="thisYear"><value>' + popYear + '</value></Data>\n')
		for popYearData in ['1950','1955','1960','1965','1970','1975','1980','1985','1990','1995','2000','2005','2010','2015','2020','2025','2050']:
			outputFile.write('<Data name="pop' + popYearData + '"><value>' + str(eval("row.pop" + popYearData)) + '</value></Data>\n')
		outputFile.write('</ExtendedData>\n')

		outputFile.write('<Polygon>\n')
		outputFile.write('<extrude>1</extrude>\n')
		outputFile.write('<altitudeMode>absolute</altitudeMode>\n')
		outputFile.write('<outerBoundaryIs>\n')
		outputFile.write('<LinearRing>\n')
		outputFile.write('<coordinates>\n')

		# deg 2 rads
		lat = abs(row.Latitude * (2 * math.pi)/360)
		longlen = (p1 * math.cos(lat)) + (p2 * math.cos(3 * lat)) + (p3 * math.cos(5 * lat))
		xWidth = widthFactor * (111319.458 / longlen)

		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude - widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude + xWidth,2)) + ',' + str(round(row.Latitude - widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude + xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(row.pop * heightFactor,0)) + ' ')
		outputFile.write(str(round(row.Longitude - xWidth,2)) + ',' + str(round(row.Latitude + widthFactor,2)) + ',' + str(round(popThisYear * heightFactor,0)) + ' ')

		outputFile.write('</coordinates>\n')
		outputFile.write('</LinearRing>\n')
		outputFile.write('</outerBoundaryIs>\n')
		outputFile.write('</Polygon>\n')
		outputFile.write('</Placemark>\n')
	outputFile.write('</Folder>\n')
# }}}
# }}}

# {{{ LABELS
cursor.execute("SELECT * FROM popstat3 ORDER BY City")
outputFile.write('<Folder>\n')
outputFile.write('<name>City labels</name>\n')
outputFile.write('<TimeSpan>\n')
outputFile.write('<begin>1950-01-01</begin>\n')
outputFile.write('<end>2050-12-31</end>\n')
outputFile.write('</TimeSpan>\n')
for row in cursor:
	outputFile.write('<Placemark>\n')
	outputFile.write('<name>' + row.City.encode("utf-8") + '</name>\n')
	outputFile.write('<styleUrl>#cLabel</styleUrl>\n')
	outputFile.write('<Point>\n')
	outputFile.write('<coordinates>\n')
	outputFile.write(str(round(row.Longitude,2)) + ',' + str(round(row.Latitude,2)) + ',0 ')
	outputFile.write('</coordinates>\n')
	outputFile.write('</Point>\n')
	outputFile.write('</Placemark>\n')
outputFile.write('</Folder>\n')
# }}}

outputFile.write('</Folder>\n')
# {{{ OTHER STUFF
outputFile.write('<ScreenOverlay>\n')
outputFile.write('<name>Title and information</name><snippet></snippet>\n')
outputFile.write('<Icon><href>title.png</href></Icon>\n')
outputFile.write('<overlayXY x="0" y="1" xunits="fraction" yunits="fraction"/>\n')
outputFile.write('<screenXY x="0" y="0.90" xunits="fraction" yunits="fraction"/>\n')
outputFile.write('<size x="-1" y="-1" xunits="pixels" yunits="pixels" />\n')
outputFile.write('</ScreenOverlay>\n')
outputFile.write('<Placemark>\n')
outputFile.write('<name>About the cities data</name>\n')
outputFile.write('<snippet></snippet>\n')
outputFile.write('<visibility>1</visibility>\n')
outputFile.write('<styleUrl>#nordpil_logo</styleUrl>\n')
outputFile.write('<MultiGeometry>\n')
outputFile.write('<Point>\n')
outputFile.write('<coordinates>-2,70,0</coordinates>\n')
outputFile.write('</Point>\n')
outputFile.write('<Point>\n')
outputFile.write('<coordinates>-20,-15,0</coordinates>\n')
outputFile.write('</Point>\n')
outputFile.write('<Point>\n')
outputFile.write('<coordinates>70,-10,0</coordinates>\n')
outputFile.write('</Point>\n')
outputFile.write('<Point>\n')
outputFile.write('<coordinates>140,15,0</coordinates>\n')
outputFile.write('</Point>\n')
outputFile.write('<Point>\n')
outputFile.write('<coordinates>-100,0,0</coordinates>\n')
outputFile.write('</Point>\n')
outputFile.write('</MultiGeometry>\n')
outputFile.write('</Placemark>\n')
# }}}
outputFile.write('</Document>\n')
outputFile.write('</kml>\n')
outputFile.close()

