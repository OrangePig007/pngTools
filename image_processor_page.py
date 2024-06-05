# image_processor_page.py
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
from PyQt5.QtCore import QFile

class ImageProcessorPage(QWidget):
    def __init__(self, stacked_widget, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window  # 将MainWindow对象存储在实例变量中
        self.initUI()

    def initUI(self):
        self.input_dir = ''
        self.output_dir = ''

        layout = QVBoxLayout()
        
        # 添加演示图片
        self.demo_image_label = QLabel(self)
        demo_image_path = 'pic/shrink.png'  # 替换为你的演示图片路径
        self.demo_image_label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.demo_image_label.setPixmap(QPixmap(demo_image_path).scaledToWidth(380, Qt.SmoothTransformation))
        layout.addWidget(self.demo_image_label)
        
        # 创建水平布局放置输入和输出按钮
        h_layout = QHBoxLayout()

        self.input_btn = QPushButton('选择输入文件夹', self)
        self.input_btn.clicked.connect(self.select_input_directory)
        h_layout.addWidget(self.input_btn)
        
        self.output_btn = QPushButton('选择输出文件夹', self)
        self.output_btn.clicked.connect(self.select_output_directory)
        h_layout.addWidget(self.output_btn)

        layout.addLayout(h_layout)

        self.process_btn = QPushButton('执行', self)
        self.process_btn.setObjectName("excButton")
        self.process_btn.clicked.connect(self.process_images)
        layout.addWidget(self.process_btn)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)
        
        # 添加返回按钮
        self.back_btn = QPushButton('返回主页面', self)
        self.back_btn.setObjectName("backButton")
        self.back_btn.clicked.connect(self.back_to_main)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)
        self.setWindowTitle('图像处理工具')

        style_sheet = QFile("style.qss")
        style_sheet.open(QFile.ReadOnly | QFile.Text)
        self.setStyleSheet(str(style_sheet.readAll(), encoding='utf-8'))

    def select_input_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, '选择输入文件夹')
        if dir_name:
            self.input_dir = dir_name
            self.status_label.setText(f'输入文件夹: {self.input_dir}')

    def select_output_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, '选择输出文件夹')
        if dir_name:
            self.output_dir = dir_name
            self.status_label.setText(f'输出文件夹: {self.output_dir}')

    def process_images(self):
        if not self.input_dir or not self.output_dir:
            QMessageBox.warning(self, '警告', '请先选择输入文件夹和输出文件夹')
            return

        self.status_label.setText('正在处理...')
        try:
            self.process_directory(self.input_dir, self.output_dir)
            self.status_label.setText('处理完成！')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'处理过程中出现错误: {str(e)}')
            self.status_label.setText('处理失败')

    def back_to_main(self):
        main_page_index = self.main_window.get_main_page_index()
        self.stacked_widget.setCurrentIndex(main_page_index)


    def trim_image(self, image):
        """将图像透明边缘缩小至有颜色的地方"""
        # 获取图像的像素数据
        image_data = image.getdata()
        
        # 获取图像的宽度和高度
        width, height = image.size
        
        # 初始化边界
        left = width
        top = height
        right = 0
        bottom = 0
        
        # 遍历所有像素，找到非透明区域的边界
        for y in range(height):
            for x in range(width):
                # 获取像素的透明度
                alpha = image_data[y * width + x][3]
                
                if alpha != 0:  # 非透明像素
                    if x < left:
                        left = x
                    if x > right:
                        right = x
                    if y < top:
                        top = y
                    if y > bottom:
                        bottom = y

        # 裁剪图像
        trimmed_image = image.crop((left, top, right + 1, bottom + 1))
        return trimmed_image

    def process_directory(self, input_dir, output_dir):
        """处理目录中的所有图像"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename in os.listdir(input_dir):
            if filename.lower().endswith('.png'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                image = Image.open(input_path).convert("RGBA")
                trimmed_image = self.trim_image(image)
                trimmed_image.save(output_path)
