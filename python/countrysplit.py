# -*- coding: UTF-8 -*-
#---------------------------------------------------------------------------
# This Python script will split a feature class and export individual
# shape files based on an attribute field
#
# This script has not been tested with other kinds of workspaces, e.g.
# Geodatabases etc...
#
# To execute this script...
#  - python.exe countrysplit.py "shapefile" "field" "prefix" "workspace" "export to svg true/false"
#  - or execute toolbox
#  - or import the script as a module, and then countrysplit.countrysplit("shapefile","field","prefix","workspace","export to svg true/false")
# Only the two first parameters are required
#
#---------------------------------------------------------------------------
#   Name:          countrysplit
#   Version:       1.0
#   Authored by:   Hugo Ahlenius, Nordpil - http://nordpil.com
#   
#   License:       Creative Commons Attribution 3.0 Unported License
#---------------------------------------------------------------------------
#
# TODO: Trips up on geoprocessing options - look at the overwrite settings + adding results by default

#Import modules
import arcpy,sys,os,re

def getUniqueValues(shapeFile,field):
	# Returns a list of unique values in the specified feature class and for the specified field
	arcpy.SetProgressor("default", "Searching for unique values")
	allVals = []
	rows = arcpy.SearchCursor(shapeFile)
	for row in rows:
		allVals.append(row.getValue(field))
	uniqueList = sorted(list(set(allVals)))
	return uniqueList


def performExport(uniques, shapeFile, exportPrefix, field, doSvg):
	# Iterates over unique values and exports to a new featureclass
	# For SVG we need a slightly different approach, since we are actually exporting a map view
	try:
		# FOR SVG, we need to check that there is a map view, in ArcMap, if not the script fails
		if doSvg:
			curMap = arcpy.mapping.MapDocument("CURRENT")
			allLayers = arcpy.mapping.ListLayers(curMap)
			for lyr in allLayers:
				lyr.visible = False
	except:
		arcpy.AddError("For SVG export, this needs to be run from inside ArcMap")

	arcpy.SetProgressor("step", "Exporting %s features" % len(uniques), 0, len(uniques), 1)
	for i,val in enumerate(uniques):
		# Loops over all the unique values and exports the data one by one
		val = str(val)
		arcpy.SetProgressorLabel("Exporting features " + val)
		arcpy.SetProgressorPosition(i)
		arcpy.MakeFeatureLayer_management(shapeFile, 'lyrSel', ' "%s" = \'%s\' ' % (field,val))
		outFile = re.sub("\W","_",'%s%s' % (exportPrefix,val))
		if doSvg:
			if not 'lyrSel' in [j.name for j in arcpy.mapping.ListLayers(curMap)]:
				try:
					arcpy.mapping.AddLayer(arcpy.mapping.ListDataFrames(curMap)[0],'lyrSel')
				except:
					arcpy.AddError("For SVG export, this needs to be run from inside ArcMap")
			arcpy.mapping.ExportToSVG(curMap,arcpy.env.workspace + os.sep + outFile
						+ '.svg',arcpy.mapping.ListDataFrames(curMap)[0],900000,900000,25000)
			thisLayer = arcpy.mapping.ListLayers(curMap)[
						[j.name for j in arcpy.mapping.ListLayers(curMap)].index('lyrSel')]
			arcpy.mapping.RemoveLayer(arcpy.mapping.ListDataFrames(curMap)[0],thisLayer)
		else:
			arcpy.CopyFeatures_management('lyrSel',outFile)

def countrysplit(paramInShape, paramField, paramOutShapePrefix='', paramWorkspace='', doSvg=False):
	# {{{ MAIN METHOD
	try:
		# {{{ HANDLE PARAMETERS
		if len(paramWorkspace) == 0:
			paramWorkspace = arcpy.env.workspace
		if not arcpy.Exists(paramInShape):
			arcpy.AddError('Input parameters are incorrect\rcountrysplit.py '
						+'(Shapefile) (fieldname) {optional prefix for output files}'
						+'{optional workspace path} {set to True to do Svg}\n'
						+'If workspace is not set in the environment,'
						+'the workspace needs to be provided as an argument')

		if paramWorkspace is None or not os.path.isdir(paramWorkspace):
			paramWorkspace = arcpy.Describe(paramInShape).path
		arcpy.env.workspace = paramWorkspace
		if doSvg == 'true': doSvg = True
		if doSvg != True: doSvg = False
		# }}}

		# Get unique Values
		uniqVals = getUniqueValues(paramInShape,paramField)
		performExport(uniqVals, paramInShape, paramOutShapePrefix, paramField, doSvg)
	except arcpy.ExecuteError:
		print arcpy.GetMessages(2)
		arcpy.AddError(arcpy.GetMessages(2))
	except Exception as e:
		print e.args[0]
		arcpy.AddError(e.args[0])
	# }}}



# {{{ HANDLE PARAMETERS
if __name__ == '__main__':
	argv = tuple(arcpy.GetParameterAsText(i)
				for i in range(arcpy.GetArgumentCount()))
	print argv
	print arcpy.GetParameterAsText(0)
	print "\n\n\n\n"
	countrysplit(*argv)
# }}}
