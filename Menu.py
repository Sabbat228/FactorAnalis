import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QMenu, QAction, QWidget, \
    QFileDialog, QMessageBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap

import FCA
import ICA
import PCA
import locale


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        self.file_name = None
        self.selected_method = ""
        self.setWindowTitle("Simple program")

        self.new_text = QLabel(self)

        main_text = QLabel(self)
        main_text.setText("Изначальное изображение:")
        main_text.move(500, 200)
        main_text.adjustSize()

        self.method_label = QLabel(self)
        self.method_label.move(500, 100)
        self.method_label.adjustSize()
        self.image_label1 = QLabel(self)
        self.image_label1.setFixedSize(500, 500)

        self.image_label2 = QLabel(self)
        self.image_label2.setFixedSize(500, 500)

        layout = QHBoxLayout()
        layout.addWidget(self.image_label1)
        layout.addWidget(self.image_label2)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.popup_menu = QMenu(self)
        PCA_action = QAction("PCA", self)
        ICA_action = QAction("ICA", self)
        FCA_action = QAction("FCA", self)
        self.popup_menu.addAction(PCA_action)
        self.popup_menu.addAction(ICA_action)
        self.popup_menu.addAction(FCA_action)

        btn = QPushButton(self)
        btn.move(850, 800)
        btn.setText("Методы")
        btn.setFixedWidth(200)
        btn.setMenu(self.popup_menu)

        PCA_action.triggered.connect(self.PCA_triggered)
        ICA_action.triggered.connect(self.ICA_triggered)
        FCA_action.triggered.connect(self.FCA_triggered)
        btn.clicked.connect(self.add_label)

        file_btn = QPushButton(self)
        file_btn.move(600, 800)
        file_btn.setText("Выбрать файл")
        file_btn.setFixedWidth(200)
        file_btn.clicked.connect(self.open_file_dialog)

        save_processed_btn = QPushButton(self)
        save_processed_btn.move(1100, 800)
        save_processed_btn.setText("Сохранить обработанное изображение")
        save_processed_btn.setFixedWidth(400)
        save_processed_btn.clicked.connect(self.save_processed_image)

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

    def open_file_dialog(self):
        options = QFileDialog.Options()

        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "",
                                                   "All Files (*);;Image Files (*.jpg *.png)", options=options)
        if file_name:
            print("Выбранный файл:", file_name)
            self.load_image(file_name)
        self.file_name = file_name

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label1.setPixmap(pixmap)
        self.image_label1.adjustSize()

    def PCA_triggered(self):
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

    def ICA_triggered(self):
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

    def FCA_triggered(self):
        self.selected_method = "FCA"
        self.add_label()
        image_path = self.file_name

        pixmap5 = QPixmap(image_path)
        pixmap5 = pixmap5.scaled(QSize(500, 500))

        processed_image = FCA.function(image_path)
        pixmap6 = QPixmap(processed_image)
        pixmap6 = pixmap6.scaled(QSize(500, 500))

        self.image_label1.setPixmap(pixmap5)
        self.image_label2.setPixmap(pixmap6)

    def add_label(self):
        self.method_label.setText(self.selected_method)
        self.method_label.move(1350, 200)
        self.method_label.adjustSize()


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
