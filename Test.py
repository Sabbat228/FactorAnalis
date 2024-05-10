import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
import cv2
import numpy as np
from sklearn.decomposition import FactorAnalysis


def function(image_path, saved_number):
    # Загрузка цветного изображения
    img = cv2.imread("2014_05_22_ris2_big.jpg")

    # Генерация шума с меньшей дисперсией
    mean = 0
    var = 0.5
    sigma = var ** 0.5
    gaussian_noise = np.random.normal(mean, sigma, img.shape)
    noisy_img = np.clip(img + gaussian_noise, 0, 255).astype(np.uint8)

    # Применение факторного анализа для удаления шумов
    fa = FactorAnalysis(n_components=1)
    img_flattened = noisy_img.reshape(-1, 3)
    img_restored = fa.fit_transform(img_flattened)

    # Обратное преобразование данных
    img_restored = np.dot(img_restored, fa.components_) + fa.mean_

    # Приведение значений к диапазону [0, 255]
    img_restored = np.clip(img_restored, 0, 255).astype(np.uint8)
    img_restored = img_restored.reshape(img.shape)

    # Отображение изначального изображения с добавленным шумом
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(noisy_img, cv2.COLOR_BGR2RGB))
    plt.title('Noisy Image')
    plt.axis('off')

    # Отображение измененного изображения после удаления шума
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img_restored, cv2.COLOR_BGR2RGB))
    plt.title('Restored Image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()
