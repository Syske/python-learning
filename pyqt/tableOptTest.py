import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem

class Example(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        # 创建一个QTableWidget实例
        self.table = QTableWidget(5, 2)  # 5行2列
        
        # 设置表头标签
        self.table.setHorizontalHeaderLabels(['Name', 'Action'])
        
        # 填充数据和添加按钮
        for i in range(5):
            name_item = QTableWidgetItem(f'Item {i}')
            self.table.setItem(i, 0, name_item)
            
            # 创建一个按钮并设置文本
            button = QPushButton('Click me')
            button.clicked.connect(lambda checked, row=i: self.onButtonClick(row))  # 使用lambda函数捕获行索引
            
            # 将按钮添加到表格的最后一列
            self.table.setCellWidget(i, 1, button)
        
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Table with Buttons')
        self.show()
    
    # 按钮点击槽函数
    def onButtonClick(self, row):
        print(f"Button clicked for row {row}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())