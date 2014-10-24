# Script to migrate data from utnes to db.grida.no
import arcgisscripting
import sys
import os
import re
import pyodbc

# {{{ INITIALIZATION
gp = arcgisscripting.create()
# Handle the input arguments
try:
	fromSDE = "Database Connections/" + sys.argv[1] + "/"
except:
	fromSDE = "Database Connections/world_geo.sde/"
try:
	toSDE = "Database Connections/" + sys.argv[2] + "/"
except:
	toSDE = "Database Connections/europe_emep.sde/"
try:
	pattern = sys.argv[3]
except:
	pattern = "*"
try:
	actions = sys.argv[4]
except:
	actions = "feature,raster,table,metadata"
actions = actions.split(",")
actionsAll = "feature,raster,table,metadata".split(",")
actions2 = ["Featureclass migration","Raster migration", "Table listing", "MetaData migration"]

print "\nActions:"
for action in actions:
	print "\t" + actions2[actionsAll.index(action)]
print "\n\n"

# Set up the workspace + initiate database connection
print "Inititating connections..."
gp.workspace = fromSDE
dbDBserver = pyodbc.connect('Driver={SQL Server};Server=db.grida.no;Database=sde;Uid=sde;Pwd=CinderCone;protocol=TCPIP')
dbDBserver.autocommit = True
dbUtnes = pyodbc.connect('Driver={SQL Server};Server=salomon.grida.no;Database=sde;Uid=sde;Pwd=CinderCone;protocol=TCPIP')
# }}}

#{{{ COPY ALL THE FEATURE CLASSES
if "feature" in actions:
	listDataset = gp.ListFeatureClasses(pattern)
	print "\n\nLISTING ALL FEATURE CLASSES"
	listDataset.reset()
	dataset = listDataset.next()
	while dataset:
		shortDatasetName = re.sub("[^\.]+\.[^\.]+\.","",dataset,1).upper()
		try:
			if gp.exists(toSDE + shortDatasetName):
				raise("Feature exists")
			print "Copying " + shortDatasetName
			gp.CopyFeatures(dataset,toSDE + shortDatasetName)
		except:
			print "FAILED COPYING " + dataset + " (feature)"
			print sys.exc_info()
		print "------------------------------------------------------------"
		dataset = listDataset.next()
#}}} 

#{{{ COPY ALL RASTER DATASETS
if "raster" in actions:
	listDataset = gp.ListRasters(pattern)
	print "\n\nLISTING ALL RASTERS"
	listDataset.reset()
	dataset = listDataset.next()
	while dataset:
		try:
			shortDatasetName = re.sub("[^\.]+\.[^\.]+\.","",dataset,1).upper()
			tempName = "_A"
			if gp.exists(toSDE + tempName) == 0:
				gp.workspace = toSDE
				listTemp = gp.ListRasters("*")
				listTemp.reset()
				checkDataset = listTemp.next()
				while checkDataset and tempName == "_A":
					if re.sub("[^\.]+\.[^\.]+\.","",checkDataset,1)[0:4].upper() == "SDE_":
						tempName = re.sub("[^\.]+\.[^\.]+\.","",checkDataset,1).upper()
					checkDataset = listTemp.next()
			gp.workspace = fromSDE
			if gp.exists(toSDE + shortDatasetName):
				raise("Feature exists")
			if gp.exists(toSDE + "_A"):
				# delete the temp raster dataset
				gp.delete(toSDE + "_A")
				print "Deleted existing raster"
			if gp.exists(toSDE + tempName):
				# delete the temp raster dataset
				gp.delete(toSDE + tempName)
				print "Deleted existing raster"
			print "Copying " + shortDatasetName
			tempName = "_A"
			gp.CopyRaster(shortDatasetName,toSDE + tempName,"#","#","#","NONE","NONE","#")
			if gp.exists(toSDE + tempName) == 0:
				gp.workspace = toSDE
				listTemp = gp.ListRasters("*")
				listTemp.reset()
				checkDataset = listTemp.next()
				while checkDataset and tempName == "_A":
					print checkDataset
					if re.sub("[^\.]+\.[^\.]+\.","",checkDataset,1)[0:4].upper() == "SDE_":
						tempName = re.sub("[^\.]+\.[^\.]+\.","",checkDataset,1).upper()
					checkDataset = listTemp.next()
			gp.workspace = fromSDE
			print tempName
			gp.rename(toSDE + tempName, toSDE + shortDatasetName)
		except:
			print "FAILED COPYING " + dataset + " (raster)"
			print sys.exc_info()
		print "------------------------------------------------------------"
		dataset = listDataset.next()
