import numpy as np
import rasterio
from skimage.morphology import binary_dilation, binary_erosion
from skimage.filters import threshold_otsu

def detect_water_from_single_file(input_tif, output_path):
    """
    Функция для обнаружения водных объектов на данных Sentinel-2A,
    если все каналы находятся в одном .tif файле, и сохранения результата в новый файл.

    Аргументы:
    - input_tif: путь к файлу с каналами и маской
    - output_path: путь для сохранения итоговой маски водных объектов

    Возвращает:
    - None, но сохраняет бинарную маску водных объектов по указанному пути
    """
    # Открываем входной файл и читаем необходимые каналы
    with rasterio.open(input_tif) as src:
        # Читаем каналы
        green = src.read(1)  # Зеленый канал (B03)
        nir = src.read(2)    # NIR канал (B08)
        swir = src.read(3)   # SWIR канал (B11)
        mask = src.read(4)   # Маска, где 1 - вода, 0 - фон

        # Проверка на одинаковое разрешение всех каналов
        assert green.shape == nir.shape == swir.shape == mask.shape, \
            "Все каналы должны иметь одинаковое разрешение."

        # Расчет NDWI и MNDWI
        ndwi = (green - nir) / (green + nir)
        mndwi = (green - swir) / (green + swir)

        # Проверка диапазона индексов
        print(f"Диапазон NDWI: {ndwi.min()} - {ndwi.max()}")
        print(f"Диапазон MNDWI: {mndwi.min()} - {mndwi.max()}")

        # Применение порога Otsu для бинаризации NDWI и MNDWI
        threshold_ndwi = threshold_otsu(ndwi)
        threshold_mndwi = threshold_otsu(mndwi)
        print(f"Порог Otsu для NDWI: {threshold_ndwi}")
        print(f"Порог Otsu для MNDWI: {threshold_mndwi}")

        water_mask_ndwi = ndwi > threshold_ndwi
        water_mask_mndwi = mndwi > threshold_mndwi

        # Объединение результатов NDWI и MNDWI для повышения точности
        water_mask = water_mask_ndwi | water_mask_mndwi

        # Применение маски для выделения водных объектов
        water_mask = np.where(mask == 1, water_mask, 0)

        # Морфологическая обработка
        water_mask = binary_dilation(water_mask, footprint=np.ones((3, 3)))
        water_mask = binary_erosion(water_mask, footprint=np.ones((3, 3)))

    # Преобразование в целочисленные значения и добавление цветовой карты
    water_mask = water_mask.astype(rasterio.uint8) * 255  # Вода = 255, фон = 0

    # Сохранение результата с цветовой картой
    with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=src.height,
            width=src.width,
            count=1,
            dtype=rasterio.uint8,
            crs=src.crs,
            transform=src.transform,
    ) as dst:
        dst.write(water_mask, 1)

        # Применение цветовой карты (синий цвет для воды)
        cmap = {
            0: (0, 0, 0),         # фон - черный
            255: (0, 0, 255)      # вода - синий
        }
        dst.write_colormap(1, cmap)

    print(f"Обнаружение водных объектов завершено, результат сохранен в '{output_path}'")
    
