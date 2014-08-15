import sys
path = 'E:/foley/poseLibrary/1.1.1/source'

if path not in sys.path:
    sys.path.append(path)


from poseLibrary.UI import poseLibrary
poseLibrary.PoseLib()
