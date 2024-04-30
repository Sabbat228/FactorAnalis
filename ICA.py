import cv2
import numpy as np
from sklearn.decomposition import FastICA
from skimage import io
from sklearn.preprocessing import MinMaxScaler
from PyQt5.QtGui import QPixmap, QImage


def function(image_path):
    # Генерация гауссовского шума
    image = io.imread(image_path)
    mean = 0
    var = 5.9
    sigma = var ** 0.5
    gaussian_noise = np.random.normal(mean, sigma, image.shape).astype('uint8')

    # Добавление шума к изображению
    noisy_image = np.clip(image + gaussian_noise, 0, 255).astype(np.uint8)

    # Преобразование цветного изображения в одномерный массив
    X = noisy_image.reshape(-1, 3)

    # Нормализация значений изображения
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Применение ICA
    ica = FastICA(n_components=3, max_iter=1000, tol=0.0001)
    X_transformed = ica.fit_transform(X_scaled)

    # Восстановление изображения из преобразованных данных
    X_restored = ica.inverse_transform(X_transformed)

    # Масштабирование значений обратно в исходный диапазон
    restored_image = X_restored.reshape(noisy_image.shape)
    restored_image = (restored_image - np.min(restored_image)) / (np.max(restored_image) - np.min(restored_image)) * 255

    # Преобразование изображения к формату QImage
    restored_image = cv2.cvtColor(restored_image.astype(np.uint8), cv2.COLOR_RGB2BGR)
    height, width, channel = restored_image.shape
    bytesPerLine = 3 * width
    qImg = QPixmap(QImage(restored_image.data, width, height, bytesPerLine, QImage.Format_RGB888))

    return qImg