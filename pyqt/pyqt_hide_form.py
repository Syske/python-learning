import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置布局
        self.layout = QVBoxLayout()

        # 创建一个按钮用于控制表单的显示与隐藏
        self.toggle_button = QPushButton("显示/隐藏表单")
        self.toggle_button.clicked.connect(self.toggle_form_visibility)
        self.layout.addWidget(self.toggle_button)

        # 表单容器
        self.form_layout = QFormLayout()
        
        # 添加一些表单项
        self.name_label = QLabel("姓名:")
        self.name_input = QLineEdit()
        self.email_label = QLabel("邮箱:")
        self.email_input = QLineEdit()
        
        self.form_layout.addRow(self.name_label, self.name_input)
        self.form_layout.addRow(self.email_label, self.email_input)

        # 将表单添加到主布局中
        self.layout.addLayout(self.form_layout)

        # 初始设置表单为隐藏
        self.form_visible = False
        self.toggle_form_visibility()

        # 设置窗口的布局
        self.setLayout(self.layout)

    def toggle_form_visibility(self):
        """切换表单的可见性"""
        self.form_visible = not self.form_visible
        for i in range(self.form_layout.count()):
            item = self.form_layout.itemAt(i).widget()
            if item is not None:
                item.setVisible(self.form_visible)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('动态隐藏/展开表单')
    window.show()
    sys.exit(app.exec_())