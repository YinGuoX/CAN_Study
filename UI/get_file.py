from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFormLayout, QRadioButton
from PyQt5.QtWidgets import QFileDialog

'''
QT界面中 选择多个文件
'''

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        # 读取Excel文件路径按钮
        self.chose_excel_button = QtWidgets.QPushButton()
        self.chose_excel_button.setObjectName("GetExcelPathButton")
        self.chose_excel_button.setText("请选择读取的Excel文件")
        # 工具界面日志
        self.log_TextEdit = QtWidgets.QTextEdit()
        # 业务相关
        self.excel_path = None

    def main_window(self):
        self.setWindowTitle("选取文件")
        form_layout = QFormLayout()
        form_layout.addRow(self.chose_excel_button)
        self.chose_excel_button.setCheckable(True)
        self.chose_excel_button.clicked.connect(lambda: self.click_find_file_path(self.chose_excel_button))
        form_layout.addRow("日志信息：", self.log_TextEdit)
        self.setLayout(form_layout)

    def click_find_file_path(self, button):
        # 设置文件扩展名过滤，同一个类型的不同格式如xlsx和xls 用空格隔开
        # filename, filetype = QFileDialog.getOpenFileName(self, "选取Excel文件", "./data",
        #                                                  "Excel Files (*.xls *.xlsx)")
        filename, filetype = QtWidgets.QFileDialog.getOpenFileNames(self, "多文件选择", "./", "所有文件 (*);;文本文件 (*.txt)")
        print(filename)
        print(filetype)
        if button.text() == "请选择读取的Excel文件":
            if button.isChecked():
                self.excel_path = filename
                self.log_TextEdit.append("需要读取的Excel路径为:" + filename)
                self.log_TextEdit.append("文件格式为:" + filetype)
        button.toggle()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = MyWindow()
    main.main_window()
    main.show()
    sys.exit(app.exec_())

