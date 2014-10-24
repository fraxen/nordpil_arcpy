"""
Tool Name:  Create Filled Contours
Source Name: CreateFilledContours.py
Version: ArcGIS 10.2.1
Author: ESRI, Nordpil

This utility creates filled polygons from an input raster.

Limitations:
	- Cannot output to shapefile because of string length>254 required
	  in SpatialJoin
	- If more than 3 contour lines cross a single cell you might want to
	  Resample using half the original cellsize
"""
import os
import sys
import re
import time
import arcpy
from arcpy.sa import *

def int_if_youCan(x):
	""" Return string without decimals if value has none"""
	if x % 1.0 == 0:
		strX = str(int(x))
	else:
		strX = "%.6f" % (x)
	return strX

def FindZ(outContoursPolygons, in_raster, tempWs, sessid):
	""" Use the point within the polygon to determine the low and high
		sides of the polygon"""
	outEVT = os.path.join(tempWs,'outEVT' + sessid)
	outEVTjoinedLayer = os.path.join(tempWs,'outEVTjoinedLayer')
	outPolygPoints = os.path.join(tempWs,'outPolygPoints' + sessid)
	arcpy.AddMessage("  FeatureToPoint_management...")
	try:
		arcpy.FeatureToPoint_management(outContoursPolygons,
										outPolygPoints, 'INSIDE')
	except:
		if arcpy.Describe(
			outContoursPolygons).spatialReference.name == 'Unknown':
				arcpy.AddError('This might be caused by data with '+
							   'Unknown spatial reference.' +
							   ' Define a projection and re-run')
		sys.exit()
	arcpy.AddMessage("  ExtractValuesToPoints...")
	ExtractValuesToPoints(outPolygPoints, in_raster, outEVT,
						 'NONE', 'ALL')
	arcpy.MakeFeatureLayer_management(outContoursPolygons,
									  outEVTjoinedLayer)
	arcpy.AddMessage("  MakeFeatureLayer_management...")
	descFlayer = arcpy.Describe(outEVTjoinedLayer)
	descOutEVT = arcpy.Describe(outEVT)
	arcpy.AddMessage("  AddJoin_management...")
	arcpy.AddJoin_management(outEVTjoinedLayer, descFlayer.OIDFieldName,
							 outEVT, descOutEVT.OIDFieldName, 'KEEP_ALL')
	return outEVTjoinedLayer, outEVT, outPolygPoints

def delete_trailing_zeros(strValue):
	""" Remove all the trailing zeros"""
	newStr = strValue
	if '.' in strValue:
		lStr = strValue.split('.')[0]
		rStr = strValue.split('.')[1].rstrip('0')
		newStr = lStr + '.' + rStr
		if rStr == '':
			newStr = lStr
	return newStr

def findUniqueContours(inlist):
	""" Find list of unique contours"""
	uniqueContourList = []
	for item in inlist:
		if item not in uniqueContourList:
			uniqueContourList.append(item)
	return uniqueContourList

def PerformSpatialJoin(target_fc, join_fc, out_fc, contour_list):
	""" Perform Spatial Join between contours and filled contours to
		create low and high contour label"""
	try:
		# add a temp field called range
		field = arcpy.Field()
		field.name = "range"
		field.aliasName = "range"
		field.length = 65534
		field.type = "Text"
		# this is the field from where the contour values are coming
		fm = arcpy.FieldMap()
		fm.mergeRule = "Join"
		fm.joinDelimiter = ";"
		fm.addInputField(join_fc, "Contour")
		fm.outputField = field
		# add the field map to the fieldmappings
		fms = arcpy.FieldMappings()
		fms.addFieldMap(fm)
		# add a temp field called elevation
		field = arcpy.Field()
		field.name = "elevation"
		field.aliasName = "Elevation from raster"
		field.type = "Double"
		# this is the field from where raster elevation values are in
		fm2 = arcpy.FieldMap()
		fieldnames = [f.name for f in arcpy.ListFields(target_fc)]
		# find index of elevation field (RASTERVALU) in output
		# created by ExtractValuesToPoints
		rastervalu_index = [index for index, item in
					   enumerate(fieldnames) if 'RASTERVALU' in item][0]
		fm2.addInputField(target_fc, fieldnames[rastervalu_index])
		fm2.outputField = field
		fms.addFieldMap(fm2)
		arcpy.AddMessage("  SpatialJoin_analysis...")
		arcpy.SpatialJoin_analysis(target_fc, join_fc, out_fc, '', '',
								   fms, 'SHARE_A_LINE_SEGMENT_WITH')
		arcpy.AddMessage("  AddField_management...")
		CreateOutputContourFields(out_fc, contour_list)

	except Exception as ex:
		arcpy.AddMessage(ex.args[0])

