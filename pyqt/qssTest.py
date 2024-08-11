import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox,QLineEdit, QRadioButton, QGroupBox, QLabel, QPushButton, QButtonGroup, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt

class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()
           

class TestWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    

    def initUI(self):
        
        # 创建垂直布局
        main_layout = QVBoxLayout()
        self.label = QLabel('企业ID:')

        h_layout0 = QHBoxLayout()
        h_layout0.addWidget(self.label)
         # 创建数字输入框
        self.lineEdit = QLineEdit(self)
        h_layout0.addWidget(self.lineEdit)
        main_layout.addLayout(h_layout0)

        # 设置窗口的布局
        self.setLayout(main_layout)

        # 设置窗口标题和位置
        self.setWindowTitle('测试widget')
        self.setGeometry(300, 400, 200, 150)
   
if __name__ == "__main__":          
    app = QApplication(sys.argv)
    window = TestWidget()

    style_file = './qss/style.qss'
    style_sheet = QSSLoader.read_qss_file(style_file)
    window.setStyleSheet(style_sheet)

    window.show()
    sys.exit(app.exec_())