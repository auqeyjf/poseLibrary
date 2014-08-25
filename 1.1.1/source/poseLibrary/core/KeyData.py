#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 25 Aug 2014 09:24:18
#========================================
import os.path, json
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def getKeyByObject(obj):
    data = dict()
    
    #- object exists ?
    if not mc.objExists(obj):
        return data
    data['object'] = obj
    
    #- object has attributes ?
    attributes = mc.listAttr(obj, k=True)
    if not attributes:
        return data
    
    #- get keys
    for attr in attributes:
        times     = mc.keyframe(obj,   at=attr, q=True,  tc=True)
        values    = mc.keyframe(obj,   at=attr, q=True,  vc=True)
        inAngles  = mc.keyTangent(obj, at=attr, q=True,  ia=True)
        outAngles = mc.keyTangent(obj, at=attr, q=True,  oa=True)
        
        #- keys not found..
        if not times:
            continue
        
        #- save data..
        data.setdefault('keyData', {})[attr] = zip(times, values, inAngles, outAngles)
    
    return data



def setKeyByData(data):
    #- data format not right..
    if not isinstance(data, dict):
        return
    
    #- data is empty..
    if len(data) == 0:
        return
    
    #- object not exists..
    obj = data.get('object', '*')
    if not mc.objExists(obj):
        return
    
    #- reading data..
    for attr, keydata in data.get('keyData', dict()).iteritems():
        #- testing attribute..
        
        #- key it
        for tm, va, ia, oa in keydata:
            #- set key
            mc.setKeyframe(obj, at=attr, t=tm, v=va)
            #- fix curve
            mc.keyTangent('%s.%s'%(obj, attr), l=False)
            mc.keyTangent(obj, e=True, at=attr, a=True, t=(tm, tm), ia=ia, oa=oa)
            mc.keyTangent('%s.%s'%(obj, attr), l=True)




def getKeyByObjects(objects):
    data = list()
    #-
    if not isinstance(objects, (list, tuple)):
        return data
    
    for obj in objects:
        data.append(getKeyByObject(obj))
    
    return data





def setKeyByDatas(datas):
    if not isinstance(datas, (list, tuple)):
        return
    
    for data in datas:
        setKeyByData(data)





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