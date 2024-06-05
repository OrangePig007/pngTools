# main_window.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QStackedWidget, QWidget, QLabel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from image_processor_page import ImageProcessorPage
from slice_page import SlicePage  # 导入新子页面类
from PyQt5.QtCore import QFile, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('多功能工具')
        self.setGeometry(100, 100, 800, 600)
        
        style_sheet = QFile("style.qss")
        style_sheet.open(QFile.ReadOnly | QFile.Text)
        self.setStyleSheet(str(style_sheet.readAll(), encoding='utf-8'))

        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QFontDatabase

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        self.stacked_widget = QStackedWidget()

        # 创建子页面实例，并传递对 stacked_widget 的引用
        self.image_processor_page = ImageProcessorPage(self.stacked_widget, self)
        self.stacked_widget.addWidget(self.image_processor_page)
        self.slice_page = SlicePage(self.stacked_widget, self)
        self.stacked_widget.addWidget(self.slice_page)
        
        # 初始页面
        self.home_page = QWidget()
        self.initHomePage()
        self.stacked_widget.addWidget(self.home_page)

        main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(main_widget)

        # 显示初始页面
        self.stacked_widget.setCurrentWidget(self.home_page)

    def initHomePage(self):
            layout = QVBoxLayout()

            # 创建第一个水平布局
            h_layout1 = QHBoxLayout()
            
            # 创建第一个按钮
            image_processor_label1 = QLabel(self.home_page)
            pixmap1 = QPixmap('pic/shrink.png')  # 用你的图像文件替换 'image_processor_icon.png'
            image_processor_label1.setPixmap(pixmap1.scaled(500, 500, Qt.KeepAspectRatio))  # 设置图片并启用等比例缩放
            image_processor_label1.setAlignment(Qt.AlignCenter)  # 居中对齐
            image_processor_label1.mousePressEvent = lambda event, arg=self.image_processor_page: self.stacked_widget.setCurrentWidget(arg)
            h_layout1.addWidget(image_processor_label1)

            # 创建第二个按钮
            slice_page_label1 = QLabel(self.home_page)
            pixmap2 = QPixmap('pic/slice.png')  # 用你的图像文件替换 'slice_page_icon.png'
            slice_page_label1.setPixmap(pixmap2.scaled(500, 500, Qt.KeepAspectRatio))  # 设置图片并启用等比例缩放
            slice_page_label1.setAlignment(Qt.AlignCenter)  # 居中对齐
            slice_page_label1.mousePressEvent = lambda event, arg=self.slice_page: self.stacked_widget.setCurrentWidget(arg)
            h_layout1.addWidget(slice_page_label1)

            # 将第一个水平布局添加到垂直布局中
            layout.addLayout(h_layout1)

            # 创建第二个水平布局
            h_layout2 = QHBoxLayout()

            # 创建第三个按钮
            image_processor_btn2 = QPushButton('裁剪PNG空白区域', self.home_page)
            image_processor_btn2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.image_processor_page))
            h_layout2.addWidget(image_processor_btn2)

            # 创建第四个按钮
            slice_page_btn2 = QPushButton('将PNG不粘连部分切割成块', self.home_page)
            slice_page_btn2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.slice_page))
            h_layout2.addWidget(slice_page_btn2)

            # 将第二个水平布局添加到垂直布局中
            layout.addLayout(h_layout2)

            self.home_page.setLayout(layout)
    def get_main_page_index(self):
        return self.stacked_widget.indexOf(self.home_page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
