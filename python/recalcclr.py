import sys,os

# Takes a surfer colormap and recalculates the gradient (using rgb gradients)
# TODO: Do HSV gradients instead

# {{{ HANDLE PARAMETERS
numSteps = 100
try:
	if len(sys.argv) < 2: raise
	inFile = sys.argv[1]
	outFile = inFile.split(".")[0] + "_recalc.clr"
	if (len(sys.argv) > 2): numSteps = int(sys.argv[2])
	if (not os.path.exists(inFile)): raise
except:
	print "\nPlease verify the input arguments:\n" + sys.argv[0] + " <input clr colormap> [number of steps]\n\n"
	sys.exit()
# }}}

def round_figures(x, n):
	# Returns x rounded to n significant figures.
	return round(x, int(n - math.ceil(math.log10(abs(x)))))

inputFile = open(inFile, "r")
outputFile = open(outFile, "w")

# {{{ READ inputFile into an array
thisData = inputFile.readline() # first line is just the header, ignore that
thisData = inputFile.readline()
allData={}
while (thisData <> ""):
	allData[float(thisData.split(" ")[0])] = [int(thisData.split(" ")[1].strip()),int(thisData.split(" ")[2].strip()),int(thisData.split(" ")[3].strip())]
	thisData = inputFile.readline()
valueRange = allData.keys()
valueRange.sort()
step = (valueRange[len(valueRange)-1] - valueRange[0]) / numSteps
# }}}

# Output clr header
outputFile.write ("ColorMap 1 1\n")

# {{{ Loop over values and stops...
valIndex = 0
val = valueRange[0]
while (val < valueRange[len(valueRange)-1]):
	if (val == valueRange[valIndex]):
		outColor = allData[valueRange[valIndex]]
	else:
		if (abs((val - valueRange[valIndex+1])/(valueRange[valIndex+1]+0.0000001)) < 0.01):
			val = valueRange[valIndex+1]
			outColor = allData[valueRange[valIndex+1]]
			valIndex += 1
		else:
			outColor = [0,0,0]
			for color in range(0,3):
				valRange = valueRange[valIndex+1] - valueRange[valIndex]
				stepRange = val - valueRange[valIndex]
				if (allData[valueRange[valIndex+1]][color] > allData[valueRange[valIndex]][color]):
					base = allData[valueRange[valIndex]][color]
					max = allData[valueRange[valIndex+1]][color]
					outColor[color] = base + ((max - base)/valRange) * stepRange
				else:
					base = allData[valueRange[valIndex+1]][color]
					max = allData[valueRange[valIndex]][color]
					outColor[color] = max - ((max - base)/valRange) * stepRange

	outputFile.write(str(round(val,5)) + " " + str(int(round(outColor[0],0))) + " " + str(int(round(outColor[1],0))) + " " + str(int(round(outColor[2],0))) + "\n")
	if (val < valueRange[len(valueRange)-1]):
		val = val + (valueRange[valIndex+1] - valueRange[valIndex])/(numSteps/(len(valueRange)-1))
outputFile.write(str(round(valueRange[len(valueRange)-1],5)) + " " + str(int(round(allData[valueRange[len(valueRange)-1]][0],0))) + " " + str(int(round(allData[valueRange[len(valueRange)-1]][1],0))) + " " + str(int(round(allData[valueRange[len(valueRange)-1]][2],0))) + "\n")
# }}}

outputFile.close()
inputFile.close()

print "\n\nRecalculated surfer clr file <" + inFile + "> with <" + str(numSteps) + "> number of steps, and saved as <" + outFile + ">\n"


