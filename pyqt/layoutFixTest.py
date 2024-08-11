import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox,QLineEdit, QRadioButton, QGroupBox, QLabel, QPushButton, QButtonGroup, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt

class TestWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    

    def initUI(self):
        
        # 创建垂直布局
        main_layout = QVBoxLayout()
        
        # 创建布局用于放置单选框
        radio_layout = QHBoxLayout()
        # 创建单选框
        radio1 = QRadioButton('radio1')
        radio2 = QRadioButton('radio2')

        # 设置单选框的互斥性（即一次只能选择一个）
        radio1.setChecked(True)  # 默认选中选项1

        # 将单选框添加到布局中
        radio_layout.addWidget(radio1)
        radio_layout.addWidget(radio2)
        
        # 垂直布局
        input_layout = QVBoxLayout()
        label = QLabel('ID:')
        input_layout.addWidget(label)
         # 创建数字输入框
        lineEdit = QLineEdit(self)
        input_layout.addWidget(lineEdit)
        
        main_layout.addLayout(input_layout)
        main_layout.addLayout(radio_layout)

        # 设置窗口的布局
        self.setLayout(main_layout)

        # 设置窗口标题和位置
        self.setWindowTitle('测试嵌套布局')
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