#CITY OF CHESAPEAKE
#DEPARTMENT OF INFORMATION TECHNOLOGY
#GEOGRAPHIC INFORMATION SYSTEMS DIVISION

#BEGINNING OF PYTHON SCRIPT HEADER****************************************

#NAME:            Duplicate_Mover.py

#USAGE:           

#PURPOSE:         Moves points with duplicate geometry to scatter them
#                 around the original location.  This is one method for
#                 causing the points to be visible (rather than stacked)
#                 in cartographic products.

#NOTE:            Developed w/ Python IDLE 2.4.1 and ArcGIS 9.2.

#DISCLAIMER:      N/A

#ARGUMENTS:
#     REQUIRED:   N/A
#
#     OPTIONAL:   N/A

#CONSTANTS:
#                 GP        -geoprocessor

#VARIABLES:
#                 the_fc    -path of the input featureclass
#                 the_ws    -the output workspace
#                 the_out   -name for the output featureclass
#                 the_dist  -amount of distance for scattering points
#                 okay      -indicates if script should continue
#                 fc_prop   -featureclass properties
#                 shp_fld   -the shape field
#                 fields    -the fields of a featureclass
#                 a_field   -a field returned by fields
#                 uid       -indicates if field for unique identifiers
#                            is OBJECTID or FID
#                 the_index -number for counting through a list
#                 the_cur   -a cursor
#                 the_row   -a row returned by the_cur
#                 the_id    -the OBJECTID or FID of a feature
#                 geom      -a feature's geometry
#                 the_part  -the first part of a feature's geometry
#                 the_str   -stores a string for the short term
#                 str_ind   -index of a location within a string
#                 coord1    -the coordinate of the current feature
#                 coord2    -the coordinate of the previous feature
#                 last_x    -the x value of the last point worked
#                 last_y    -the y value of the last point worked
#                 mov_fac   -a factor that determines magnitude for
#                            moving point (moving factor)
#                 frmla     -an integer for selecting a formula
#                 the_x     -the x value of the point being worked
#                 the_y     -the y value of the point being worked
#                 mov_dist  -amount of distance for moving point along
#                            x axis and/or y axis
#                 new_x     -the new x value of the point being moved
#                 new_y     -the new y value of the point being moved

#LISTS:           the_list  -list of coordinates and OBJECTIDs / FIDs of
#                            all features
#                 the_ids   -list of OBJECTIDs or FIDs of features that
#                            have duplicate geometry (in same order as
#                            the_dups)
#                 the_dups  -list of coordinates and OBJECTIDs or FIDs of
#                            features that have duplicate geometry

#INPUT / CONDITIONS NEEDED:
#   Set variables in portion commented as "CONTROL PANEL":
#      -path of the input featureclass
#      -workspace of output featureclass
#      -a name for output featureclass, which must not already exist
#      -amount of distance (in units of input featureclass)
#          by which points will be moved along x axis and y axis
#   Avoid having output workspace open in other applications while
#      this script runs to avoid schema locking
#   Write permission for output workspace

#PROCESSING (psuedo code)
#   Accept input:
#      -path of input featureclass
#      -path of output workspace
#      -name for output featureclass
#      -amount of distance (in units of input featureclass)
#          by which points will be moved along x axis and y axis
#   The given information is checked for validity
#   Create the output featureclass by exporting the input featureclass
#      to the output workspace
#   For each set of points in output featureclass with duplicate geometry,
#      Allow one of the points to retain its original geometry
#      Scatter the other points around the orignial location with the
#         given amount of distance

#KNOWN BUGS:  N/A

#HISTORY:
#     DATE          PROGRAMMER   ORG   DESCRIPTION
#     12-19-2007    Ivan Brown   GIS   Original Coding

#END OF PYTHON SCRIPT HEADER**********************************************
#BEGINNING OF MAIN BODY***************************************************

print "***** RUNNING Duplicate_Mover SCRIPT *****"

#***** IMPORT MODULES
print "IMPORTING MODULES..."
import arcgisscripting, sys

#***** CREATE GEOPROCESSOR
print "CREATING GEOPROCESSOR..."
GP = arcgisscripting.create()

#***** BEGIN CONTROL PANEL - SET VARIABLES *******************************
print "SETTING VARIABLES..."

#---PATH OF INPUT FEATURECLASS
#   *** USE DOUBLE BACKSLASHES ***
#   *** IF FEATURECLASS IS SHAPEFILE, INCLUDE THE .shp FILE EXTENSION ***
#   *** IF FEATURECLASS IS IN GEODATABASE, INCLUDE THE APPROPRIATE FILE
#       EXTENSION IN THE PATH ***
the_fc = "C:\\temp_work\\test_duplicates\\the_gdb.gdb\\as_gdb"

