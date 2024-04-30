import matplotlib
from PyQt5.QtGui import QImage

matplotlib.use('TkAgg')
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def function(image_path):
    # Загрузка изображения
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    mean = 0
    var = 1.9
    sigma = var ** 0.5
    # Создание гауссовского шума для каждого канала
    gaussian_noise = np.random.normal(mean, sigma, (h, w, 3))
    noisy_image = img  # cv2.add(img, gaussian_noise.astype('uint8'))

    # Преобразование цветного изображения в матрицу для PCA
    img_flattened = noisy_image.reshape(h * w, 3).astype(np.float64)

    # Применение PCA для уменьшения шума, оставляем только 1 компонент
    n_components = 1
    pca = PCA(n_components=n_components)
    img_pca = pca.fit_transform(img_flattened)

    # Обратное преобразование после уменьшения размерности
    img_restored = pca.inverse_transform(img_pca)
    img_restored = img_restored.reshape(h, w, 3).astype(np.uint8)

    # Сглаживание с помощью фильтра Гаусса
    smoothed_img = cv2.GaussianBlur(img_restored, (5, 5), 0)

    # Повышение четкости с помощью фильтра увеличения резкости
    sharp_img = cv2.filter2D(img_restored, -1, np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))

    image = cv2.cvtColor(sharp_img, cv2.COLOR_BGR2RGB)
    height, width, channel = image.shape
    bytesPerLine = 3 * width
    qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return qImg
