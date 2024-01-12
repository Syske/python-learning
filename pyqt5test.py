import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
 
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("My Window")
        
        # 创建按钮对象
        button = QPushButton('点击我', self)
        button.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        print("按钮被点击了！")
        # 这里可以写需要执行的代码
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())