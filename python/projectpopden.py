# A little script that splits the Arctic into four tiles, and then does some basic raster processing
# * Subsets the arctic in geog projection to four tiles
# * Then reprojects those separately
# * ...and then mosaics them
import arcgisscripting
gp = arcgisscripting.create(9.3)

gp.Workspace = "u:/ws/grump"
gp.toolbox = "SA"
gp.CheckOutExtension("Spatial")
gp.OverWriteOutput = 1
cellSize_Geo = "MAXOF"
cellSize_Result = 1000

tiles = [['nw', '-180 40 -85 90'], ['sw','-90 40 5 90'],['se','-5 40 95 90'],['ne','85 40 180 90']]

for tile in tiles:
	print "\n\nprocessing tile " + tile[0]
	thisTile = tile[0]
	gp.Extent = tile[1]
	gp.CellSize = cellSize_Geo
	print "subsetting tile " + tile[0]
	gp.SingleOutputMapAlgebra_sa("grump_pd2","grump_pd3" + thisTile)
	gp.Extent = "MAXOF"
	print "reprojecting tile " + tile[0]
	gp.ProjectRaster_management ("grump_pd3" + thisTile, "grump_pd4" + thisTile, "Y:/config/Application Data/ESRI/ArcMap/Coordinate Systems/Arctic LAEA Greenwich.prj", "nearest", cellSize_Result) 

gp.Extent = "MAXOF"
if gp.Exists("grump_pd5"):
	gp.Delete("grump_pd5")
print "\n\nmosaicing tiles..."
gp.MosaicToNewRaster_management ("grump_pd4nw;grump_pd4sw;grump_pd4ne;grump_pd4se", gp.Workspace, "grump_pd5", "#", "#", cellSize_Result, "#", "Mean") 
print "\n\nDone!"