def CreateOutputContourFields(inFC, contour_list):
	""" Create and populate the contour fields in the
											   output feature class"""
	newFields = ['low_cont',  'high_cont', 'range_cont']
	newFieldAlias = ['Low contour',  'High contour', 'Contour range']
	icnt = 0
	for newField in newFields:
		arcpy.AddField_management(inFC, newField, 'TEXT', '#', '#', '#',
								  newFieldAlias[icnt], 'NULLABLE',
								  'REQUIRED', '#')
		icnt+=1
	cur = arcpy.UpdateCursor(inFC)
	icnt=0
	for row in cur:
		icnt+=1
		joinCount = row.getValue('Join_Count')
		contourString = row.getValue('range')
		pointElevation = row.getValue('elevation')
		contourList = []
		for i in contourString.split(';'):
			contourList.append(float(i))

		nuniques = findUniqueContours(contourList)

		try:
			if len(nuniques) > 2:
				contourList = [x for x in contourList if x > -999999]
			minValue = min(contourList)
			maxValue = max(contourList)
			if minValue == maxValue:
				joinCount = 1
			if minValue < -999999 or joinCount == 1:
				if pointElevation > maxValue:
					minValue = maxValue
					maxValue = contour_list[contour_list.index(minValue)+1]
				else:
					minValue = contour_list[contour_list.index(maxValue)-1]

			sminValue = int_if_youCan(minValue)
			smaxValue = int_if_youCan(maxValue)

		except:
			sminValue = int_if_youCan(-1000000)
			smaxValue = int_if_youCan(-1000000)

		row.setValue(newFields[0], sminValue)
		row.setValue(newFields[1], smaxValue)
		row.setValue(newFields[2], delete_trailing_zeros(sminValue) + ' - ' + \
								   delete_trailing_zeros(smaxValue))
		if minValue < -999999:
			row.setValue(newFields[2], '<NoData>')
		cur.updateRow(row)
	del cur, row

