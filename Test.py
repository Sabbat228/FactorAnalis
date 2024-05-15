from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QRadioButton, \
    QVBoxLayout, QFileDialog, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QFont

import FCA
import ICA
import PCA


class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        initial_image = QPixmap("no-img.jpg")
        font = QFont("Arial", 12)

        self.method_label = QLabel(self)
        self.method_label.move(700, 100)
        self.method_label.setFont(font)
        self.method_label.adjustSize()

        self.image_label1 = QLabel(self)
        self.image_label1.setMinimumSize(200, 200)
        self.image_label1.setFixedSize(800, 800)
        self.image_label1.setPixmap(initial_image)
        self.image_label1.adjustSize()

        self.image_label2 = QLabel(self)
        self.image_label2.setMinimumSize(200, 200)
        self.image_label2.setFixedSize(800, 800)
        self.image_label2.adjustSize()

        self.radio_pca = QRadioButton("PCA", self)
        self.radio_ica = QRadioButton("ICA", self)
        self.radio_fca = QRadioButton("FCA", self)

        self.radio_pca.setEnabled(False)
        self.radio_ica.setEnabled(False)
        self.radio_fca.setEnabled(False)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 100, 100, 600)

        h_layout_images = QHBoxLayout()

        h_layout_images.setAlignment(Qt.AlignRight)

        self.image_label1.setFixedSize(800, 800)
        self.image_label2.setFixedSize(800, 800)

        scroll_area1 = QScrollArea()
        scroll_area1.setWidget(self.image_label1)
        scroll_area1.setWidgetResizable(True)
        scroll_area1.setMinimumSize(800, 600)

        scroll_area2 = QScrollArea()
        scroll_area2.setWidget(self.image_label2)
        scroll_area2.setWidgetResizable(True)
        scroll_area2.setMinimumSize(800, 600)

        scroll_area1.setAlignment(Qt.AlignRight)
        scroll_area2.setAlignment(Qt.AlignRight)

        h_layout_images.addWidget(scroll_area1)
        h_layout_images.addWidget(scroll_area2)

        layout.addLayout(h_layout_images)

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

if __name__ == '__main__':
    app = QApplication([])
    window = ImageProcessingApp()
    window.show()
    app.exec_()