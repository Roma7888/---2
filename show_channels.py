import rasterio
import matplotlib.pyplot as plt


def display_all_channels(input_tif):
    """
    Выводит все 10 каналов спутникового изображения в виде отдельных графиков с цветными палитрами.

    Параметры:
    - input_tif (str): Путь к входному .tif файлу (10-канальное изображение).
    """
    # Открываем изображение и считываем данные
    with rasterio.open(input_tif) as src:
        img = src.read()
        assert img.shape[0] == 10, "Ожидалось 10 каналов в изображении"

    # Определяем цветовую палитру для каждого канала
    color_maps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'twilight', 'spring', 'summer', 'autumn',
                  'winter']

    # Настраиваем размер графика для отображения 10 каналов в сетке 2x5
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))

    # Выводим каждый канал на отдельном подграфике
    for i in range(10):
        ax = axes[i // 5, i % 5]
        ax.imshow(img[i], cmap=color_maps[i])
        ax.set_title(f"Channel {i + 1}", fontsize=10)
        ax.axis('off')  # Убираем оси для более чистого вида

    plt.tight_layout()  # Плотная компоновка без основного заголовка
    plt.show()
