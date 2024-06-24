import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
 
class LoginWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
    def initUi(self):
        #初始化窗口部件
        usrLbl = QLabel()
        usrEdit = QLineEdit()
        pwdLbl = QLabel()
        pwdEdit = QLineEdit()
        confirmBtn = QPushButton()
        cancelBtn = QPushButton()
        usrLbl.setText('用户名')
        pwdLbl.setText('密码')
        confirmBtn.setText('确定')
        cancelBtn.setText('取消')
        hrLayot1 = QHBoxLayout()
        hrLayot2 = QHBoxLayout()
        hrLayot3 = QHBoxLayout()
        hrLayot1.addWidget(usrLbl)
        hrLayot1.addWidget(usrEdit)
        hrLayot2.addWidget(pwdLbl)
        hrLayot2.addWidget(pwdEdit)
        hrLayot3.addWidget(confirmBtn)
        hrLayot3.addWidget(cancelBtn)
        vrLayout = QVBoxLayout()
        vrLayout.addLayout(hrLayot1)
        vrLayout.addLayout(hrLayot2)
        vrLayout.addLayout(hrLayot3)
        self.setLayout(vrLayout)
        self.setWindowTitle("登录窗口")
 
        #信号槽连接
        confirmBtn.clicked.connect(self.confirmBtnClicked)
        cancelBtn.clicked.connect(self.cancelBtnClicked)
 
    def confirmBtnClicked(self):
        print('您点击了确定按钮')
 
    def cancelBtnClicked(self):
        print('您点击了取消按钮')
        self.close()
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginWgt = LoginWidget()
    loginWgt.show()
    sys.exit(app.exec_())