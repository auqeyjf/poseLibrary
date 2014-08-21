import maya.cmds as cmds
import json

lx_allanimationDataDic = {}
lx_objects =[]
lx_objects = cmds.ls(selection=1,)
lx_objNum = len(lx_objects)

lx_allImportDataDic={}
lx_allImportDataDic = json.loads(open('D:/testForAni.json').read())