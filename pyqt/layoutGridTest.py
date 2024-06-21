import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox,QLineEdit, QRadioButton, QGroupBox, QLabel, QPushButton, QButtonGroup, QTextEdit, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt

class TestWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    

    def initUI(self):
        # 格栅布局
        grid_layout = QGridLayout()
        names = ['格子1', '格子2', '格子3', '格子4', '格子5', '格子6', '格子7', '格子8', '格子9']
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                button = QPushButton(names[index])  # 也可以使用QLabel显示图片
                button.setFixedWidth(100)
                button.setFixedHeight(100)
                grid_layout.addWidget(button, i, j)

        # 设置窗口的布局
        self.setLayout(grid_layout)

        # 设置窗口标题和位置
        self.setWindowTitle('测试格栅布局')
        self.setGeometry(300, 400, 400, 400)
        
if __name__ == "__main__":

    # 创建应用
    app = QApplication(sys.argv)

    # 创建窗口
    widget = TestWidget()

    # 显示窗口
    widget.show()

    # 运行应用
    sys.exit(app.exec_())