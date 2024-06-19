import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ListViewExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 创建一个QStandardItemModel
        model = QStandardItemModel()

        # 添加一些列表项
        for i in range(5):
            item = QStandardItem(f"Item {i+1}")
            model.appendRow(item)

        # 创建一个QListView
        self.listView = QListView()
        self.listView.setModel(model)

        # 将QListView添加到布局中
        layout.addWidget(self.listView)

        # 设置窗口的布局
        self.setLayout(layout)

        # 设置窗口的标题和大小
        self.setWindowTitle('QListView with QStandardItemModel')
        self.setGeometry(300, 300, 300, 200)

def main():
    app = QApplication(sys.argv)
    ex = ListViewExample()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()