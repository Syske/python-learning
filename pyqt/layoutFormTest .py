import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox,QLineEdit, QRadioButton, QGroupBox, QLabel, QPushButton, QButtonGroup, QTextEdit, QFormLayout
from PyQt5.QtCore import Qt

class TestWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    

    def initUI(self):
        
        # 创建垂直布局
        main_layout = QFormLayout()
        
        lineEdit = QLineEdit(self)
        label = QLabel('account:')
        main_layout.addRow(label, lineEdit)
        
        lineEdit1 = QLineEdit(self)
        label1 = QLabel('passwd:')
        main_layout.addRow(label1, lineEdit1)

        # 设置窗口的布局
        self.setLayout(main_layout)

        # 设置窗口标题和位置
        self.setWindowTitle('测试表单布局')
        self.setGeometry(300, 400, 200, 150)
        
if __name__ == "__main__":

    # 创建应用
    app = QApplication(sys.argv)

    # 创建窗口
    widget = TestWidget()

    # 显示窗口
    widget.show()

    # 运行应用
    sys.exit(app.exec_())