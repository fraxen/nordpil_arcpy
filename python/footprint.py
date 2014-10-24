# -*- coding: UTF-8 -*-
#---------------------------------------------------------------------------
# This Python script will traverse through a workspace/folder of shapefiles
# and inspect them in regards to attributes/fields. The list of fields will
# are written to a spreadsheet with names and properties.
#
# This script has not been tested with other kinds of workspaces, e.g.
# Geodatabases etc...
#---------------------------------------------------------------------------
#   Name:          footprint
#   Version:       1.0
#   Authored by:   Hugo Ahlenius, Nordpil - http://nordpil.com
#   
#   License:       Creative Commons Attribution 3.0 Unported License
#---------------------------------------------------------------------------

#Import modules
import arcpy,sys,os,datetime
arcpy.env.overwriteOutput = True

# {{{ HANDLE PARAMETERS
paramInRaster = arcpy.GetParameterAsText(0)
paramOutShape = arcpy.GetParameterAsText(1)
paramWorkspace = arcpy.GetParameterAsText(2)

if len(paramWorkspace) == 0:
	paramWorkspace = arcpy.env.workspace

if arcpy.env.workspace is None or not os.path.isdir(paramWorkspace) or not arcpy.Exists(paramInRaster):
	arcpy.AddError("Input parameters are incorrect\rfootprint.py (name of raster dataset) {optional name of output shapefile} {optional workspace path}\nIf workspace is not set in the environment, the workspace needs to be provided as an argument")
	raise StandardError

paramOutFile = paramOutShape
if len(paramOutShape) == 0:
	# If no paramOutShape given, it suggests a new name...
	paramOutFile = paramInRaster + '_footprint.shp'
	if len(paramInRaster.split('/')[0].split('\\')[-1].split('.')) > 1:
		paramOutFile = paramInRaster.split('.')[:-1][0] + '_footprint.shp'
if not paramOutFile.split('.')[-1] == 'shp':
	paramOutFile = paramOutFile + '.shp'
# }}}

# Get properties for the specified raster dataset
propsInRaster = arcpy.Describe(paramInRaster)

# {{{ Create a polygon for the featureList array
point = arcpy.Point()
array = arcpy.Array()
featureList = []

point.X = propsInRaster.extent.XMin
point.Y = propsInRaster.extent.YMin
array.add(point)

point.X = propsInRaster.extent.XMin
point.Y = propsInRaster.extent.YMax
array.add(point)

point.X = propsInRaster.extent.XMax
point.Y = propsInRaster.extent.YMax
array.add(point)

point.X = propsInRaster.extent.XMax
point.Y = propsInRaster.extent.YMin
array.add(point)
array.add(array.getObject(0))
polygon = arcpy.Polygon(array)
featureList.append(polygon)
# }}}

arcpy.CopyFeatures_management(featureList,paramOutFile)
arcpy.DefineProjection_management(paramOutFile,propsInRaster.spatialReference)

# Here I am trying to add it to current ArcMap pane, if run from the ArcMap python console/pane, but it doesn't seem to work... I guess it returns false here...
isArcMap = True
try:
	thisMxd = arcpy.mapping.MapDocument("CURRENT")
except:
	isArcMap = False

if isArcMap:
	arcpy.MakeFeatureLayer_management (paramOutFile,paramOutFile.split('/')[0].split('\\')[-1].split('.')[:-1][0])
