import matplotlib
from PyQt5.QtGui import QPixmap, QImage
from matplotlib import pyplot as plt

matplotlib.use('TkAgg')
import cv2
import numpy as np
from sklearn.decomposition import FactorAnalysis


def function(image_path, saved_number):
    # Загрузка цветного изображения
    img = cv2.imread(image_path)

    # Генерация шума с меньшей дисперсией
    mean = 0
    var = 3000.5
    sigma = var ** 0.5
    gaussian_noise = np.random.normal(mean, sigma, img.shape)
    noisy_img = np.clip(img + gaussian_noise, 0, 255).astype(np.uint8)

    # Применение факторного анализа для удаления шумов
    fa = FactorAnalysis(n_components=saved_number)
    img_flattened = noisy_img.reshape(-1, 3)
    img_restored = fa.fit_transform(img_flattened)

    # Обратное преобразование данных
    img_restored = np.dot(img_restored, fa.components_) + fa.mean_

    # Приведение значений к диапазону [0, 255]
    img_restored = np.clip(img_restored, 0, 255).astype(np.uint8)
    img_restored = img_restored.reshape(img.shape)

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(noisy_img, cv2.COLOR_BGR2RGB))
    plt.title('Noisy Image')
    plt.axis('off')

    # Отображение измененного изображения после удаления шума
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img_restored, cv2.COLOR_BGR2RGB))
    plt.title('Restored Image')
    plt.axis('off')
    plt.show()

    # Создание объекта QImage из восстановленного изображения
    height, width, _ = img_restored.shape
    qImg = QImage(img_restored.data, width, height, width * 3, QImage.Format_RGB888)

    # Создание объекта QPixmap из QImage
    pixmap = QPixmap.fromImage(qImg)

    return pixmap
