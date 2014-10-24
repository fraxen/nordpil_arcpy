import arcgisscripting, sys, re, os
import time,datetime
from subprocess import call

# {{{ STARTUP STUFF...
# First we need to check that the arguments are ok...
try:
	if len(sys.argv) < 3: raise
	bkFolder = sys.argv[1]
	sdeDatabase = sys.argv[2]
except:
	print "\n\nError:", str(sys.exc_info())
	print "\n\nPlease verify the input arguments\n\narcsdeexport.py <database>\n\n"
	sys.exit()

print "\n\nExporting data from database: " + sdeDatabase

# Initialization...
if (not os.path.exists(bkFolder)):
	os.mkdir(bkFolder)
gp = arcgisscripting.create(9.3)
gp.workspace = "Database Connections\\" + sdeDatabase + '.sde'
gp.SetProduct("ArcInfo")
gp.Overwriteoutput = 1
gp.toolbox = 'management'
outGDB = bkFolder + '/'+ sdeDatabase + '.gdb'
if (not gp.Exists(outGDB)):
	gp.CreateFileGDB(bkFolder,sdeDatabase + '.gdb')
# }}}

print '------\nCOPYING TABLES'
datasets = gp.ListTables()
for dataset in datasets:
	print dataset + "\t\t" + "(table)"
	gp.Copy_management(dataset,outGDB + '/' + dataset.split('.')[len(dataset.split('.'))-1])

print '------\nCOPYING RASTERS'
datasets = gp.ListRasters()
for dataset in datasets:
	print dataset + "\t\t" + "(raster)"
	gp.CopyRaster_management(dataset,outGDB + '/' + dataset.split('.')[len(dataset.split('.'))-1])

print '------\nCOPYING FEATURE CLASSES'
datasets = gp.ListFeatureClasses()
for dataset in datasets:
	print "Copying feature class: " + dataset
	gp.CopyFeatures_management(dataset,outGDB + '/' + dataset.split('.')[len(dataset.split('.'))-1])

if os.path.exists(os.environ.get('PROGRAMFILES') + r'\Growl for Windows\growlnotify.exe'):
	call([os.environ.get('PROGRAMFILES') + r'\Growl for Windows\growlnotify.exe', '/p:2','/t:"ArcSDE Export on ' + os.environ.get('COMPUTERNAME') + '"',r'/ai:"\\palau.grida.no\home\ahlenius\bin\icon_arcgis.png"','Export finished of database' + sdeDatabase])

