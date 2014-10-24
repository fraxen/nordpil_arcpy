import sys,os

# {{{ HANDLE PARAMETERS
try:
	if len(sys.argv) < 2: raise
	inFile = sys.argv[1]
	if (len(sys.argv) == 2):
		outFile = 'outgrid'
	else:
		outFile = sys.argv[2]
	if (not os.path.exists(inFile)): raise
	if (os.path.exists(outFile)): raise
except:
	print "\nPlease verify the input arguments:\n" + sys.argv[0] + " <input ascii-file> <output ascii grid>\n\n"
	sys.exit()

if (outFile[(len(outFile)-4):len(outFile)] <> ".asc"): outFile = outFile + '.asc'
print "\nParsing file:\n....." + inFile + "\nand creating ArcInfo raster ascii grid\n....." + outFile + "\n"
# }}}

# Need to revise the script to extract other depth horizons, or for other cell sizes...
gridCols = 360
gridRows = 180
inLevels = 33

inputFile = open(inFile, "r")
outputFile = open(outFile, "w")

# {{{ READING
print 'Reading all values'
thisData = inputFile.readline()
allData ={}
for row in range(1, gridRows+1):
	allData[row] = []
	for col in range(0, gridCols+1):
		allData[row].append(-9999) 
row = 181
col = 180
# }}}

# {{{ PARSING
while not (row == 1 and col == 180):
	for rowVal in range(0,10):
		col = col + 1
		if (col == 361): col = 1
		if (col == 181): row = row-1
		thisVal = float(thisData[8*rowVal:7+8*rowVal].strip())
		if (thisVal == -99.999):
			thisVal = -9999
		else:
			thisVal = int(round(thisVal * 100,0))
			#thisVal = round(thisVal,3)
		allData[row][col-1] = thisVal
		#print str(row) + ' - ' + str(col) + ' - ' + str(thisVal)
		if (thisVal == 20.307): exit()
	thisData = inputFile.readline()
print 'Parsed values'
# }}}

# {{{ WRITING
# {{{ HEADER
outputFile.write('NCOLS ' + str(gridCols) + '\n')
outputFile.write('NROWS ' + str(gridRows) + '\n')
outputFile.write('XLLCORNER -180\n')
outputFile.write('YLLCORNER -90\n')
outputFile.write('CELLSIZE ' + str(gridCols/360) + '\n')
outputFile.write('NODATA_VALUE -9999\n')
print 'Header written'
# }}}
for row in range(1,gridRows+1):
	outQueue = ''
	for col in range(1,gridCols+1):
		outQueue = outQueue + str(allData[row][col-1]) + ' '
	outputFile.write(outQueue + '\n')
print 'Values written'
# }}}
print 'Script finished'

inputFile.close()
outputFile.close()
