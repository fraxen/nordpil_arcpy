# -*- coding: UTF-8 -*-
import os
import sys
import re
import subprocess

# Import fmeobjects
if os.path.exists(r'C:\Program Files\FME\fmeobjects\python27'):
    sys.path.append(r'C:\Program Files\FME\fmeobjects\python27')

try:
    import arc_utils
except Exception:
    pass

try:
    import arcpy
    from arcpy.sa import *  # noqa: F403,F401
    arcpy.env.overwriteOutput = True
    try:
        arcpy.CheckOutExtension('Spatial')
    except Exception:
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
except Exception:
    print 'arcpy not installed'



def curCenter():
    e = curExtent()
    print 'N = %s  -- E = %s' % (int(e.YMin + e.height / 2), int(e.XMin + e.width / 2))


def gotoXY(s):
    if type(s) is list and len(s) == 2:
        if not(type(s) is float):
            s = [float(c) for c in s]
    else:
        s = re.sub(r'[^\d|^,|^.|^ |^\t]', '', s)  # trim any non number chars
        if re.search('\t', s):
            s = s.split('\t')
        elif re.subn(',', '', s)[1] == 1:
            s = s.split(',')
        else:
            s = s.split(' ')
        s = [c.strip() for c in s]  # just plain strip
        s = [c.replace(',', '.') for c in s]  # normalize to dot decimal separator
        s = [c.replace(' ', '') for c in s]  # remove spaces
        s = [float(c) for c in s]

    print s
    df = curFrame()
    newExtent = df.extent
    newExtent.XMin, newExtent.YMin = s[0] - df.extent.width / 2, s[1] - df.extent.height / 2
    newExtent.XMax, newExtent.YMax = s[0] + df.extent.width / 2, s[1] + df.extent.height / 2
    df.extent = newExtent

    arcpy.RefreshActiveView()


def updateNames():
    for l in arcpy.mapping.ListLayers(curDoc()):
        if hasattr(l, 'dataSource') and l.dataSource != '' and l.workspacePath[-4:] == '.sde':
            stage = [f for f in l.dataSource.split('\\') if f.lower().find('stage') > -1][0].split('@')[0].lower()
            if l.name.lower().find(l.datasetName.split('.')[0].lower()) == -1:
                l.name = '{} {}'.format(l.datasetName.split('.')[0].upper(), l.name)
            if l.name.lower().find(stage) == -1:
                l.name = '{} {}'.format(stage, l.name)
    arcpy.RefreshTOC()


def switchSDE(toStage):
    if toStage == 'ow':
        toStage = 'owstage'
    elif toStage == 'dl':
        toStage = 'dlstage'

    for l in arcpy.mapping.ListLayers(curDoc()):
        if hasattr(l, 'dataSource') and l.dataSource != '' and l.workspacePath[-4:] == '.sde':
            try:
                if toStage is None:
                    if l.workspacePath.find('owstage') != -1:
                        newWs = l.workspacePath.replace('owstage', 'dlstage')
                    else:
                        newWs = l.workspacePath.replace('dlstage', 'owstage')
                else:
                    newWs = l.workspacePath.replace('owstage', toStage)
                    newWs = newWs.replace('dlstage', toStage)
                print('Updating %s to %s' % (l.name, newWs))
                l.replaceDataSource(
                    newWs,
                    'SDE_WORKSPACE',
                    l.datasetName
                )
                if re.search('\w\wstage', l.name, re.IGNORECASE):
                    l.name = re.sub('\w\wstage', toStage, l.name, flags=re.IGNORECASE)
                else:
                    l.name = toStage + ' ' + l.name
            except Exception:
                print('FAILED UPDATING %s to %s' % (l.name, newWs))
                print Exception
                print sys.exc_info()


def fixSde():
    for l in arcpy.mapping.ListLayers(curDoc()):
        if hasattr(l, 'dataSource') and l.dataSource != '' and l.workspacePath[-4:] == '.sde':
            oldStage = l.dataSource.split(u'\\')[1][11:12]
            newStage = int(oldStage) + 1
            if newStage == 7:
                newStage = 1
            newWs = l.workspacePath.replace('sde%s' % str(oldStage), 'sde%s' % str(newStage))
            print('Updating %s to %s' % (l.name, newWs))
            l.replaceDataSource(
                newWs,
                'SDE_WORKSPACE',
                l.datasetName
            )
    arcpy.RefreshTOC()


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
        except Exception:
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
            if 'fmeobjects' in sys.modules or 'fme' in sys.modules:
                subprocess.call([
                    'cmd.exe', '/c', 'start', 'growlnotify.exe', '/p:2',
                    '/t:"FME processing on ' + os.environ.get('COMPUTERNAME') + '"',
                    r'/ai:"%s\bin\icon_fme.png"' % os.environ['HOME'], msg
                ])
            else:
                subprocess.call([
                    'cmd.exe', '/c', 'start', 'growlnotify.exe', '/p:2',
                    '/t:"Python processing on ' + os.environ.get('COMPUTERNAME') + '"',
                    r'/ai:"%s\bin\icon_python.png"' % os.environ['HOME'], msg
                ])
    except RuntimeError:
        subprocess.call([
            'msg.exe', os.environ['USERNAME'], msg
        ])


def curExtent():
    return arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))[0].extent


def curDoc():
    return arcpy.mapping.MapDocument("CURRENT")


def isArcMap():
    try:
        arcpy.mapping.MapDocument("CURRENT")
        return True
    except Exception:
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