#}}}

#{{{ LIST ALL THE TABLES
# TODO - it is possible to list them, but not to copy them...
if "table" in actions:
	listDataset = gp.listtables(pattern)
	print "\n\nLISTING ALL TABLES"
	listDataset.reset()
	dataset = listDataset.next()
	while dataset:
		shortDatasetName = re.sub("[^\.]+\.[^\.]+\.","",dataset,1).upper()
		print "NEED TO COPY SEPARATELY... " + shortDatasetName
		print "------------------------------------------------------------"
		dataset = listDataset.next()
#}}} 

#{{{ MOVE THE METADATA
gp.workspace = toSDE
if "metadata" in actions:
	def updateMetadata(listDset,dataType):
		listDset.reset()
		dataset = listDset.next()
		while dataset:
			shortDatasetName = re.sub("[^\.]+\.[^\.]+\.","",dataset,1).upper()
			try:
				metarecordUtnes = dbUtnes.execute("SELECT top 1 xml, id, name FROM sde.gdb_usermetadata WHERE DatabaseName = '" + re.sub("[^\.]+\.([^\.]+)\.[^\.]+",r"\1",dataset,1) + "' AND name = '" + shortDatasetName + "' ORDER BY id desc").fetchone()
				if metarecordUtnes:
					metarecordDB = dbDBserver.execute("SELECT top 1 xml, id, name FROM sde.gdb_usermetadata WHERE DatabaseName = '" + re.sub("[^\.]+\.([^\.]+)\.[^\.]+",r"\1",dataset,1) + "' AND  name = '" + shortDatasetName + "' ORDER BY id desc").fetchone()
					if metarecordDB:
						print "Updating metadata record " + shortDatasetName + " " + str(metarecordUtnes.id) + "," + str(metarecordDB.id) + " (Utnes,DB)"
						dbDBserver.execute("UPDATE sde.gdb_usermetadata SET xml=? WHERE id=?", metarecordUtnes.xml, metarecordDB.id)
					else:
						# Get highest id on DB
						metarecordDB = dbDBserver.execute("SELECT top 1 id FROM sde.gdb_usermetadata ORDER BY id desc").fetchone()
						print "Inserting new metadata record " + shortDatasetName + " " + str(metarecordUtnes.id) + "," + str(metarecordDB.id) + " (Utnes,DB)"
						dbDBserver.execute("\
							INSERT INTO\
								sde.gdb_usermetadata (id,DatabaseName,Owner,Name,DatasetType,xml)\
							VALUES (\
								?,\
								'" + re.sub("[^\.]+\.([^\.]+)\.[^\.]+",r"\1",dataset,1) + "',\
								'" + re.sub("[^\.]+\.([^\.]+)\.[^\.]+",r"\1",dataset,1) + "',\
								'" + shortDatasetName + "',\
								'" + str(dataType) + "',\
								?\
							)\
							", metarecordDB.id+1, metarecordUtnes.xml)
				else:
					raise("record not found on Utnes")
			except:
				print "FAILED UPDATING METADATA RECORD " + dataset
				print sys.exc_info()
			print "------------------------------------------------------------"
			dataset = listDset.next()

	print "\n\nLISTING ALL METADATA ENTRIES"
	updateMetadata(gp.ListRasters(pattern),16)
	updateMetadata(gp.ListFeatureClasses(pattern),5)
	updateMetadata(gp.ListTables(pattern),10)
dbUtnes.close()
dbDBserver.close()
#}}}