#---PATH OF OUTPUT WORKSPACE (GEODATABASE OR DIRECTORY)
#   *** USE DOUBLE BACKSLASHES ***
#   *** IF OUTPUT WORKSPACE IS A GEODATABASE, INCLUDE FILE EXTENSION,
#          IF APPLICABLE ***
the_ws = "C:\\temp_work\\test_duplicates\\the_gdb.gdb"

#---NAME FOR OUTPUT FEATURECLASS
#   *** JUST THE NAME, NOT THE PATH ***
#   *** IF OUTPUT FEATURECLASS IS SHAPEFILE,
#       INCLUDE .shp FILE EXTENSION ***
the_out = "friday"

#---AMOUNT OF DISTANCE (IN UNITS OF INPUT FEATURECLASS)
#      BY WHICH POINTS WILL BE MOVED ALONG X AXIS AND Y AXIS
#   *** DO NOT INCLUDE QUOTES, VARIABLE MUST BE NUMERIC ***
the_dist = 20

#***** END CONTROL PANEL *************************************************

#***** DISPLAY SETTINGS SET IN CONTROL PANEL, CONFIRM SETTINGS
print "VARIABLE SETTINGS---"
print "   THE INPUT FEATURECLASS IS:  " + the_fc
print "   THE OUTPUT WORKSPACE IS:  " + the_ws
print "   THE NAME FOR OUTPUT FEATURECLASS IS:  " + the_out
print "   THE AMOUNT OF DISTANCE FOR SCATTERING POINTS IS:  " + str(the_dist)
print "ARE THE VARIABLE SETTINGS OKAY?  ENTER Y FOR YES OR N FOR NO."
okay = raw_input("ENTER Y FOR YES OR N FOR NO: ")
okay = okay.upper()
if okay != "Y":
    print "SCRIPT TERMINATED."
    raw_input("PRESS ENTER TO EXIT.")
    sys.exit()

#***** VERIFY VALIDITY OF SETTINGS
print "VERIFYING VALIDITY OF SETTINGS..."

#----- CHECK PATH OF GIVEN INPUT FEATURECLASS
print "CHECKING PATH OF INPUT FEATURECLASS..."
if GP.Exists(the_fc) == 0:
    print "GIVEN INPUT FEATURECLASS DOES NOT EXIST.  SCRIPT TERMINATED."
    raw_input("PRESS ENTER TO EXIT.")
    sys.exit()

#----- MAKE SURE INPUT FEATURECLASS IS A POINT FEATURECLASS
print "MAKING SURE INPUT FEATURECLASS IS A POINT FEATURECLASS..."
fc_prop = GP.Describe(the_fc)
if fc_prop.ShapeType != "Point":
    print "INPUT FEATURECLASS IS A " + fc_prop.ShapeType + " FEATURECLASS."
    print "THIS SCRIPT REQUIRES A POINT FEATURECLASS."
    print "SCRIPT TERMINATED."
    raw_input("PRESS ENTER TO EXIT.")
    sys.exit()

#----- MAKE SURE OUTPUT WORKSPACE EXISTS
print "MAKING SURE OUTPUT WORKSPACE EXISTS..."
if GP.Exists(the_ws) == 0:
    print "GIVEN OUTPUT WORKSPACE DOES NOT EXIST.  SCRIPT TERMINATED."
    raw_input("PRESS ENTER TO EXIT.")
    sys.exit()

#----- SET WORKSPACE PROPERTY OF GEOPROCESSOR TO OUTPUT WORKSPACE
print "SETTING WORKSPACE PROPERTY OF GEOPROCESSOR TO GIVEN OUTPUT WORKSPACE..."
GP.Workspace = the_ws

#----- MAKE SURE OUTPUT FEATURECLASS DOES NOT ALREADY EXIST
print "MAKING SURE OUTPUT FEATURECLASS DOES NOT ALREADY EXIST..."
if GP.Exists(the_out) == 1:
    print "GIVEN OUTPUT FEATURECLASS ALREADY EXISTS.  SCRIPT TERMINATED."
    raw_input("PRESS ENTER TO EXIT.")
    sys.exit()

#***** CREATE THE OUTPUT FEATURECLASS
print "CREATING OUTPUT FEATURECLASS BY EXPORTING INPUT FEATURECLASS..."
GP.FeatureclassToFeatureclass_conversion(the_fc, the_ws, the_out)

#***** FIND SHAPE FIELD
print "FINDING SHAPE FIELD..."
fc_prop = GP.Describe(the_out)
shp_fld = fc_prop.ShapeFieldName

