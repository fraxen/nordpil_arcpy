import os
import arcpy
import pythonaddins

class SetWorkspace(object):
    """Implementation for setworkspace_addin.setworkspace (Extension)"""
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self.enabled = True
    def openDocument(self):
		print "Before:" + arcpy.env.workspace
		mxd = arcpy.mapping.MapDocument('current')
		mxdPath = os.path.dirname(mxd.filePath)
		arcpy.env.workspace = mxdPath
		arcpy.env.scratchWorkspace = mxdPath
		print "Current scratch/workspace set to " + mxdPath
