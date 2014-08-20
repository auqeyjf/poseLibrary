'''
explort and import animation data 

Author : Jiangjishi

#先查询当前动画节点有K多少针，再依次查询 [控制器名称:[Time：value]]
    def lx_importAniData():
'''
import maya.cmds as cmds
import sys,json

lx_allanimationDataDic = {}
lx_objects =[]
lx_objects = cmds.ls(selection=1,)
lx_objNum = len(lx_objects)
lx_file = open('D:/testForAni.json','w')

i=0
while i<lx_objNum: #控制器名称
    #lx_keys =cmds.keyframe(lx_objects[i],query=1,keyframeCount =1)
    lx_aniNodes =cmds.keyframe(lx_objects[i],query=1,name=1)  #控制器上有哪些动画节点
       
    aa = len(lx_aniNodes)
    
    #print lx_objects[i]
    j=0
    while j<aa: #动画节点名称
        #print lx_aniNodes[j]
        lx_vc =cmds.keyframe(lx_aniNodes[j],query =1,valueChange=1) #查询动画节点上的关键帧的数值
        lx_tc =cmds.keyframe(lx_aniNodes[j],query =1,timeChange=1) #查询动画节点上的关键帧的帧值
        bb = len(lx_vc)
        k=0
        #print len(lx_allanimationDataDic)
        while k<bb: #关键帧
            #print lx_tc[k]
            temp={}
            temp[lx_tc[k]] = lx_vc[k]
            lx_allanimationDataDic[lx_aniNodes[j]+str(lx_tc[k])] =  temp  
            
            k=k +1
            
        j=j+1
            
    i= i +1
    
json.dump(lx_allanimationDataDic, lx_file)
lx_file.close()