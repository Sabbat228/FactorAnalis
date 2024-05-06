import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QMenu, QAction, QWidget, \
    QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import QSize, QEventLoop
from PyQt5.QtGui import QPixmap, QFont

from FCA import function
import FCA
import ICA
import PCA
import locale


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.saved_number = None
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        font = QFont()
        font.setPointSize(11)
        initial_image = QPixmap("no-img.jpg")
        self.file_name = None
        self.selected_method = ""
        self.setWindowTitle("Simple program")

        self.new_text = QLabel(self)

        main_text = QLabel(self)
        main_text.move(600, 200)
        main_text.setText("Изначальное изображение:")
        main_text.setFont(font)
        main_text.adjustSize()


        self.method_label = QLabel(self)
        self.method_label.move(700, 100)
        self.method_label.setFont(font)
        self.method_label.adjustSize()
        self.image_label1 = QLabel(self)
        self.image_label1.setFixedSize(800, 800)
        self.image_label1.setPixmap(initial_image)

        self.image_label2 = QLabel(self)
        self.image_label2.setFixedSize(500, 500)

        layout = QHBoxLayout()
        layout.setContentsMargins(300, 0, 0, 0)
        layout.addWidget(self.image_label1)
        layout.addWidget(self.image_label2)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.popup_menu = QMenu(self)
        self.popup_menu.setFixedSize(200, 110)
        self.popup_menu.setFont(font)
        PCA_action = QAction("PCA", self)
        ICA_action = QAction("ICA", self)
        FCA_action = QAction("FCA", self)
        self.popup_menu.addAction(PCA_action)
        self.popup_menu.addAction(ICA_action)
        self.popup_menu.addAction(FCA_action)

        btn = QPushButton(self)
        btn.move(50, 400)
        btn.setText("Методы")
        btn.setFixedSize(200, 70)
        btn.setFont(font)
        btn.setMenu(self.popup_menu)

        PCA_action.triggered.connect(self.PCA_triggered)
        ICA_action.triggered.connect(self.ICA_triggered)
        FCA_action.triggered.connect(self.FCA_triggered)
        btn.clicked.connect(self.add_label)

        file_btn = QPushButton(self)
        file_btn.move(50, 200)
        file_btn.setText("Выбрать файл")
        file_btn.setFixedSize(200, 70)
        file_btn.setFont(font)
        file_btn.clicked.connect(self.open_file_dialog)

        save_processed_btn = QPushButton(self)
        save_processed_btn.move(50, 800)
        save_processed_btn.setText("Сохранить обработанное изображение")
        save_processed_btn.setFixedSize(420, 70)
        save_processed_btn.setFont(font)
        save_processed_btn.clicked.connect(self.save_processed_image)

        self.number_input = QLineEdit(self)
        self.number_input.setGeometry(50, 520, 100, 30)  # Укажите координаты и размер поля ввода
        self.number_input.setFixedSize(200, 50)
        self.number_input.setFont(font)
        self.number_input.setVisible(False)  # Начально скрываем поле ввода

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
        self.number_input.setVisible(True)
        self.number_input.textChanged.connect(self.save_number)

        pixmap5 = QPixmap(image_path)
        pixmap5 = pixmap5.scaled(QSize(500, 500))

        self.image_label1.setPixmap(pixmap5)

        loop = QEventLoop()
        self.number_input.returnPressed.connect(loop.quit)
        loop.exec_()
        self.number_input.setVisible(False)

        processed_image = function(image_path, self.saved_number)
        pixmap6 = QPixmap(processed_image)
        pixmap6 = pixmap6.scaled(QSize(500, 500))

        self.image_label2.setPixmap(pixmap6)

    def add_label(self):
        self.method_label.setText(self.selected_method)
        self.method_label.move(1350, 200)
        self.method_label.adjustSize()

    def save_number(self):
        number_text = self.number_input.text()
        try:
            number = int(number_text)
            self.saved_number = number
            self.popup_menu.setEnabled(True)
        except ValueError:
            pass

def application():
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
