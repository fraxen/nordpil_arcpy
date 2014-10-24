# A little script that calculates the area of each grid cells
# Area output is in sqkm!!!
# Will only work for WGS84 lat/lon grids!

import arcgisscripting, sys, os, math
# {{{ STARTUP STUFF...
# First we need to check that the arguments are ok...
gp = arcgisscripting.create(9.3)

try:
	if len(sys.argv) == 0: raise
	inGrid = sys.argv[1].replace('\\','\\\\')
	outGrid = sys.argv[2].replace('\\','\\\\')
	try:
		thisWorkspace = sys.argv[3].replace('\\','\\\\')
	except:
		thisWorkspace = gp.Workspace
except:
	print "\n\nError:", str(sys.exc_info())
	print "\n\nPlease verify the input arguments\n\ncalculategridarea.py <input grid> <output grid> [workspace]\n\n"
	sys.exit()

print "\nCalculating the grid cell area of :\n....." + inGrid + "\nand creating output grid\n....." + outGrid + "\nin workspace\n....." + thisWorkspace + "\n"

tempWs = os.environ["temp"]

# }}}

gp.toolbox = "SA"
gp.CheckOutExtension("Spatial")
gp.OverWriteOutput = 1

desc = gp.describe(inGrid)

gp.CellSize = desc.MeanCellHeight
gp.Extent = desc.Extent

cellSizeMeters = float(gp.CellSize) * 111120
cellArea = cellSizeMeters * cellSizeMeters
halfCellWidth = float(cellSizeMeters) / 2
earthRadius = 6371
oneDeginRad = 0.0174532925
cellSizeinRad = float(gp.cellSize) * ((2*math.pi) /360)
halfaDeginRad = 0.00872664625

gp.Workspace = tempWs

#SETWINDOW -180 -90 180 90
#SETCELL 0.5
#&SETVAR oneDeginRad = 0.0174532925
#&SETVAR halfaDeginRad = 0.00872664625
#worldxl1 = float(($$colmap * .5) - 180) * %oneDeginRad%
gp.SingleOutputMapAlgebra_sa ("float(($$colmap * " + str(gp.CellSize) + ") - " + str(desc.Extent.xMax) +") * " + str(oneDeginRad), "worldxl1")
#worldxr1 = worldxl1 + %halfaDeginRad%
gp.SingleOutputMapAlgebra_sa ("worldxl1 + " + str(cellSizeinRad), "worldxr1")
#worldyt1 = - float( ($$rowmap * .5) - 90) * %oneDeginRad%
gp.SingleOutputMapAlgebra_sa ("-1 * (float( ($$rowmap * " + str(gp.CellSize) + ") - " + str(desc.Extent.yMax) + ") * "+ str(oneDeginRad) + ")", "worldyt1")
#worldyb1 = worldyt1 - %halfaDeginRad%
gp.SingleOutputMapAlgebra_sa ("worldyt1 - " + str(cellSizeinRad), "worldyb1")
#term1 = earthRadius * earthRadius
gp.SingleOutputMapAlgebra_sa ("6371 * 6371", "term1")
#term2 = worldxr1 - worldxl1
#term3a = sin (worldyt1)
#term3b = sin (worldyb1)
#term3 = term3a - term3b
#worldarea1 = term1 * term2 * term3
gp.SingleOutputMapAlgebra_sa ("worldxr1 - worldxl1","term2")
gp.SingleOutputMapAlgebra_sa ("sin (worldyt1)","term3a")
gp.SingleOutputMapAlgebra_sa ("sin (worldyb1)","term3b")
gp.SingleOutputMapAlgebra_sa ("term3a - term3b","term3")
gp.SingleOutputMapAlgebra_sa ("term1 * term2 * term3","worldarea1")

gp.DefineProjection_management("worldarea1","GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")

gp.copy ("worldarea1", thisWorkspace + "/" + outGrid)

print "\n\nCalculation complete, created: " + thisWorkspace + "/" + outGrid + "\n\n"