#***** FIND FIELD THAT IS FOR UNIQUE IDENTIFIERS
print "FINDING FIELD THAT IS FOR UNIQUE IDENTIFIERS..."
fields = GP.ListFields(the_out)
a_field = fields.Next()
while a_field:
    if a_field.Name == "OBJECTID":
        uid = "OBJECTID"
        a_field = None
    elif a_field.Name == "FID":
        uid = "FID"
        a_field = None
    else:
        a_field = fields.Next()
print "FIELD FOR UNIQUE IDENTIFIERS IS:  " + uid

#***** WRITE COORDINATES AND OBJECTIDs / FIDs INTO A SORTED LIST (SORT BY X)
print "WRITING A SORTED LIST OF COORDINATES AND OBJECTIDS / FIDS ..."
the_list = [""]
the_index = 0
the_cur = GP.SearchCursor(the_out)
the_row = the_cur.Next()
while the_row:
    the_id = the_row.GetValue(uid)
    geom = the_row.GetValue(shp_fld)
    the_part = geom.GetPart()
    the_str = str(the_part.x) + "_" + str(the_part.y) + "_" + str(the_id)
    the_list[the_index] = the_str
    the_row = the_cur.Next()
    if the_row:
        the_list.append("")
        the_index = the_index + 1
#SORT THE LIST
the_list.sort()

#***** WRITE LIST FEATURES TO BE MOVED AND LIST OF OLD COORDINATES
print "WRITING LIST OF FEATURES TO BE MOVED AND LIST OF OLD COORDINATES..."
the_ids = [""]
the_dups = [""]
#----- (STARTING WITH INDEX 1 BECAUSE LOOP COMPARES FEATURE TO PREVIOUS FEATURE)
the_index = 1
while the_index < len(the_list):
    #GET THE COORDINATE OF THIS FEATURE
    the_str = the_list[the_index]
    str_ind = the_str.find("_")
    str_ind = the_str.find("_", str_ind + 1)
    coord1 = the_str[0:str_ind]
    #GET THE FEATURE'S UNIQUE ID
    the_id = long(the_str[str_ind + 1: len(the_str)])
    #GET THE COORDINATE OF THE PREVIOUS FEATURE
    the_str = the_list[the_index - 1]
    str_ind = the_str.find("_")
    str_ind = the_str.find("_", str_ind + 1)
    coord2 = the_str[0:str_ind]
    #IF COORDINATE OF THIS FEATURE AND COORDINATE OF PREVIOUS FEATURE ARE SAME,
    #   THIS FEATURE HAS DUPLICATE GEOMETRY, ADD IT TO THE LIST
    if coord1 == coord2:
        print "FEATURE " + str(the_id) + " HAS DUPLICATE GEOMETRY, ADDING IT TO LISTS..."
        #IF THIS IS THE FIRST DUPLICATE FOUND, SIMPLY SET TO INDEX 0 IN LISTS
        if the_ids[0] == "":
            #THE LIST OF OBJECTIDs OR FIDs
            the_ids[0] = the_id
            #THE LIST OF OLD COORDINATES
            the_dups[0] = coord1
        #OTHERWISE, APPEND THE ID AND COORDINATE TO THE LISTS
        else:
            #THE LIST OF OBJECTIDs OR FIDs
            the_ids.append(the_id)
            #THE LIST OF OLD COORDINATES
            the_dups.append(coord1)
    the_index = the_index + 1
    
#***** IF NO DUPLICATE FEATURES FOUND, INFORM USER AND EXIT SCRIPT
if the_ids[0] == "":
    print "NO DUPLICATE FEATURES FOUND.  NO FEATURES WILL BE MOVED."
    print "SCRIPT COMPLETED."
    #DELETE CURSOR
    del the_cur
    raw_input("PRESS ENTER TO EXIT.")
    sys.exit()

