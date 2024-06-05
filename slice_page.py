# slice_page.py
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import QFile

class SlicePage(QWidget):
    def __init__(self, stacked_widget, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window  # 将MainWindow对象存储在实例变量中
        self.initUI()

        
    def initUI(self):
        self.image_path = ''
        self.output_dir = ''

        layout = QVBoxLayout()
        
        # 添加演示图片
        self.demo_image_label = QLabel(self)
        demo_image_path = 'pic/slice.png'  # 替换为你的演示图片路径
        self.demo_image_label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.demo_image_label.setPixmap(QPixmap(demo_image_path).scaledToWidth(380, Qt.SmoothTransformation))
        layout.addWidget(self.demo_image_label)
        
        # 创建水平布局放置输入和输出按钮
        h_layout = QHBoxLayout()

        self.input_btn = QPushButton('选择输入文件', self)
        self.input_btn.clicked.connect(self.select_input_file)
        h_layout.addWidget(self.input_btn)
        
        self.output_btn = QPushButton('选择输出文件夹', self)
        self.output_btn.clicked.connect(self.select_output_directory)
        h_layout.addWidget(self.output_btn)

        layout.addLayout(h_layout)

        self.process_btn = QPushButton('执行', self)
        self.process_btn.setObjectName("excButton")
        self.process_btn.clicked.connect(self.process_image)
        layout.addWidget(self.process_btn)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)
        
        # 添加返回按钮
        self.back_btn = QPushButton('返回主页面', self)
        self.back_btn.setObjectName("backButton")
        self.back_btn.clicked.connect(self.back_to_main)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)
        self.setWindowTitle('图像分割工具')

        style_sheet = QFile("style.qss")
        style_sheet.open(QFile.ReadOnly | QFile.Text)
        self.setStyleSheet(str(style_sheet.readAll(), encoding='utf-8'))

    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, '选择输入文件', '', 'Images (*.png *.jpg *.bmp)')
        if file_name:
            self.image_path = file_name
            self.status_label.setText(f'输入文件: {self.image_path}')

    def select_output_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, '选择输出文件夹')
        if dir_name:
            self.output_dir = dir_name
            self.status_label.setText(f'输出文件夹: {self.output_dir}')

    def process_image(self):
        if not self.image_path or not self.output_dir:
            QMessageBox.warning(self, '警告', '请先选择输入文件和输出文件夹')
            return

        self.status_label.setText('正在处理...')
        try:
            self.main_process(self.image_path, self.output_dir)
            self.status_label.setText('处理完成！')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'处理过程中出现错误: {str(e)}')
            self.status_label.setText('处理失败')

    def back_to_main(self):
        main_page_index = self.main_window.get_main_page_index()
        self.stacked_widget.setCurrentIndex(main_page_index)


    def get_connected_components(self, image):
        """根据透明度获取图片中不粘连的部分"""
        width, height = image.size
        pixels = image.load()
        visited = [[False] * height for _ in range(width)]

        def is_transparent(x, y):
            return pixels[x, y][3] == 0

        def bfs(start_x, start_y):
            queue = [(start_x, start_y)]
            component = []
            while queue:
                x, y = queue.pop(0)
                if visited[x][y]:
                    continue
                visited[x][y] = True
                component.append((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and not visited[nx][ny] and not is_transparent(nx, ny):
                        queue.append((nx, ny))
            return component

        components = []
        for x in range(width):
            for y in range(height):
                if not visited[x][y] and not is_transparent(x, y):
                    component = bfs(x, y)
                    if component:
                        components.append(component)
        return components

    def extract_components(self, image, components, output_dir, min_width=5, min_height=5):
        """提取组件并保存为单独的图片，限制最小尺寸"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for i, component in enumerate(components):
            min_x = min(x for x, y in component)
            max_x = max(x for x, y in component)
            min_y = min(y for x, y in component)
            max_y = max(y for x, y in component)
            width = max_x - min_x + 1
            height = max_y - min_y + 1

            if width >= min_width and height >= min_height:
                component_image = Image.new('RGBA', (width, height))
                draw = ImageDraw.Draw(component_image)
                for x, y in component:
                    draw.point((x - min_x, y - min_y), fill=image.getpixel((x, y)))
                component_image.save(os.path.join(output_dir, f'component_{i}.png'))

    def main_process(self, image_path, output_dir):
        image = Image.open(image_path).convert('RGBA')
        components = self.get_connected_components(image)
        self.extract_components(image, components, output_dir)
