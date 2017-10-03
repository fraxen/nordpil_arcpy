# -*- coding: UTF-8 -*-
import os
# Import fmeobjects
try:
    sys.path.append(r'C:\Program Files\FME\fmeobjects\python27')
except:
    print 'no fme'

try:
    import arcpy
    from arcpy.sa import *
    arcpy.env.overwriteOutput = True
    try:
        arcpy.CheckOutExtension('Spatial')
    except:
        pass
    arcpy.ImportToolbox(
        os.path.join(
            os.environ.get('USERPROFILE'),
            'aml/python/Nordpil.tbx'
        )
    )
    arcpy.env.workspace = r'c:\data\ws'
    arcpy.env.scratchworkspace = r'f:\temp\scratch.gdb'
except:
    print 'arcpy not installed'

try:
    # import numpy
    pass
except:
    pass

import subprocess


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def wcd(newDir):
    # Uses wcd to change directory
    subprocess.call([
        'c:/winbin/wcd/wcdwin32.exe', '-i', '-w', newDir
    ])
    thisDir = ''
    with open(os.path.join(os.environ['WCDHOME'], 'wcdgo.bat'), 'r') as wcdFile:
        try:
            thisDir = [x for x in wcdFile.readlines() if x[0:3] == 'cd '][0].split('"')[1]
            os.chdir(thisDir)
        except:
            return False


def gPing(msg, isArc=0):
    try:
        if (isArc == 1):
            subprocess.call([
                'cmd.exe', '/c', 'start', 'growlnotify.exe', '/p:2',
                '/t:"ArcPy processing on ' + os.environ.get('COMPUTERNAME') + '"',
                r'/ai:"%s\bin\icon_arcgis.png"' % os.environ['HOME'], msg
            ])
        else:
            subprocess.call([
                'cmd.exe', '/c', 'start', 'growlnotify.exe', '/p:2',
                '/t:"Python processing on ' + os.environ.get('COMPUTERNAME') + '"',
                r'/ai:"%s\bin\icon_python.png"' % os.environ['HOME'], msg
            ])
    except RuntimeError:
        print RuntimeError
        print('[UNABLE TO LAUNCH GROWLNOTIFY]\n\n' + msg)


def curExtent():
    return arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))[0].extent


def curDoc():
    return arcpy.mapping.MapDocument("CURRENT")


def isArcMap():
    try:
        arcpy.mapping.MapDocument("CURRENT")
        return True
    except:
        return False


def curFrame():
    return arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))[0]


def curProjection():
    return arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))[0].spatialReference.exportToString()


def ExtentToFeatureclass(fcName):
    pointArray = arcpy.Array()
    node = arcpy.Point()

    node.X = curExtent().XMin
    node.Y = curExtent().YMax
    pointArray.add(node)
    node.X = curExtent().XMax
    node.Y = curExtent().YMax
    pointArray.add(node)
    node.X = curExtent().XMax
    node.Y = curExtent().YMin
    pointArray.add(node)
    node.X = curExtent().XMin
    node.Y = curExtent().YMin
    pointArray.add(node)
    node.X = curExtent().XMin
    node.Y = curExtent().YMax
    pointArray.add(node)

    box = arcpy.Polyline(pointArray, curProjection())
    arcpy.CopyFeatures_management(box, fcName)

    return 'Prepared extent to fc: ' + fcName

try:
    import pyreadline.rlmain
    pyreadline.rlmain.config_path = r"~\pyreadlineconfig.ini"
    import readline
    import atexit
    import pyreadline.unicode_helper
    # Normally the codepage for pyreadline is set to be sys.stdout.encoding
    # if you need to change this uncomment the following line
    # pyreadline.unicode_helper.pyreadline_codepage="utf8"
except ImportError:
    print "Module readline not available."
else:
    # import tab completion functionality
    import rlcompleter
    # activate tab completion
    readline.parse_and_bind("tab: complete")
    readline.read_history_file()
    atexit.register(readline.write_history_file)
    del readline, rlcompleter, atexit

# VIM: let g:flake8_ignore=g:flake8_ignore . ",F401"