def main(in_raster, out_polygon_features, contour_list):
	arcpy.AddMessage("\nCreating contours out of %s to %s, with contour intervals %s\n------\n\n" \
		% (in_raster, out_polygon_features, ','.join([str(int_if_youCan(x)) for x in contour_list])))
	# Setting up a file geodatabase scratch workspace
	tempWs = arcpy.env.scratchGDB
	if arcpy.Describe(arcpy.env.scratchGDB).workspaceFactoryProgID.split('.')[1] != 'FileGDBWorkspaceFactory':
		if arcpy.Describe(arcpy.env.scratchWorkspace).workspaceFactoryProgID('.')[1] == 'FileGDBWorkspaceFactory':
			tempWs = arcpy.env.scratchWorkspace
		else:
			arcpy.CreateFileGDB_management(arcpy.env.scratchWorkspace,'contourlist_scratch')
			tempWs = os.path.join(arcpy.env.scratchWorkspace,'contourlist_scratch')
	
	# We are creating a semi-unique id, based on the time, so that we don't get collisions in the scratch db
	sessid = time.strftime("%Y%m%d%H%M%S")
		
	# Setting variable names for temporary feature classes
	outContours = os.path.join(tempWs,'outContours' + sessid)
	outPolygonBndry = os.path.join(tempWs,'outPolygonBndry' + sessid)
	outContoursPolygons = os.path.join(tempWs,'outContoursPolygons' + sessid)
	outBuffer = os.path.join(tempWs,'outBuffer' + sessid)
	outBufferContourLine = os.path.join(tempWs,'outBufferContourLine' + sessid)
	outBufferContourLineLyr = 'outBufferContourLineLyr'
	outContoursPolygonsWithPoints = 'outContoursPolygonsWithPoints' + sessid
	tempOut = os.path.join(tempWs,'tempOut' + sessid)

	ras_DEM = Raster(in_raster)
	ras_cellsize = ras_DEM.meanCellHeight

	arcpy.AddMessage("  Contour...")
	arcpy.sa.ContourList(in_raster, outContours, contour_list)

	arcpy.AddMessage("  RasterToPolygon_conversion...")
	arcpy.RasterToPolygon_conversion(IsNull(ras_DEM), outPolygonBndry,
									 "NO_SIMPLIFY")
	arcpy.AddMessage("  Buffer_analysis...")
	try:
		arcpy.Buffer_analysis(outPolygonBndry, outBuffer, str(-ras_cellsize)
							  + ' Unknown', 'FULL', 'ROUND', 'NONE', '#')
	except:
		arcpy.AddError('This might be caused by insufficient memory.'+
						'Use a smaller extent or try another computer.')
		arcpy.Delete_management(outContours)
		arcpy.Delete_management(outPolygonBndry)
		sys.exit()


	arcpy.AddMessage("  FeatureToLine_management...")
	arcpy.FeatureToLine_management([outContours, outBuffer],
									outBufferContourLine, '#', 'ATTRIBUTES')

	arcpy.MakeFeatureLayer_management(outBufferContourLine,
									  outBufferContourLineLyr)
	arcpy.SelectLayerByAttribute_management(outBufferContourLineLyr,
											'NEW_SELECTION',
											'"BUFF_DIST" <> 0')
	arcpy.CalculateField_management(outBufferContourLineLyr, 'Contour',
									'-1000000', 'PYTHON', '#')
	arcpy.SelectLayerByAttribute_management(outBufferContourLineLyr,
											'CLEAR_SELECTION')

	arcpy.AddMessage("  FeatureToPolygon_management...")
	arcpy.FeatureToPolygon_management([outBuffer, outContours],
									  outContoursPolygons, '#',
									  'NO_ATTRIBUTES', '#')
	outContoursPolygonsWithPoints, outEVT, outPolygPoints = \
									   FindZ(outContoursPolygons, in_raster, tempWs, sessid)


	# Spatial Join and update contour labels
	PerformSpatialJoin(outContoursPolygonsWithPoints,
					   outBufferContourLineLyr, tempOut,
					   contour_list)

	fields = arcpy.ListFields(tempOut)
	fields2delete = []
	for field in fields:
		if not field.required:
			fields2delete.append(field.name)
	arcpy.AddMessage("  DeleteField_management...")
	# these fields include all the temp fields like
	# 'Join_Count', 'TARGET_FID', 'range', and 'elevation'
	arcpy.DeleteField_management(tempOut, fields2delete)

	# Copy the result to the final location
	arcpy.CopyFeatures_management(tempOut, out_polygon_features)

	arcpy.AddMessage('  Deleting temp files.')
	arcpy.Delete_management(tempOut)
	arcpy.Delete_management(outBuffer)
	arcpy.Delete_management(outContours)
	arcpy.Delete_management(outContoursPolygons)
	arcpy.Delete_management(outBufferContourLine)
	arcpy.Delete_management(outPolygonBndry)
	arcpy.Delete_management(outEVT)
	arcpy.Delete_management(outPolygPoints)
	arcpy.Delete_management(outBufferContourLineLyr)
	arcpy.Delete_management(outContoursPolygonsWithPoints)
	try:
		# If we are in ArcMap, also remove visible layers
		thisDoc = arcpy.mapping.MapDocument("CURRENT")
		for lyr in arcpy.mapping.ListLayers(thisDoc):
			if lyr.name in ['outEVT','outPolygPoints','outBufferContourLine','outContours',
				'outContoursPolygons','outBuffer','outPolygonBndry', 'tempOut']:
				arcpy.mapping.RemoveLayer(thisDoc.activeDataFrame,lyr)
	except:
		pass
	try:
		scriptPath = sys.argv[0]
		toolSharePath = os.path.dirname(scriptPath)
		symbologyLayer = os.path.join(toolSharePath, 'CreateFilledContoursSymbology.lyr')
		params = arcpy.GetParameterInfo()
		params[1].symbology = symbologyLayer
	except:
		pass

if __name__ == "__main__":
	# Input parameters
	if arcpy.GetParameterAsText(0):
		arguments = tuple(arcpy.GetParameterAsText(i)
			for i in range(arcpy.GetArgumentCount()))
	else:
		arguments = sys.argv[1:]
	try:
		try:
			in_raster = arguments[0]
		except IndexError:
			arcpy.AddMessage("Input raster:")
			in_raster = raw_input()
		try:
			out_polygon_features = arguments[1]
		except IndexError:
			arcpy.AddMessage("Output polygon features:")
			out_polygon_features = raw_input()
		try:
			contour_list = arguments[2]
		except IndexError:
			arcpy.AddMessage("Contour list(comma separated list of values):")
			contour_list = raw_input()
		if isinstance(contour_list, basestring):
			contour_list = re.split(',|;', contour_list)
		contour_list = [float(x) for x in contour_list]
		contour_list.sort()

	except Exception,e:
		print "CreateFilledContourList - creates polygons out of contours, using the ContourList tool"
		print "Usage: CreateFilledContourList.py <input raster> <output polygon features> <contour list, a comma-separated list enclosed in quotes>"
		print "Can be run from the prompt, imported as module and run as a toolbox script"
		print "To run as a module:"
		print "   import CreateFilledContourList"
		print "   CreateFilledContourList.main(<input raster>,<output polygon features>,<contour list, a python list with values>"
	main(in_raster,out_polygon_features, contour_list)

