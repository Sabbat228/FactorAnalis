import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageWindow(QWidget):
    def __init__(self, image_path):
        super(ImageWindow, self).__init__()

        self.image_label = QLabel()
        self.pixmap = QPixmap(image_path)
        self.image_label.setPixmap(self.pixmap)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)

        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_out_button = QPushButton("Zoom Out")

        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.zoom_in_button)
        button_layout.addWidget(self.zoom_out_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def zoom_in(self):
        self.pixmap = self.pixmap.scaled(self.pixmap.width() * 1.2, self.pixmap.height() * 1.2, Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.resize(self.pixmap.width(), self.pixmap.height())

    def zoom_out(self):
        self.pixmap = self.pixmap.scaled(self.pixmap.width() * 0.8, self.pixmap.height() * 0.8, Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.resize(self.pixmap.width(), self.pixmap.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow("60136e84e7fd3ae2eeb153747c92d786.jpeg")
    window.show()
    sys.exit(app.exec_())