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


i=j=k=0
while i<lx_objNum: #����������
    #lx_keys =cmds.keyframe(lx_objects[i],query=1,keyframeCount =1)
    lx_aniNodes =cmds.keyframe(lx_objects[i],query=1,name=1)  #������������Щ�����ڵ�
    lx_vc =cmds.keyframe(lx_aniNodes[i],query =1,valueChange=1) #��ѯ�����ڵ��ϵĹؼ�֡����ֵ
    lx_tc =cmds.keyframe(lx_aniNodes[i],query =1,timeChange=1) #��ѯ�����ڵ��ϵĹؼ�֡��ֵ֡   
    aa = len(lx_aniNodes)
    bb = len(lx_vc)
    while j<aa: #�����ڵ�����
        
        while k<bb: #�ؼ�֡
            
            temp={}
            temp[lx_tc[j]] = lx_vc[k]
            lx_allanimationDataDic[lx_aniNodes[j]] =  temp  
            k=k +1
            
        j=j+1
            
    i= i +1
    
json.dump(lx_allanimationDataDic, lx_file)
lx_file.close()