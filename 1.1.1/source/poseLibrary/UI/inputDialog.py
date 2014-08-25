#========================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Mon, 25 Aug 2014 16:49:35
#========================================
import os
from utils import scriptTool, uiTool
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#======================================================
SCRIPT_PATH = scriptTool.getScriptPath()
#======================================================

baseClass, windowClass = uiTool.loadUi(os.path.join(SCRIPT_PATH, 'inputDialog.ui'))
class InputDialog(baseClass, windowClass):

    def __init__(self, path, parent=uiTool.getMayaWindow()):
        super(InputDialog, self).__init__(parent)
        self.setupUi(self)
        self.path = path
    
    
    def on_btn_OK_clicked(self, click=None):
        if click == None:return
        os.chdir(self.path)
        name = str(self.lineEdit.text())
        
        if os.path.isdir(name):
            uiTool.warning('" %s " was exists, please use other name ! !'%name, 'e')
            return
        
        os.mkdir(name)
        self.accept()