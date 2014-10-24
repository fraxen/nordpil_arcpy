"""
Tool Name:  Create Filled Contours
Source Name: CreateFilledContours.py
Version: ArcGIS 10.0
Author: ESRI

This utility creates filled polygons from an input raster.

Limitations:
    - Cannot output to shapefile because of string length>254 required
      in SpatialJoin
    - If more than 3 contour lines cross a single cell you might want to
      Resample using half the original cellsize
"""
import os
import sys
import arcpy
from arcpy.sa import *

def int_if_youCan(x):
    """ Return string without decimals if value has none"""
    if x % 1.0 == 0:
        strX = str(int(x))
    else:
        strX = "%.6f" % (x)
    return strX

def FindZ(outContoursPolygons, in_raster):
    """ Use the point within the polygon to determine the low and high
        sides of the polygon"""
    outEVT = 'outEVT'
    outEVTjoinedLayer = 'outEVTjoinedLayer'
    outPolygPoints = 'outPolygPoints'
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

def PerformSpatialJoin(target_fc, join_fc, out_fc, contour_interval):
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
        CreateOutputContourFields(out_fc, contour_interval)

    except Exception as ex:
        arcpy.AddMessage(ex.args[0])

def CreateOutputContourFields(inFC, contour_interval):
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
                    maxValue = minValue + contour_interval
                else:
                    minValue = maxValue - contour_interval

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

def main():
	# Input parameters
	if arcpy.GetParameterAsText(0):
		arguments = tuple(arcpy.GetParameterAsText(i)
			for i in range(arcpy.GetArgumentCount()))
	else:
		arguments = sys.argv[1:]
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
		contour_interval = arguments[2]
	except IndexError:
		arcpy.AddMessage("Contour interval:")
		contour_interval = raw_input()
	try:
		base_contour = arguments[3]
	except IndexError:
		arcpy.AddMessage("Base contour (optional) not specified, using default value of 0")
		base_contour = 0
	try:
		z_factor = arguments[4]
	except IndexError:
		arcpy.AddMessage("Z factor (optional) not specified, using default value of 1")
		z_factor = 1
	
	# Setting variable names for temporary feature classes
	outContours = 'outContours'
	outPolygonBndry = 'outPolygonBndry'
	outContoursPolygons = 'outContoursPolygons'
	outBuffer = 'outBuffer'
	outBufferContourLine = 'outBufferContourLine'
	outBufferContourLineLyr = 'outBufferContourLineLyr'
	outContoursPolygonsWithPoints = 'outContoursPolygonsWithPoints'
	# Input parameters
	if ".shp" in out_polygon_features:
		arcpy.AddError("Only file geodatabase output is supported.")
		sys.exit()

	outFCext = os.path.splitext(out_polygon_features)
	if (os.path.splitext(out_polygon_features)[1]).lower() == ".shp":
		arcpy.AddError("Only file geodatabase output is supported.")
		sys.exit()
	currentWS = arcpy.env.workspace
	if (os.path.splitext(currentWS)[1]).lower() != ".gdb":
		arcpy.AddError("Only file geodatabase workspace is supported.")
		sys.exit()

	ras_DEM = Raster(in_raster)
	ras_cellsize = ras_DEM.meanCellHeight

	arcpy.AddMessage("  Contour...")
	arcpy.sa.Contour(in_raster, outContours, contour_interval, base_contour,
					 z_factor)

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
									'-1000000', 'VB', '#')
	arcpy.SelectLayerByAttribute_management(outBufferContourLineLyr,
											'CLEAR_SELECTION')

	arcpy.AddMessage("  FeatureToPolygon_management...")
	arcpy.FeatureToPolygon_management([outBuffer, outContours],
									  outContoursPolygons, '#',
									  'NO_ATTRIBUTES', '#')
	outContoursPolygonsWithPoints, outEVT, outPolygPoints = \
									   FindZ(outContoursPolygons, in_raster)

	# Spatial Join and update contour labels
	PerformSpatialJoin(outContoursPolygonsWithPoints,
					   outBufferContourLineLyr, out_polygon_features,
					   contour_interval)

	fields = arcpy.ListFields(out_polygon_features)
	fields2delete = []
	for field in fields:
		if not field.required:
			fields2delete.append(field.name)
	arcpy.AddMessage("  DeleteField_management...")
	# these fields include all the temp fields like
	# 'Join_Count', 'TARGET_FID', 'range', and 'elevation'
	arcpy.DeleteField_management(out_polygon_features, fields2delete)

	arcpy.AddMessage('  Deleting temp files.')
	arcpy.Delete_management(outBuffer)
	arcpy.Delete_management(outContours)
	arcpy.Delete_management(outContoursPolygons)
	arcpy.Delete_management(outBufferContourLine)
	arcpy.Delete_management(outPolygonBndry)
	arcpy.Delete_management(outEVT)
	arcpy.Delete_management(outPolygPoints)

	scriptPath = sys.argv[0]
	toolSharePath = os.path.dirname(scriptPath)
	symbologyLayer = os.path.join(toolSharePath, 'CreateFilledContoursSymbology.lyr')
	params = arcpy.GetParameterInfo()
	params[1].symbology = symbologyLayer


if __name__ == "__main__":
	main()
