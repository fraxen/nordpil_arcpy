import arcgisscripting, sys, re, os

# {{{ STARTUP STUFF...
# First we need to check that the arguments are ok...
try:
	if len(sys.argv) == 0: raise
	thisWorkspace = sys.argv[1].replace('\\','/')
	try:
		pattern = sys.argv[2]
	except:
		pattern = "*"
except:
	print "\n\nError:", str(sys.exc_info())
	print "\n\nPlease verify the input arguments\n\nlsws.py <workspace> [pattern]\n\n"
	sys.exit()

print "\n\nListing workspace: " + thisWorkspace + ", with pattern <" + pattern + ">\n\n"

# Initialization...
gp = arcgisscripting.create(9.3)
gp.workspace = thisWorkspace
# }}}

# {{{ LIST ALL FEATURE CLASSES
datasets = gp.ListFeatureClasses(pattern)
for dataset in datasets:
	print dataset + "\t\t" + "(feature class)"
datasets = gp.ListRasters(pattern)
for dataset in datasets:
	print dataset + "\t\t" + "(raster)"
datasets = gp.ListTables(pattern)
for dataset in datasets:
	print dataset + "\t\t" + "(table)"
# }}}


