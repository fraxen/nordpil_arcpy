from xml.etree import ElementTree
import arcpy

arcpy.env.workspace = r'C:\Users\hugo\checkout\PackDLMap'

document = ElementTree.parse(r'C:\Users\hugo\checkout\PackDLMap\h22ka07212.xml')

arcpy.CreateFeatureclass_management(r'C:\Users\hugo\checkout\PackDLMap', 'polys1.shp', 'Polygon')
arcpy.AddField_management('polys1.shp', 'ID', 'LONG')
arcpy.AddField_management('polys1.shp', 'AREA', 'FLOAT')
arcpy.AddField_management('polys1.shp', 'PERIMETER', 'FLOAT')
arcpy.AddField_management('polys1.shp', 'H22KA07_', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA07_ID', 'LONG')
arcpy.AddField_management('polys1.shp', 'KEN', 'TEXT')
arcpy.AddField_management('polys1.shp', 'CITY', 'TEXT')
arcpy.AddField_management('polys1.shp', 'KEN_NAME', 'TEXT')
arcpy.AddField_management('polys1.shp', 'SITYO_NAME', 'TEXT')
arcpy.AddField_management('polys1.shp', 'GST_NAME', 'TEXT')
arcpy.AddField_management('polys1.shp', 'CSS_NAME', 'TEXT')
arcpy.AddField_management('polys1.shp', 'HCODE', 'LONG')
arcpy.AddField_management('polys1.shp', 'KIHON1', 'TEXT')
arcpy.AddField_management('polys1.shp', 'DUMMY1', 'TEXT')
arcpy.AddField_management('polys1.shp', 'KIHON2', 'TEXT')
arcpy.AddField_management('polys1.shp', 'KEYCODE1', 'TEXT')
arcpy.AddField_management('polys1.shp', 'KEYCODE2', 'TEXT')
arcpy.AddField_management('polys1.shp', 'AREA_MAX_F', 'TEXT')
arcpy.AddField_management('polys1.shp', 'KIGO_D', 'TEXT')
arcpy.AddField_management('polys1.shp', 'N_KEN', 'TEXT')
arcpy.AddField_management('polys1.shp', 'N_CITY', 'TEXT')
arcpy.AddField_management('polys1.shp', 'N_C1', 'LONG')
arcpy.AddField_management('polys1.shp', 'KIGO_E', 'TEXT')
arcpy.AddField_management('polys1.shp', 'KIGO_I', 'TEXT')
arcpy.AddField_management('polys1.shp', 'TATE', 'LONG')
arcpy.AddField_management('polys1.shp', 'DIR', 'LONG')
arcpy.AddField_management('polys1.shp', 'HIGHT', 'LONG')
arcpy.AddField_management('polys1.shp', 'JIKAKU', 'LONG')
arcpy.AddField_management('polys1.shp', 'NMOJI', 'LONG')
arcpy.AddField_management('polys1.shp', 'MOJI', 'TEXT')
arcpy.AddField_management('polys1.shp', 'SEQ_NO2', 'LONG')
arcpy.AddField_management('polys1.shp', 'KSUM', 'LONG')
arcpy.AddField_management('polys1.shp', 'CSUM', 'LONG')
arcpy.AddField_management('polys1.shp', 'JINKO', 'FLOAT')
arcpy.AddField_management('polys1.shp', 'SETAI', 'FLOAT')
arcpy.AddField_management('polys1.shp', 'X_CODE', 'FLOAT')
arcpy.AddField_management('polys1.shp', 'Y_CODE', 'FLOAT')
arcpy.AddField_management('polys1.shp', 'KCODE1', 'TEXT')
arcpy.AddField_management('polys1.shp', 'KEY_CODE', 'TEXT')
arcpy.AddField_management('polys1.shp', 'H22KA08_', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA08_ID', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA09_', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA09_ID', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA10_', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA10_ID', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA11_', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA11_ID', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA12_', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA12_ID', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA13_', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA13_ID', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA14_', 'LONG')
arcpy.AddField_management('polys1.shp', 'H22KA14_ID', 'LONG')
fields = [
    'ID', 'AREA', 'PERIMETER', 'H22KA07_', 'H22KA07_ID', 'KEN', 'CITY', 'KEN_NAME',
    'SITYO_NAME', 'GST_NAME', 'CSS_NAME', 'HCODE', 'KIHON1', 'DUMMY1', 'KIHON2', 'KEYCODE1',
    'KEYCODE2', 'AREA_MAX_F', 'KIGO_D', 'N_KEN', 'N_CITY', 'N_C1', 'KIGO_E', 'KIGO_I', 'TATE',
    'DIR', 'HIGHT', 'JIKAKU', 'NMOJI', 'MOJI', 'SEQ_NO2', 'KSUM', 'CSUM', 'JINKO', 'SETAI',
    'X_CODE', 'Y_CODE', 'KCODE1', 'KEY_CODE', 'H22KA08_', 'H22KA08_ID', 'H22KA09_', 'H22KA09_ID',
    'H22KA10_', 'H22KA10_ID', 'H22KA11_', 'H22KA11_ID', 'H22KA12_', 'H22KA12_ID', 'H22KA13_',
    'H22KA13_ID', 'H22KA14_', 'H22KA14_ID'
]
cursor = arcpy.da.InsertCursor('polys1.shp', ['SHAPE@'] + fields)

for feat in document.findall(u'.//GeometricFeature'):
    print feat.attrib['id']
    array = arcpy.Array()
    for pnt in feat.findall('.//LinearRing/Coordinates')[0].text.split(' '):
        thisPoint = [float(x) for x in pnt.split(',')]
        array.add(arcpy.Point(thisPoint[0], thisPoint[1]))
    poly = [arcpy.Polygon(array)]
    poly.append(feat.attrib['id'])
    for field in fields:
        if field == 'ID':
            continue
        poly.append(feat.findall('.//Property[@propertytypename="%s"]' % field)[0].text)
    cursor.insertRow(poly)
del cursor
del array
del poly
