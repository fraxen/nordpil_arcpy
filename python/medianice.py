# A little script that griddifies a bunch of shape files and then takes the median extent
# for the arctic sea ice
# * rasterize shapefiles
# * get median
# * convert back to polygons
# * reproject
import arcgisscripting
gp = arcgisscripting.create(9.3)

gp.Workspace = "u:/ws/ice"
gp.toolbox = "SA"
gp.CheckOutExtension("Spatial")
gp.OverWriteOutput = 1
cellSize_PS = 1000
outCS = "Y:/config/Application Data/ESRI/ArcMap/Coordinate Systems/Arctic LAEA Greenwich.prj"
gp.Extent = "MAXOF"
gp.CellSize = cellSize_PS

for month in ["09","03"]:
	for year in range(1979,2000):
		thisYear = str(year)
		print "\n\nRasterizing year " + thisYear
		gp.FeatureToRaster_conversion("extent_N_" + thisYear + month + "_polygon.shp", "INDEX", "ice" + thisYear + month + "_2", gp.CellSize)
		print "Cleaning up year " + thisYear
		gp.SingleOutputMapAlgebra_sa("SETNULL(ISNULL(ice" + thisYear + month + "_2),1)","ice" + thisYear + month + "_3")

	sumString = ""
	for year in range(1979,2000):
		thisGrid = "ice" + str(year) + month + "_3"
		sumString = sumString + "con(ISNULL(" + thisGrid + "),0,1) + "

	print "\n\nSumming up the years..."
	gp.SingleOutputMapAlgebra_sa(sumString + "0","ice" + month + "_4")
	print "\n\nGrabbing the median"
	gp.SingleOutputMapAlgebra_sa("SETNULL(ice" + month + "_4 LT 11,1)","ice" + month + "_5")
	gp.RasterToPolygon_conversion("ice" + month + "_5", "ice" + month + "_6.shp", "NO_SIMPLIFY")
	gp.Project_management ("ice" + month + "_6.shp","ice" + month + "_7.shp",outCS)