#***** DETERMINE NEW COORDINATES OF POINTS
print "WILL DETERMINE NEW COORDINATES OF POINTS..."
last_x = None
last_y = None
mov_fac = 0
frmla = 0
the_index = 0
while the_index < len(the_dups):
    #GET COORDINATE FROM THE LIST
    the_str = the_dups[the_index]
    #GET THE X VALUE OF THIS FEATURE
    str_ind = the_str.find("_")
    the_x = the_str[0:str_ind]
    the_x = float(the_x)
    #GET THE Y VALUE OF THIS FEATURE
    the_y = the_str[str_ind + 1:len(the_str)]
    the_y = float(the_y)
    print "WORKING FEATURE " + str(the_ids[the_index]) + " ..."
    #IF COORDINATE OF THIS FEATURE IS SAME AS COORDINATE OF LAST,
    #   ADJUST THE frmla (FORMULA NUMBER) VARIABLE
    #   ADJUST THE mov_fac (MOVING FACTOR) VARIABLE,
    #      IF HAVE COMPLETED A CYCLE OF 8 FORMULAS FOR THIS LOCATION
    #      (THERE ARE 8 FORMULAS)
    if the_x == last_x and the_y == last_y:
        #IF frmla (FORMULA NUMBER) IS LESS THAN 8 (THERE ARE 8 FORMULAS),
        #   ADD 1 TO frmla
        if frmla < 8:
            frmla = frmla + 1
        #OTHERWISE, SET frmla TO 1, TO RETURN TO FIRST FORMULA,
        #   AND ADD 1 TO mov_fac VARIABLE
        else:
            frmla = 1
            mov_fac = mov_fac + 1
    #OTHERWISE,
    #   RESET THE mov_fac (MOVING FACTOR) VARIABLE TO 1
    #   RESET THE frmla (FORMULA NUMBER) VARIABLE TO 1
    else:
        mov_fac = 1
        frmla = 1
    #SET last_x AND last_y VARIABLES TO CAPTURE COORDINATE OF THIS FEATURE
    #   BEFORE COORDINATE ADJUSTMENT
    last_x = the_x
    last_y = the_y
    #ADJUST THE COORDINATE WITH ONE OF 8 FORMULAS
    mov_dist = the_dist * mov_fac
    #   NORTH
    if frmla == 1:
        the_y = the_y + mov_dist
        print "THE FEATURE WILL BE MOVED " + str(mov_dist) + " UNITS TOWARD THE NORTH..."
    #   NORTHEAST
    elif frmla == 2:
        the_x = the_x + mov_dist
        the_y = the_y + mov_dist
        print "THE FEATURE WILL BE MOVED " + str(mov_dist) + " UNITS TOWARD THE NORTH AND EAST..."
    #   EAST
    elif frmla == 3:
        the_x = the_x + mov_dist
        print "THE FEATURE WILL BE MOVED " + str(mov_dist) + " UNITS TOWARD THE EAST..."
    #   SOUTHEAST
    elif frmla == 4:
        the_x = the_x + mov_dist
        the_y = the_y - mov_dist
        print "THE FEATURE WILL BE MOVED " + str(mov_dist) + " UNITS TOWARD THE SOUTH AND EAST..."
    #   SOUTH
    elif frmla == 5:
        the_y = the_y - mov_dist
        print "THE FEATURE WILL BE MOVED " + str(mov_dist) + " UNITS TOWARD THE SOUTH..."
    #   SOUTHWEST
    elif frmla == 6:
        the_x = the_x - mov_dist
        the_y = the_y - mov_dist
        print "THE FEATURE WILL BE MOVED " + str(mov_dist) + " UNITS TOWARD THE SOUTH AND WEST..."
    #   WEST
    elif frmla == 7:
        the_x = the_x - mov_dist
        print "THE FEATURE WILL BE MOVED " + str(mov_dist) + " UNITS TOWARD THE WEST..."
    #   NORTHWEST
    else:
        the_x = the_x - mov_dist
        the_y = the_y + mov_dist
        print "THE FEATURE WILL BE MOVED " + str(mov_dist) + " UNITS TOWARD THE NORTH AND WEST..."
    #RE-WRITE ENTRY IN THE LIST OF DUPLICATE COORDINATES WITH ADJUSTED COORDINATE
    the_dups[the_index] = str(the_x) + "_" + str(the_y)
    the_index = the_index + 1

#***** SCATTER THE DUPLICATE POINTS
print "WILL SCATTER THE DUPLICATE POINTS..."
#----- CREATE AN UPDATE CURSOR FOR OUTPUT FEATURECLASS
the_cur = GP.UpdateCursor(the_out)
the_row = the_cur.Next()
while the_row:
    #   GET THE FEATURE'S UNIQUE ID
    the_id = the_row.GetValue(uid)
    #   SEARCH FOR THE UNIQUE ID IN THE LIST OF FEATURES TO BE MOVED
    the_index = 0
    while the_index < len(the_ids):
        if the_ids[the_index] == the_id:
            print "MOVING POINT FOR FEATURE " + str(the_id) + " ..."
            the_str = the_dups[the_index]
            str_ind = the_str.find("_")
            new_x = the_str[0:str_ind]
            new_x = float(new_x)
            new_y = the_str[str_ind + 1:len(the_str)]
            new_y = float(new_y)
            geom = the_row.GetValue(shp_fld)
            the_part = geom.GetPart()
            the_part.x = new_x
            the_part.y = new_y
            the_row.SetValue(shp_fld, the_part)
            the_cur.UpdateRow(the_row)
            the_index = len(the_ids)
        the_index = the_index + 1
    the_row = the_cur.Next()

#***** DELETE CURSOR
print "DUPLICATE POINTS HAVE BEEN SCATTERED..."
del the_cur

#***** SCRIPT COMPLETED
raw_input("SCRIPT COMPLETED.  PRESS ENTER TO EXIT.")
