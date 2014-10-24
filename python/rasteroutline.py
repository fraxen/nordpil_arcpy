# -*- coding: UTF-8 -*-
import sys
import os
import arcpy
import re
from arcpy import env
from arcpy.sa import *
env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

try:
	if len(sys.argv) < 2: raise
	inRaster = sys.argv[1]
	if len(sys.argv) == 2:
		if (re.search(r'\d+$',inRaster)):
			outPoly = re.sub(r'(.*?)\d+$',r'\1',inRaster) + str(int(re.sub(r'.*?(\d+$)',r'\1',inRaster)) +1)
	else:
		outPoly = sys.argv[2]
except:
	print "\n\nError:", str(sys.exc_info())
	print "\n\nPlease verify the input arguments\n" + sys.argv[0] + " <inRaster> [outPoly shape]>\n\n"
	sys.exit()

print 'Creating footprint/outline from: ' + inRaster

temp1 = CreateConstantRaster(1,"INTEGER", Raster(inRaster).meanCellHeight, Raster(inRaster).extent)
arcpy.RasterToPolygon_conversion(temp1,outPoly)
