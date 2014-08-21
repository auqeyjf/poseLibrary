#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Fri, 15 Aug 2014 09:59:45
#========================================
import re, os.path, poseLibrary.PoseLibEnv
from utils import scriptTool, uiTool
from PyQt4 import QtCore, QtGui
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#======================================================

SCRIPT_PATH = scriptTool.getScriptPath()

#======================================================

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
        return len(self.__data)
    
    
    
    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            return self.__data[index.row()][index.column()]
    
    
    def flags(self, index):
        if self.__data[index.row()][index.column()] != None:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsSelectable
    

    def clear(self):
        for i in reversed(range(self.rowCount())):
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            self.__data.pop(i)
            self.endRemoveRows()



    def updateData(self, L):
        for i in range(0, len(L), 3):
            #- [[1, 2, 3], [4, 5, 6], [7, None, None]]
            x = []
            for s in range(3):
                index = i + s
                if index < len(L):
                    x.append(L[index])
                else:
                    x.append(None)
            #- insert
            self.beginInsertRows(QtCore.QModelIndex(), i / 3, i / 3)
            self.__data.append(x)
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
        for imgExt in ('.png', '.jpg', '.jpeg', '.bmp'):
            image = os.path.splitext(data)[0] + imgExt
            if os.path.isfile(image):
                image = image.replace('\\', '/')
                return image
        
        return imagePath




baseClass, windowClass = uiTool.loadUi(os.path.join(SCRIPT_PATH, 'poseLibrary.ui'))
class PoseLib(baseClass, windowClass):
    
    ROOT_PATH = poseLibrary.PoseLibEnv.ROOT_CHARACTER_PATH
    CHARACTER = None
    POSE_TYPE = None
    
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
        os.chdir(self.ROOT_PATH)
        #-
        charcters = [d for d in os.listdir(self.ROOT_PATH) if os.path.isdir(d)]
        #-
        self.__model_character.changeData(charcters)
        self.__model_pose.clear()



    def on_LSV_Character_clicked(self):
        selectedChara = self.LSV_Character.selectedIndexes()
        if selectedChara == []:
            return
        self.CHARACTER =  self.__model_character.getData(selectedChara[0])
        #-
        path = os.path.join(self.ROOT_PATH, self.CHARACTER)
        os.chdir(path)
        poseTypes = [d for d in os.listdir(path) if os.path.isdir(d)]
        #-
        self.__model_poseType.changeData(poseTypes)
        self.__model_pose.clear()



    def on_LSV_PoseType_clicked(self):
        selectedPosetype = self.LSV_PoseType.selectedIndexes()
        if selectedPosetype == []:
            return
        self.POSE_TYPE = self.__model_poseType.getData(selectedPosetype[0])
        
        #-
        posePath = os.path.join(self.ROOT_PATH, self.CHARACTER, self.POSE_TYPE)
        #-
        os.chdir(posePath)
        poseFiles = [f for f in os.listdir(posePath) if re.search('json$', f)]
        #-
        self.__model_pose.clear()
        self.__model_pose.updateData(poseFiles)
        
        #- set row height
        for i in range(self.__model_pose.rowCount()):
            self.LSV_Pose.setRowHeight(i, 134)
        
        for row in range(self.__model_pose.rowCount()):
            for column in range(3):
                index = self.__model_pose.index(row, column)
                data  = self.__model_pose.data(index, QtCore.Qt.EditRole)
                if data == None:
                    continue
                self.LSV_Pose.openPersistentEditor(index)
        
    #=================================================================================    
    #                                  Tool  Bar                                     #
    #=================================================================================    
    def on_btn_playBlast_clicked(self, args=None):
        if args == None:return
        print 1
                
    def on_btn_apply_clicked(self, args=None):
        if args == None:return
        print 2
    
                
    def on_btn_create_clicked(self, args=None):
        if args == None:return
        Menu = QtGui.QMenu()
        Menu.move(QtGui.QCursor.pos())
        Menu.addAction('Add New Character...')
        Menu.addSeparator()
        Menu.addAction('Add New Pose Type...')
        Menu.addSeparator()
        Menu.addAction('Add New Pose...')
        Menu.exec_()


    def on_btn_grabImage_clicked(self, args=None):
        if args == None:return
        print 4
                
    def on_btn_addStar_clicked(self, args=None):
        if args == None:return
        print 5
                
    def on_btn_delete_clicked(self, args=None):
        if args == None:return
        print 6  