import sys

from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, \
    QSizePolicy, QRadioButton, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

import FCA
import ICA
import PCA


class ImageWindow(QMainWindow):
    def __init__(self, image_path1, image_path2):
        super(ImageWindow, self).__init__()
        font = QFont("Arial", 12)

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

        self.zoom_in_button1.clicked.connect(self.zoom_in_image1)
        self.zoom_out_button1.clicked.connect(self.zoom_out_image1)
        self.zoom_in_button2.clicked.connect(self.zoom_in_image2)
        self.zoom_out_button2.clicked.connect(self.zoom_out_image2)
        self.scroll_area1.setMinimumSize(self.size())
        self.scroll_area2.setMinimumSize(self.size())

        self.scroll_area1.setWidgetResizable(True)
        self.scroll_area2.setWidgetResizable(True)

        self.radio_pca = QRadioButton("PCA", self)
        self.radio_ica = QRadioButton("ICA", self)
        self.radio_fca = QRadioButton("FCA", self)

        self.radio_pca.setEnabled(False)
        self.radio_ica.setEnabled(False)
        self.radio_fca.setEnabled(False)

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

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 100, 100, 600)

        self.btn_process = QPushButton("Обработать изображение", self)
        self.btn_process.move(50, 400)
        self.btn_process.setFixedSize(200, 70)
        self.btn_process.setFont(font)
        self.btn_process.setEnabled(False)
        self.btn_process.clicked.connect(self.process_image)

        layout.addWidget(self.radio_pca)
        layout.addWidget(self.radio_ica)
        layout.addWidget(self.radio_fca)
        layout.addWidget(self.btn_process)
        self.setLayout(layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        file_btn = QPushButton(self)
        file_btn.move(50, 100)
        file_btn.setText("Выбрать файл")
        file_btn.setFixedSize(200, 70)
        file_btn.setFont(font)
        file_btn.clicked.connect(self.open_file_dialog)

        main_layout = QVBoxLayout()
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout1)
        main_layout.addLayout(button_layout2)

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

    def process_image(self):
        if self.btn_process.isEnabled():
            if self.radio_pca.isChecked():
                self.selected_method = "PCA"
                self.add_label()
                image_path = self.file_name

                pixmap1 = QPixmap(image_path)
                pixmap1 = pixmap1.scaled(QSize(500, 500))

                processed_image = PCA.function(image_path)
                pixmap2 = QPixmap(processed_image)
                pixmap2 = pixmap2.scaled(QSize(500, 500))

                self.image_label1.setPixmap(pixmap1)
                self.image_label2.setPixmap(pixmap2)
            elif self.radio_ica.isChecked():
                self.selected_method = "ICA"
                self.add_label()
                image_path = self.file_name

                pixmap3 = QPixmap(image_path)
                pixmap3 = pixmap3.scaled(QSize(500, 500))

                processed_image = ICA.function(image_path)
                pixmap4 = QPixmap(processed_image)
                pixmap4 = pixmap4.scaled(QSize(500, 500))

                self.image_label1.setPixmap(pixmap3)
                self.image_label2.setPixmap(pixmap4)
                self.image_label2.adjustSize()
                pass
            elif self.radio_fca.isChecked():
                self.selected_method = "FCA"
                self.add_label()
                image_path = self.file_name

                pixmap5 = QPixmap(image_path)
                pixmap5 = pixmap5.scaled(QSize(500, 500))

                self.image_label1.setPixmap(pixmap5)

                processed_image = FCA.function(image_path)
                pixmap6 = QPixmap(processed_image)
                pixmap6 = pixmap6.scaled(QSize(500, 500))

                self.image_label2.setPixmap(pixmap6)
                self.image_label2.adjustSize()
                pass

    def open_file_dialog(self):
        options = QFileDialog.Options()

        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "",
                                                   "All Files (*);;Image Files (*.jpg *.png)", options=options)
        if file_name:
            print("Выбранный файл:", file_name)
            self.load_image(file_name)
        self.file_name = file_name
        self.radio_pca.setEnabled(True)
        self.radio_ica.setEnabled(True)
        self.radio_fca.setEnabled(True)
        self.btn_process.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow("60136e84e7fd3ae2eeb153747c92d786.jpeg",
                         "60136e84e7fd3ae2eeb153747c92d786.jpeg")  # Путь к двум изображениям
    window.show()
    sys.exit(app.exec_())