=============================================================
import sys
path = 'E:/foley/poseLibrary/1.1.1/source'

if path not in sys.path:
    sys.path.append(path)

from poseLibrary import poseLib
poseLib.PoseLib()
=============================================================

变量设置
1.1.1/source/poseLibrary/PoseLibEnv.py


角色数据文件夹
ROOT_CHARACTER_PATH = 你的路径（默认为 1.1.1\resource\character）
