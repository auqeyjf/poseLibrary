#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 25 Aug 2014 09:24:18
#========================================
import os.path, json, re
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def getObjectReferencedName(namespace, obj):
    objects = ' '.join(mc.ls())
    res = re.search('%s\S+%s'%(namespace, obj), objects)
    if res:
        return res.group()
    return obj


def getKeyByObject(obj):
    data = dict()
    
    #- object exists ?
    if not mc.objExists(obj):
        return data
    data['object'] = re.search('\w+$', obj).group()
    
    #- object has attributes ?
    attributes = mc.listAttr(obj, k=True)
    if not attributes:
        return data
    
    #- get keys
    for attr in attributes:
        times      = mc.keyframe(obj,   at=attr, q=True,  tc=True)
        values     = mc.keyframe(obj,   at=attr, q=True,  vc=True)
        inAngles   = mc.keyTangent(obj, at=attr, q=True,  ia=True)
        outAngles  = mc.keyTangent(obj, at=attr, q=True,  oa=True)
        inWeights  = mc.keyTangent(obj, at=attr, q=True,  iw=True)
        outWeights = mc.keyTangent(obj, at=attr, q=True,  ow=True)
        #- keys not found..
        if not times:
            continue
        
        #- save data..
        data.setdefault('keyData', {})[attr] = zip(times, values, inAngles, inWeights, outAngles, outWeights)
    
    return data



def setKeyByData(namespace, data):
    #- data format not right..
    if not isinstance(data, dict):
        return
    
    #- data is empty..
    if len(data) == 0:
        return
    
    #- object not exists..
    obj = getObjectReferencedName(namespace, data.get('object', '"'))
    if not mc.objExists(obj):
        return
    
    #- reading data..
    for attr, keydata in data.get('keyData', dict()).iteritems():
        #- testing attribute..
        
        #- key it
        for tm_V, va_V, ia_V, iw_V, oa_V, ow_V in keydata:
            #- set key
            mc.setKeyframe(obj, at=attr, t=tm_V, v=va_V)
            #- fix curve
            mc.keyTangent('%s.%s'%(obj, attr), l=False)
            mc.keyTangent(obj, e=True, at=attr, a=True, t=(tm_V, tm_V), ia=ia_V, iw=iw_V, oa=oa_V, ow=ow_V)
            mc.keyTangent('%s.%s'%(obj, attr), l=True)




def getKeyByObjects(objects):
    data = list()
    #-
    if not isinstance(objects, (list, tuple)):
        return data
    
    for obj in objects:
        data.append(getKeyByObject(obj))
    
    return data





def setKeyByDatas(namespace, datas):
    if not isinstance(datas, (list, tuple)):
        return
    
    for data in datas:
        setKeyByData(namespace, data)





def writeData(data, filePath):
    f = open(filePath, 'w')
    json.dump(data, f, indent=4)
    f.close()
    



def readData(filePath):
    data = list()
    if not os.path.isfile(filePath):
        return data
    
    f = open(filePath, 'r')
    data = json.load(f)
    f.close()
    
    return data



def exportKeysBySelect(filePath):
    sel = mc.ls(sl=True)
    if len(sel) == 0:
        return
    
    data = getKeyByObjects(sel)
    writeData(data, filePath)
    print 'Data exported to : %s'%filePath