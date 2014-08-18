#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Fri, 15 Aug 2014 09:59:45
#========================================
import os.path, math
from FoleyUtils import scriptTool, uiTool
from PyQt4 import QtCore, QtGui
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class ListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(ListModel, self).__init__(parent)
        self.__data = ['TempCharacterA', 'TempCharacterB']
    
    
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
        self.__data = [1,2,3,4,5,6,7,8,9, 10, 11, 121, 13]
    
    def columnCount(self, index=QtCore.QModelIndex()):
        return 3
    
    
    def rowCount(self, index=QtCore.QModelIndex()):
        return int(math.ceil(len(self.__data) / float(self.columnCount())))
    
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
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
        #--   
        self.show()
    

    def __refeshPose(self):
        if self.LSV_Character.selectedIndexes() == []:
            return
        if self.LSV_PoseType.selectedIndexes() == []:
            return
        
        #character = self.__model_character.getData(self.LSV_Character.selectedIndexes()[0])
        #poseType  = self.__model_poseType.getData(self.LSV_PoseType.selectedIndexes()[0])
        
        #- refresh data
        self.__model_pose.clear()
        self.__model_pose.updateData(range(100))
        
        #- set row height
        for i in range(self.__model_pose.rowCount()):
            self.LSV_Pose.setRowHeight(i, 134)
        
        
    def on_LSV_Character_clicked(self):
        self.__refeshPose()


    def on_LSV_PoseType_clicked(self):
        self.__refeshPose()