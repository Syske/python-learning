import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QEvent

class NewWindow(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.initUI()

    def initUI(self):
        # 在这里添加新窗口的UI代码，例如显示数据等
        layout = QVBoxLayout()
        # 假设我们有一个按钮用于演示
        button = QPushButton('这是新窗口的按钮')
        layout.addWidget(button)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('主窗口')
        self.new_windows = []  # 跟踪新窗口的列表
        self.initUI()

    def initUI(self):
        # 创建一个表格来显示多列数据
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)  # 假设有3列数据
        self.tableWidget.setHorizontalHeaderLabels(['列1', '列2', '列3'])
        self.tableWidget.setRowCount(5)  # 假设有5行数据

        # 填充一些示例数据
        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem(f'数据 {i+1},{j+1}')
                self.tableWidget.setItem(i, j, item)

        # 添加一个按钮来打开新窗口
        openButton = QPushButton('打开新窗口')
        openButton.clicked.connect(self.openNewWindow)

        # 设置布局
        centralWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(openButton)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def openNewWindow(self):
        # 根据表格数据或其他逻辑创建新窗口
        # 这里只是一个简单的示例，每次点击都打开相同的窗口
        new_window = NewWindow('新窗口')
        new_window.show()
        self.new_windows.append(new_window)  # 添加到跟踪列表

    def closeEvent(self, event: QEvent) -> None:
        # 关闭所有新窗口
        for window in self.new_windows:
            window.close()
        self.new_windows.clear()  # 清空列表
        super().closeEvent(event)  # 调用基类方法来实际关闭主窗口

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())