import sys

from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, \
    QSizePolicy, QFileDialog, QMessageBox, QRadioButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

import FCA
import ICA
import PCA


class ImageWindow(QWidget):
    def __init__(self):
        super(ImageWindow, self).__init__()
        font = QFont("Arial", 12)
        initial_image = QPixmap("no-img.jpg")
        self.selected_method = ""

        self.image_label1 = QLabel()
        pixmap1 = QPixmap(initial_image)
        self.image_label1.setPixmap(pixmap1)

        self.image_label2 = QLabel()
        pixmap2 = QPixmap(initial_image)
        self.image_label2.setPixmap(pixmap2)

        self.radio_pca = QRadioButton("PCA", self)
        self.radio_ica = QRadioButton("ICA", self)
        self.radio_fca = QRadioButton("FCA", self)

        self.radio_pca.setEnabled(False)
        self.radio_ica.setEnabled(False)
        self.radio_fca.setEnabled(False)

        self.scroll_area1 = QScrollArea()
        self.scroll_area1.setWidget(self.image_label1)

        self.scroll_area2 = QScrollArea()
        self.scroll_area2.setWidget(self.image_label2)

        self.zoom_in_button1 = QPushButton("Приблизить 1")
        self.zoom_out_button1 = QPushButton("Отдалить 1")
        self.zoom_in_button2 = QPushButton("Приблизить 2")
        self.zoom_out_button2 = QPushButton("Отдалить 2")

        self.new_label = QLabel(self)
        self.new_label.setText("Исходное изображение:")
        self.new_label.setFont(font)
        self.new_label.adjustSize()

        self.new_label.move(600, 200)

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
        image_layout.setAlignment(Qt.AlignCenter)
        image_layout.setContentsMargins(350, 0, 0, 800)
        self.scroll_area1.setFixedSize(400, 400)
        self.scroll_area2.setFixedSize(400, 400)
        self.scroll_area1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.scroll_area2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.method_label = QLabel(self)
        self.method_label.move(700, 100)
        self.method_label.setFont(font)
        self.method_label.adjustSize()

        self.file_btn = QPushButton(self)
        self.file_btn.move(50, 100)
        self.file_btn.setText("Выбрать файл")
        self.file_btn.setFixedSize(200, 70)
        self.file_btn.setFont(font)
        self.file_btn.clicked.connect(self.open_file_dialog)

        self.btn_process = QPushButton("Обработать изображение", self)
        self.btn_process.move(50, 400)
        self.btn_process.setFixedSize(200, 70)
        self.btn_process.setFont(font)
        self.btn_process.setEnabled(False)
        self.btn_process.clicked.connect(self.process_image)

        self.save_processed_btn = QPushButton(self)
        self.save_processed_btn.move(50, 800)
        self.save_processed_btn.setText("Сохранить обработанное изображение")
        self.save_processed_btn.setFixedSize(420, 70)
        self.save_processed_btn.setFont(font)
        self.save_processed_btn.setEnabled(False)
        self.save_processed_btn.clicked.connect(self.save_processed_image)

        new_button_layout = QVBoxLayout()
        new_button_layout.addWidget(self.file_btn)
        new_button_layout.addWidget(self.radio_pca)
        new_button_layout.addWidget(self.radio_ica)
        new_button_layout.addWidget(self.radio_fca)
        new_button_layout.addWidget(self.btn_process)
        new_button_layout.addWidget(self.save_processed_btn)
        self.file_btn.setFixedSize(300, 50)
        self.btn_process.setFixedSize(300, 50)
        self.save_processed_btn.setFixedSize(300, 50)

        main_layout = QVBoxLayout()
        main_layout.addLayout(new_button_layout)
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
        new_pixmap = current_pixmap.scaled(new_size, aspectRatioMode=Qt.KeepAspectRatio,
                                           transformMode=Qt.SmoothTransformation)
        self.image_label1.setPixmap(new_pixmap)

    def zoom_out_image1(self):
        current_pixmap = self.image_label1.pixmap()
        current_size = current_pixmap.size()
        new_size = current_size * 0.8
        new_pixmap = current_pixmap.scaled(new_size, aspectRatioMode=Qt.KeepAspectRatio,
                                           transformMode=Qt.SmoothTransformation)
        self.image_label1.setPixmap(new_pixmap)

    def zoom_in_image2(self):
        current_pixmap = self.image_label2.pixmap()
        current_size = current_pixmap.size()
        new_size = current_size * 1.2
        new_pixmap = current_pixmap.scaled(new_size, aspectRatioMode=Qt.KeepAspectRatio,
                                           transformMode=Qt.SmoothTransformation)
        self.image_label2.setPixmap(new_pixmap)

    def zoom_out_image2(self):
        current_pixmap = self.image_label2.pixmap()
        current_size = current_pixmap.size()
        new_size = current_size * 0.8
        new_pixmap = current_pixmap.scaled(new_size, aspectRatioMode=Qt.KeepAspectRatio,
                                           transformMode=Qt.SmoothTransformation)
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
                self.save_processed_btn.setEnabled(True)
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
                self.save_processed_btn.setEnabled(True)
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
                self.save_processed_btn.setEnabled(True)
                pass

    def add_label(self):
        self.method_label.setText(self.selected_method)
        self.method_label.move(1350, 200)
        self.method_label.adjustSize()

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

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label1.setPixmap(pixmap)
        self.image_label1.adjustSize()

    def save_processed_image(self):
        processed_image = None
        if self.selected_method == "PCA":
            processed_image = PCA.function(self.file_name)
        elif self.selected_method == "ICA":
            processed_image = ICA.function(self.file_name)
        elif self.selected_method == "FCA":
            processed_image = FCA.function(self.file_name)
        else:
            error_message = "Вы не выбрали изображение"
            QMessageBox.critical(self, "Ошибка", error_message)
            return

        if processed_image is not None:
            save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Image Files (*.jpg *.png)")
            if save_path:
                processed_image.save(save_path)
        else:
            print("Изображение не было обработано")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())
