'''
explort and import animation data 

Author : Jiangjishi

#�Ȳ�ѯ��ǰ�����ڵ���K�����룬�����β�ѯ [����������:[Time��value]]
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
while i<lx_objNum: #����������
    #lx_keys =cmds.keyframe(lx_objects[i],query=1,keyframeCount =1)
    lx_aniNodes =cmds.keyframe(lx_objects[i],query=1,name=1)  #������������Щ�����ڵ�
       
    aa = len(lx_aniNodes)
    
    #print lx_objects[i]
    j=0
    while j<aa: #�����ڵ�����
        #print lx_aniNodes[j]
        lx_vc =cmds.keyframe(lx_aniNodes[j],query =1,valueChange=1) #��ѯ�����ڵ��ϵĹؼ�֡����ֵ
        lx_tc =cmds.keyframe(lx_aniNodes[j],query =1,timeChange=1) #��ѯ�����ڵ��ϵĹؼ�֡��ֵ֡
        bb = len(lx_vc)
        k=0
        #print len(lx_allanimationDataDic)
        while k<bb: #�ؼ�֡
            #print lx_tc[k]
            temp={}
            temp[lx_tc[k]] = lx_vc[k]
            lx_allanimationDataDic[lx_aniNodes[j]+str(lx_tc[k])] =  temp  
            
            k=k +1
            
        j=j+1
            
    i= i +1
    
json.dump(lx_allanimationDataDic, lx_file)
lx_file.close()