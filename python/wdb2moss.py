import re,sys

wdbFile = open(sys.argv[1], "r")
mossFile = open(sys.argv[2], "w")

for line in wdbFile:
	if line.find('segment') > -1:
		featId = re.sub("segment (\d+).*\n",r"\1",line)
		featRank = re.sub(".*rank (\d+).*\n",r"\1",line)
		featPointCount = re.sub(".*points (\d+)\n",r"\1",line) 
		if int(featId) > 9999:
			featId = "*****"
		featId = "     -" + featId
		featPadding = "                                        "
		featPadding = featPadding[0:len(featPadding) - len(featRank) - len(featPointCount)]
		mossFile.write(featId[len(featId)-5:len(featId)] + "          " + featRank + featPadding + featPointCount + '\n')
	else:
		mossFile.write(re.sub("\t(.*) (.*)\n",r"\2 \1 0\n",line))

wdbFile.close()
mossFile.close()
