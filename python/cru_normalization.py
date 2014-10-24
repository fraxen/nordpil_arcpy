# My little script to try to normalize the heavy txt files supplied with the CGIAR formatted CRU TS 2.1
# Works with an access database
import pyodbc
import subprocess
import os

cnxn = pyodbc.connect('DRIVER=MySQL ODBC 5.1 Driver;SERVER=localhost;DATABASE=cruts21;UID=root;PWD=AlGlut')
cursor = cnxn.cursor()

# {{{ ACTUAL DATA
for Variable in ['cld','dtr','frs','pre','tmn','tmp','tmx','vap','wet']:
	print '\n\n-----\nVariable: ' + Variable
	cursor.execute("DROP TABLE IF EXISTS "+Variable);
	cnxn.commit()
	cursor.execute("CREATE TABLE `"+Variable+"` (`RowID` bigint(20) NOT NULL AUTO_INCREMENT,`CellID` bigint(20) NOT NULL,`DataYear` bigint(20) NOT NULL,`M1` bigint(20) NOT NULL,`M2` bigint(20) NOT NULL,`M3` bigint(20) NOT NULL,`M4` bigint(20) NOT NULL,`M5` bigint(20) NOT NULL,`M6` bigint(20) NOT NULL,`M7` bigint(20) NOT NULL,`M8` bigint(20) NOT NULL,`M9` bigint(20) NOT NULL,`M10` bigint(20) NOT NULL,`M11` bigint(20) NOT NULL,`M12` bigint(20) NOT NULL,PRIMARY KEY (`RowID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
	cnxn.commit()
	for Period in ['1901-1920','1921-1940','1941-1960','1961-1980','1981-2000','2001-2002']:
		print '-- Setting up tables for : ' + Period + ' ('+Variable+')'
		startYear = int(Period.split('-')[0])
		endYear = int(Period.split('-')[1])
		dataField = ""
		ignoreFields = "id"
		for popYear in range(startYear,endYear+1):
			for month in range(1,13):
				dataField = dataField + ',`M'+str(month)+'Y'+str(popYear)+'` bigint(20) NOT NULL'
				ignoreFields = ignoreFields + ',M' + str(month) + 'Y'+ str(popYear)
		cursor.execute("DROP TABLE IF EXISTS `"+Variable+"_"+Period+"_data`")
		cursor.execute("CREATE TABLE `"+Variable+"_"+Period+"_data` (`Id` bigint(20) NOT NULL"+dataField+",PRIMARY KEY (`Id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
		print '-- Loading data from: ' + Variable+'_'+Period+'_data.txt'
		cursor.execute("LOAD DATA INFILE 'c:/mnt/data/ws/cruts/global_DATA/"+Variable+"_"+Period+"_data.txt' INTO TABLE `"+Variable+"_"+Period+"_data` FIELDS TERMINATED BY ',' IGNORE 1 LINES ("+ignoreFields+");")
		cnxn.commit()
		for popYear in range(startYear,endYear+1):
			popYear = str(popYear)
			print '-- -- Normalizing year ' + popYear + ' ('+Variable+')'
			cursor.execute("INSERT INTO "+Variable+" (CellID, DataYear, M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12) SELECT ID AS CellID, "+popYear+" AS DataYear, M1Y"+popYear+" AS M1, M2Y"+popYear+" AS M2, M3Y"+popYear+" AS M3, M4Y"+popYear+" AS M4, M5Y"+popYear+" AS M5, M6Y"+popYear+" AS M6, M7Y"+popYear+" AS M7, M8Y"+popYear+" AS M8, M9Y"+popYear+" AS M9, M10Y"+popYear+" AS M10, M11Y"+popYear+" AS M11, M12Y"+popYear+" AS M12 FROM `"+Variable+"_"+Period+"_data`;")
			cnxn.commit()
# }}}

# {{{ STATION RECORD
for Variable in ['cld','dtr','pre','tmp','vap','wet']:
	print '\n\n-----\nVariable: ' + Variable + " - station record"
	cursor.execute("DROP TABLE IF EXISTS "+Variable+"_stn");
	cnxn.commit()
	cursor.execute("CREATE TABLE `"+Variable+"_stn` (`RowID` bigint(20) NOT NULL AUTO_INCREMENT,`CellID` bigint(20) NOT NULL,`DataYear` bigint(20) NOT NULL,`M1` bigint(20) NOT NULL,`M2` bigint(20) NOT NULL,`M3` bigint(20) NOT NULL,`M4` bigint(20) NOT NULL,`M5` bigint(20) NOT NULL,`M6` bigint(20) NOT NULL,`M7` bigint(20) NOT NULL,`M8` bigint(20) NOT NULL,`M9` bigint(20) NOT NULL,`M10` bigint(20) NOT NULL,`M11` bigint(20) NOT NULL,`M12` bigint(20) NOT NULL,PRIMARY KEY (`RowID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
	cnxn.commit()
	for Period in ['1901-1920','1921-1940','1941-1960','1961-1980','1981-2000','2001-2002']:
		print '-- Setting up tables for : ' + Period + ' ('+Variable+') - station record'
		startYear = int(Period.split('-')[0])
		endYear = int(Period.split('-')[1])
		dataField = ""
		ignoreFields = "id"
		for popYear in range(startYear,endYear+1):
			for month in range(1,13):
				dataField = dataField + ',`M'+str(month)+'Y'+str(popYear)+'` bigint(20) NOT NULL'
				ignoreFields = ignoreFields + ',M' + str(month) + 'Y'+ str(popYear)
		cursor.execute("DROP TABLE IF EXISTS `"+Variable+"_"+Period+"_stn`")
		cursor.execute("CREATE TABLE `"+Variable+"_"+Period+"_stn` (`Id` bigint(20) NOT NULL"+dataField+",PRIMARY KEY (`Id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
		print '-- Loading data from: ' + Variable+'_'+Period+'_stn.txt'
		cursor.execute("LOAD DATA INFILE 'c:/mnt/data/ws/cruts/global_stn/"+Variable+"_"+Period+"_stn.txt' INTO TABLE `"+Variable+"_"+Period+"_stn` FIELDS TERMINATED BY ',' IGNORE 1 LINES ("+ignoreFields+");")
		cnxn.commit()
		for popYear in range(startYear,endYear+1):
			popYear = str(popYear)
			print '-- -- Normalizing year ' + popYear + ' ('+Variable+') - station record'
			cursor.execute("INSERT INTO "+Variable+"_stn (CellID, DataYear, M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12) SELECT ID AS CellID, "+popYear+" AS DataYear, M1Y"+popYear+" AS M1, M2Y"+popYear+" AS M2, M3Y"+popYear+" AS M3, M4Y"+popYear+" AS M4, M5Y"+popYear+" AS M5, M6Y"+popYear+" AS M6, M7Y"+popYear+" AS M7, M8Y"+popYear+" AS M8, M9Y"+popYear+" AS M9, M10Y"+popYear+" AS M10, M11Y"+popYear+" AS M11, M12Y"+popYear+" AS M12 FROM `"+Variable+"_"+Period+"_stn`;")
			cnxn.commit()
# }}}
cnxn.close()

# ALSO - LOAD COORDINATES! (don't forget to have the ll coords as floating point

# ADD INDEXES...
# ALTER TABLE pre ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE cld ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE dtr ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE frs ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE tmn ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE tmp ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE tmx ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE vap ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE wet ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);

# ALTER TABLE cld_stn ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE dtr_stn ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE pre_stn ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE tmp_stn ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE vap_stn ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
# ALTER TABLE wet_stn ADD INDEX CellIndex (CellID), ADD INDEX YearIndex (DataYear), ADD INDEX CellYear (CellID,DataYear);
