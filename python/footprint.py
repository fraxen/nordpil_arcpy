# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#  This Python script creates a raster footprint featureclass
# ---------------------------------------------------------------------------
#   Name:          footprint
#   Version:       1.0
#   Authored by:   Hugo Ahlenius, Nordpil - http://nordpil.com
#
#   License:       Creative Commons Attribution 3.0 Unported License
# ---------------------------------------------------------------------------

import sys
import arcpy


def main(inRaster, outPoly):
    if not arcpy.Exists(inRaster):
        arcpy.AddError('Input raster: %s does not exist' % inRaster)
        raise StandardError
    if outPoly is None:
        outPoly = inRaster + '_fp'

    # Get properties for the specified raster dataset
    propsInRaster = arcpy.Describe(inRaster)

    # {{{ Create a polygon for the featureList array
    point = arcpy.Point()
    array = arcpy.Array()
    featureList = []
    point.X = propsInRaster.extent.XMin
    point.Y = propsInRaster.extent.YMin
    array.add(point)
    point.X = propsInRaster.extent.XMin
    point.Y = propsInRaster.extent.YMax
    array.add(point)
    point.X = propsInRaster.extent.XMax
    point.Y = propsInRaster.extent.YMax
    array.add(point)
    point.X = propsInRaster.extent.XMax
    point.Y = propsInRaster.extent.YMin
    array.add(point)
    array.add(array.getObject(0))
    polygon = arcpy.Polygon(array)
    featureList.append(polygon)
    # }}}

    arcpy.CopyFeatures_management(featureList, outPoly)

    # Did we just create a shapefile?
    if arcpy.Exists(outPoly + '.shp'):
        outPoly = outPoly + '.shp'
    arcpy.DefineProjection_management(outPoly, propsInRaster.spatialReference)
    del featureList
    del point
    del array
    del polygon

    arcpy.AddMessage('Created polygon fc %s from outline of %s' % (outPoly, inRaster))

    # Here I am trying to add it to current ArcMap pane,
    # if run from the ArcMap python console/pane,
    # but it doesn't seem to work... I guess it returns false here...
    try:
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        outLayer = arcpy.mapping.Layer(outPoly)
        arcpy.mapping.AddLayer(df, outLayer)
    except:
        pass

    return


if __name__ == '__main__':
    if arcpy.GetParameterAsText(0):
        arguments = tuple(
            arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount())
        )
    else:
        arguments = sys.argv[1:]

    try:
        inRaster = arguments[0]
        try:
            outPoly = arguments[1]
        except IndexError:
            outPoly = None
    except Exception, e:
            print 'footprint - creates polygon based on raster footprint'
            print 'Usage: footprint.py <input raster> [output polygon features]'
            print 'Can be run from the prompt, imported as module and run as a toolbox script'
            print 'To run as a module:'
            print '   import footprint'
            print '   footprint.main(<input raster>,[output polygon features])'
            sys.exit()
    main(inRaster, outPoly)
