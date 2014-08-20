#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Fri, 15 Aug 2014 09:59:45
#========================================
import re, math, os.path, poseLibrary.PoseLibEnv
from utils import scriptTool, uiTool
from PyQt4 import QtCore, QtGui
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
SCRIPT_PATH = scriptTool.getScriptPath()


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(ListModel, self).__init__(parent)
        self.__data = []
    
    
    def rowCount(self, index):
        return len(self.__data)
    


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__data[index.row()]


    def changeData(self, L):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, len(self.__data))
        self.__data = L
        self.endRemoveRows()    


    def getData(self, index):
        return self.data(index, QtCore.Qt.DisplayRole)
    

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self.__data = []
    
    def columnCount(self, index=QtCore.QModelIndex()):
        return 3
    
    
    def rowCount(self, index=QtCore.QModelIndex()):
        return int(math.ceil(len(self.__data) / float(self.columnCount())))
    
    
    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            i = index.row() * self.columnCount() + index.column()
            if i < len(self.__data):
                return self.__data[i]
            else:
                return None
    
    
    
    def clear(self):
        for i in reversed(range(self.rowCount())):
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self.__data[i * self.columnCount():]
            self.endRemoveRows()



    def updateData(self, L):
        for i, data in enumerate(L):
            if i % self.columnCount() == 0:
                self.beginInsertRows(QtCore.QModelIndex(), i, i)
            
            self.__data.append(data)
            
            if i % self.columnCount() == 0:
                self.endInsertRows() 



class PoseDelegate(QtGui.QItemDelegate):
    
    def __init__(self, model=None, parent=None):
        super(PoseDelegate, self).__init__(parent)
        self.parentModel = model
        
    
    def createEditor(self, parent, option, index):
        self.delegate = QtGui.QLabel(parent)
        imagePath = self.getImagePath(index)
        self.delegate.setStyleSheet('image: url(%s);'%imagePath)
        return self.delegate


    def getImagePath(self, index):
        imagePath = os.path.join(SCRIPT_PATH, 'icons', 'file_image.png').replace('\\', '/')
        data =  self.parentModel.data(index, QtCore.Qt.EditRole)
        if not os.path.isfile(data):
            return imagePath
        
        image = os.path.splitext(data)[0] + '.png'
        if not os.path.isfile(image):
            return imagePath
        
        image = image.replace('\\', '/')
        return image




baseClass, windowClass = uiTool.loadUi(os.path.join(scriptTool.getScriptPath(), 'poseLibrary.ui'))
class PoseLib(baseClass, windowClass):
    
    def __init__(self, parent=uiTool.getMayaWindow()):
        super(PoseLib, self).__init__(parent)
        self.setupUi(self)
        #--
        self.__model_character = ListModel()
        self.__model_poseType  = ListModel()
        self.__model_pose      = TableModel()
        
        self.LSV_Character.setModel(self.__model_character)
        self.LSV_PoseType.setModel(self.__model_poseType)
        self.LSV_Pose.setModel(self.__model_pose)
        #--        
        self.LSV_Pose.verticalHeader().setVisible(False)
        self.LSV_Pose.horizontalHeader().setVisible(False)
        
        self.LSV_Pose.setColumnWidth(0, 134)
        self.LSV_Pose.setColumnWidth(1, 134)
        self.LSV_Pose.setColumnWidth(2, 133)
        
        self.LSV_Pose.setItemDelegate(PoseDelegate(self.__model_pose))
        #--   
        self.show()
    

    def on_btn_refreshCharacters_clicked(self, args=None):
        if args == None:return
        charcters = []
        for d in os.listdir(poseLibrary.PoseLibEnv.ROOT_CHARACTER_PATH):
            if not os.path.isdir(os.path.join(poseLibrary.PoseLibEnv.ROOT_CHARACTER_PATH, d)):
                continue
            charcters.append(d)
        self.__model_character.changeData(charcters)
        self.__model_pose.clear()



    def on_LSV_Character_clicked(self):
        if self.LSV_Character.selectedIndexes() == []:
            return
        path = os.path.join(poseLibrary.PoseLibEnv.ROOT_CHARACTER_PATH, self.__model_character.getData(self.LSV_Character.selectedIndexes()[0]))
        poseTypes = []
        for d in os.listdir(path):
            if not os.path.isdir(os.path.join(path, d)):
                continue
            poseTypes.append(d)
        self.__model_poseType.changeData(poseTypes)
        self.__model_pose.clear()


    def on_LSV_PoseType_clicked(self):
        if self.LSV_PoseType.selectedIndexes() == []:
            return
        character = self.__model_character.getData(self.LSV_Character.selectedIndexes()[0])
        poseType = self.__model_poseType.getData(self.LSV_PoseType.selectedIndexes()[0])
        posePath = os.path.join(poseLibrary.PoseLibEnv.ROOT_CHARACTER_PATH, character, poseType)
        
        poseFiles = [os.path.join(posePath, f) for f in os.listdir(posePath)]
        poseFiles = [f for f in poseFiles if re.search('json$', f)]
        
        self.__model_pose.clear()
        self.__model_pose.updateData(poseFiles)
        #- set row height
        for i in range(self.__model_pose.rowCount()):
            self.LSV_Pose.setRowHeight(i, 134)
        
        for row in range(self.__model_pose.rowCount()):
            for column in range(self.__model_pose.columnCount()):
                index = self.__model_pose.index(row, column)
                data  = self.__model_pose.data(index, QtCore.Qt.EditRole)
                if data == None:
                    continue
                self.LSV_Pose.openPersistentEditor(index)
        
        
        