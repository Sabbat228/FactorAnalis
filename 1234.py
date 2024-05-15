import sys

from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, \
    QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageWindow(QWidget):
    def __init__(self, image_path1, image_path2):
        super(ImageWindow, self).__init__()

        self.image_label1 = QLabel()
        pixmap1 = QPixmap(image_path1)
        self.image_label1.setPixmap(pixmap1)

        self.image_label2 = QLabel()
        pixmap2 = QPixmap(image_path2)
        self.image_label2.setPixmap(pixmap2)

        self.scroll_area1 = QScrollArea()
        self.scroll_area1.setWidget(self.image_label1)

        self.scroll_area2 = QScrollArea()
        self.scroll_area2.setWidget(self.image_label2)

        self.zoom_in_button1 = QPushButton("Приблизить 1")
        self.zoom_out_button1 = QPushButton("Отдалить 1")
        self.zoom_in_button2 = QPushButton("Приблизить 2")
        self.zoom_out_button2 = QPushButton("Отдалить 2")

        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.zoom_in_button1)
        button_layout1.addWidget(self.zoom_out_button1)
        self.zoom_in_button1.setFixedSize(100, 50)
        self.zoom_out_button1.setFixedSize(100, 50)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.zoom_in_button2)
        button_layout2.addWidget(self.zoom_out_button2)
        self.zoom_in_button2.setFixedSize(100, 50)
        self.zoom_out_button2.setFixedSize(100, 50)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.scroll_area1)
        image_layout.addWidget(self.scroll_area2)
        self.scroll_area1.setFixedSize(400, 400)
        self.scroll_area2.setFixedSize(400, 400)
        self.scroll_area1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.scroll_area2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        main_layout = QVBoxLayout()
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout1)
        main_layout.addLayout(button_layout2)

        self.setLayout(main_layout)

        self.zoom_in_button1.clicked.connect(self.zoom_in_image1)
        self.zoom_out_button1.clicked.connect(self.zoom_out_image1)
        self.zoom_in_button2.clicked.connect(self.zoom_in_image2)
        self.zoom_out_button2.clicked.connect(self.zoom_out_image2)
        self.scroll_area1.setMinimumSize(self.size())
        self.scroll_area2.setMinimumSize(self.size())

        self.scroll_area1.setWidgetResizable(True)
        self.scroll_area2.setWidgetResizable(True)

    def zoom_in_image1(self):
        current_pixmap = self.image_label1.pixmap()
        current_size = current_pixmap.size()
        new_size = current_size * 1.2
        new_pixmap = current_pixmap.scaled(new_size, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image_label1.setPixmap(new_pixmap)

    def zoom_out_image1(self):
        current_pixmap = self.image_label1.pixmap()
        current_size = current_pixmap.size()
        new_size = current_size * 0.8
        new_pixmap = current_pixmap.scaled(new_size, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image_label1.setPixmap(new_pixmap)

    def zoom_in_image2(self):
        current_pixmap = self.image_label2.pixmap()
        current_size = current_pixmap.size()
        new_size = current_size * 1.2
        new_pixmap = current_pixmap.scaled(new_size, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image_label2.setPixmap(new_pixmap)

    def zoom_out_image2(self):
        current_pixmap = self.image_label2.pixmap()
        current_size = current_pixmap.size()
        new_size = current_size * 0.8
        new_pixmap = current_pixmap.scaled(new_size, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image_label2.setPixmap(new_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow("60136e84e7fd3ae2eeb153747c92d786.jpeg",
                         "60136e84e7fd3ae2eeb153747c92d786.jpeg")  # Путь к двум изображениям
    window.show()
    sys.exit(app.exec_())