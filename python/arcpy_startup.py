# -*- coding: UTF-8 -*-
import os
import sys
import re

# Import fmeobjects
try:
    sys.path.append(r'C:\Program Files\FME\fmeobjects\python27')
except:
    print 'no fme'

try:
    import arcpy
    from arcpy.sa import *  # noqa: F403,F401
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
    if os.environ.get('COMPUTERNAME').lower() == '5CD7232N5D80F9':
        arcpy.env.workspace = r'c:\project\work'
        arcpy.env.scratchworkspace = r'c:\project\work\scratch.gdb'
except:
    print 'arcpy not installed'

try:
    # import numpy
    pass
except:
    pass

import subprocess


def gotoXY(s):
    s = re.sub(r'[^\d|^,|^.|^ |^\t]', '', s)  # trim any non number chars
    s = s.strip()  # just plain strip
    s = s.replace(',', '.')  # normalize to dot decimal separator
    s = re.sub(r'(\.\d+)\s+', r'\1\t', s)  # separate the two pairs
    s = s.split('\t')
    s = [re.sub(r'[^\d|^.]', '', c.strip()) for c in s]  # now we have a coordinate pair
    s = [float(c) for c in s]

    df = curFrame()
    newExtent = df.extent
    newExtent.XMin, newExtent.YMin = s[0] - df.extent.width/2, s[1] - df.extent.height/2
    newExtent.XMax, newExtent.YMax = s[0] + df.extent.width/2, s[1] + df.extent.height/2
    df.extent = newExtent

    arcpy.RefreshActiveView()


def fixSde():
    for l in arcpy.mapping.ListLayers(curDoc()):
        if hasattr(l, 'dataSource') and l.dataSource != '' and l.workspacePath[-4:] == '.sde':
            oldStage = l.dataSource.split(u'\\')[1][11:12]
            newStage = int(oldStage) + 1
            if newStage == 7:
                newStage = 1
            newWs = l.workspacePath.replace('sde%s' % str(oldStage), 'sde%s' % str(newStage))
            l.replaceDataSource(
                newWs,
                'SDE_WORKSPACE',
                l.datasetName
            )


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def wcd(newDir):
    # Uses wcd to change directory
    subprocess.call([
        'c:/winbin/wcd/wcdwin64.exe', '-i', '-w', newDir
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
