#---------------------------------------------------------------------------
# This Python script will traverse through a workspace/folder of shapefiles
# and inspect them in regards to attributes/fields. The list of fields will
# are written to a spreadsheet with names and properties.
#
# This script has not been tested with other kinds of workspaces, e.g.
# Geodatabases etc...
#---------------------------------------------------------------------------
#   Name:       FcFieldInfo
#   Version:    1.0
#   Authored    By: Hugo Ahlenius, Nordpil - http://nordpil.com
#   Copyright:  Creative Commons.
#---------------------------------------------------------------------------

#Import modules
import arcpy,sys,os,datetime

# {{{ HANDLE PARAMETERS
paramWorkspace = arcpy.GetParameterAsText(0)
paramOutFile = arcpy.GetParameterAsText(1)
paramWildcard = arcpy.GetParameterAsText(2)

if len(paramWorkspace) == 0:
	paramWorkspace = arcpy.env.workspace
if not os.path.isdir(paramWorkspace):
	arcpy.AddError("Input parameters are incorrect\rfieldinfo.py {optional workspace path} {optional output xls/htm file} {optional wildcard}")
	raise StandardError

arcpy.env.workspace = paramWorkspace

if len(paramOutFile) == 0:
	paramOutFile = arcpy.env.workspace + '/fieldinfo_%s.xls' % datetime.datetime.now().strftime("%Y%m%d-%H%M")

if paramOutFile.find('xls') <1 and paramOutFile.find('htm') <1:
	paramOutFile = paramOutFile + '.xls'
# }}}

# {{{ INSPECT THE WORKSPACE
dataList = arcpy.ListFeatureClasses()
dataList.sort()

if len(dataList) == 0:
	arcpy.AddWarning('No featureclasses found')
	sys.exit()

arcpy.SetProgressor('step','Analyzing %s featureclasses...' % len(dataList), 0, len(dataList))

arcpy.AddMessage ('Examining %s featureclasses in workspace %s\nResults will be written to %s' % (len(dataList),paramWorkspace,paramOutFile))
# }}}

# {{{ SPREADSHEET HEADERS
# We are doing this as an html file, for simplicity - it opens well in OpenOffice.org, LibreOffice as well as Microsoft Excel or Microsoft Access
fieldSheet = open(paramOutFile,'wb')
fieldSheet.write('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html PUBLIC "-//Extender//DTD XHTML-Extended 1.1//EN" "http://maps.grida.no/include2/xhtml11s_extend.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" ><head>\n')
fieldSheet.write('<style type="text/css">html,body: font-family{Helvetica,Arial,Sans-Serif} td,tr,table,th,thead{Border: 1px solid #999} thead,th{font-weight:bold;background:#060075;color:white;}</style>')
fieldSheet.write('<title>%s</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta http-equiv="content-language" content="us-en" /><meta name="content-language" content="us-en" />\n' % paramOutFile)
fieldSheet.write('</head><body><table>\n<thead><tr>')
for field in ('File', 'Field', 'Alias', 'Domain', 'Type', 'Length', 'Precision', 'Scale', 'Editable', 'hasIndex', 'isNullable', 'isUnique'):
	fieldSheet.write('<th>%s</th>' % field)
fieldSheet.write('</tr></thead><tbody>\n')
# }}}

# {{{ Main loop - loop over all fc's in the workspace, and then over all their fields...
iteration = 0
for dataset in dataList:
	iteration = iteration + 1
	arcpy.SetProgressorLabel('Examining %s' % dataset)
	arcpy.SetProgressorPosition(iteration)
	allFields = arcpy.ListFields(dataset)
	for field in allFields:
		fieldSheet.write('<tr><td>%s</td>' % dataset)
		for property in ('name', 'aliasName', 'domain', 'type', 'length', 'precision', 'scale', 'editable', 'hasIndex', 'isNullable', 'isUnique'):
			try:
				fieldSheet.write('<td>%s</td>' % eval('field.%s' % property))
			except:
				fieldSheet.write('<td></td>')
		fieldSheet.write('</tr>\n')
# }}}

# Closing tags at end of file, and then close() the file...
fieldSheet.write('</tbody></table></body></html>')
fieldSheet.close()
