import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('简单窗口')
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        # 创建垂直布局
        main_layout = QHBoxLayout()
        label = QLabel('企业ID:')
#        label.setFixedHeight(40)
#        label.setFixedWidth(40)

        h_layout0 = QHBoxLayout()
        main_layout.addWidget(label)
         # 创建数字输入框
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedHeight(40)
        main_layout.addWidget(self.lineEdit)
        main_layout.addLayout(h_layout0)
        # 设置窗口的布局
        self.centralWidget.setLayout(main_layout)
        self.setGeometry(300, 400, 300, 350)
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())